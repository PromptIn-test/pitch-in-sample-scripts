import io
import os
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout

from tidy_csv import main, tidy_file, tidy_rows


class TidyRowsTest(unittest.TestCase):
    def test_tidy_rows_trims_spaces_around_cells(self):
        self.assertEqual(tidy_rows([["  Ada ", " ada@example.com"]]), [["Ada", "ada@example.com"]])

    def test_tidy_rows_drops_blank_rows(self):
        self.assertEqual(tidy_rows([["a", "b"], ["", "  "], ["c", "d"]]), [["a", "b"], ["c", "d"]])

    def test_tidy_rows_keeps_rows_with_some_empty_cells(self):
        self.assertEqual(tidy_rows([["a", ""]]), [["a", ""]])

    def test_tidy_rows_keeps_duplicates_by_default(self):
        rows = [["a", "b"], ["a", "b"]]
        self.assertEqual(tidy_rows(rows), [["a", "b"], ["a", "b"]])

    def test_tidy_rows_dedupe_keeps_first_copy_in_order(self):
        rows = [["a", "1"], ["b", "2"], ["a", "1"], ["c", "3"], ["b", "2"]]
        self.assertEqual(tidy_rows(rows, dedupe=True), [["a", "1"], ["b", "2"], ["c", "3"]])

    def test_tidy_rows_dedupe_compares_after_trimming(self):
        rows = [["Ada", "x"], ["  Ada ", " x "]]
        self.assertEqual(tidy_rows(rows, dedupe=True), [["Ada", "x"]])

    def test_tidy_rows_dedupe_is_case_sensitive_and_keeps_near_matches(self):
        rows = [["Ada", "x"], ["ada", "x"], ["Ada", "x", ""], ["Ada"]]
        self.assertEqual(tidy_rows(rows, dedupe=True), rows)

    def test_tidy_rows_dedupe_still_drops_blank_rows(self):
        self.assertEqual(tidy_rows([["", ""], ["", ""], ["a"]], dedupe=True), [["a"]])

    def test_tidy_rows_dedupe_treats_header_like_any_row(self):
        rows = [["name", "email"], ["Ada", "a"], ["name", "email"]]
        self.assertEqual(tidy_rows(rows, dedupe=True), [["name", "email"], ["Ada", "a"]])


class TidyFileTest(unittest.TestCase):
    def test_tidy_file_writes_csv_and_counts_rows(self):
        source = io.StringIO("name,email\n Ada , ada@example.com\n,\n")
        target = io.StringIO()
        self.assertEqual(tidy_file(source, target), 2)
        self.assertEqual(target.getvalue(), "name,email\nAda,ada@example.com\n")

    def test_tidy_file_dedupe_drops_duplicates_and_counts_rows(self):
        source = io.StringIO("name,email\nAda,a\n Ada , a \nBob,b\nAda,a\n")
        target = io.StringIO()
        self.assertEqual(tidy_file(source, target, dedupe=True), 3)
        self.assertEqual(target.getvalue(), "name,email\nAda,a\nBob,b\n")

    def test_tidy_file_without_dedupe_keeps_duplicates(self):
        source = io.StringIO("a,b\na,b\n")
        target = io.StringIO()
        self.assertEqual(tidy_file(source, target), 2)
        self.assertEqual(target.getvalue(), "a,b\na,b\n")


class MainTest(unittest.TestCase):
    def run_main(self, args, content="a,b\n a , b \nc,d\n"):
        with tempfile.TemporaryDirectory() as folder:
            path = os.path.join(folder, "in.csv")
            with open(path, "w", encoding="utf-8", newline="") as handle:
                handle.write(content)
            out, err = io.StringIO(), io.StringIO()
            with redirect_stdout(out), redirect_stderr(err):
                code = main(["tidy_csv.py"] + [path if a == "PATH" else a for a in args])
        return code, out.getvalue(), err.getvalue()

    def test_main_without_flag_keeps_duplicates(self):
        self.assertEqual(self.run_main(["PATH"]), (0, "a,b\na,b\nc,d\n", ""))

    def test_main_dedupe_flag_before_path(self):
        self.assertEqual(self.run_main(["--dedupe", "PATH"]), (0, "a,b\nc,d\n", ""))

    def test_main_dedupe_flag_after_path(self):
        self.assertEqual(self.run_main(["PATH", "--dedupe"]), (0, "a,b\nc,d\n", ""))

    def test_main_without_path_prints_usage(self):
        code, out, err = self.run_main(["--dedupe"])
        self.assertEqual((code, out), (2, ""))
        self.assertIn("--dedupe", err)

    def test_main_with_extra_argument_prints_usage(self):
        code, _, err = self.run_main(["PATH", "PATH"])
        self.assertEqual(code, 2)
        self.assertIn("Usage", err)


if __name__ == "__main__":
    unittest.main()
