import io
import unittest

from tidy_csv import tidy_file, tidy_rows


class TidyRowsTest(unittest.TestCase):
    def test_tidy_rows_trims_spaces_around_cells(self):
        self.assertEqual(tidy_rows([["  Ada ", " ada@example.com"]]), [["Ada", "ada@example.com"]])

    def test_tidy_rows_drops_blank_rows(self):
        self.assertEqual(tidy_rows([["a", "b"], ["", "  "], ["c", "d"]]), [["a", "b"], ["c", "d"]])

    def test_tidy_rows_keeps_rows_with_some_empty_cells(self):
        self.assertEqual(tidy_rows([["a", ""]]), [["a", ""]])


class TidyFileTest(unittest.TestCase):
    def test_tidy_file_writes_csv_and_counts_rows(self):
        source = io.StringIO("name,email\n Ada , ada@example.com\n,\n")
        target = io.StringIO()
        self.assertEqual(tidy_file(source, target), 2)
        self.assertEqual(target.getvalue(), "name,email\nAda,ada@example.com\n")


if __name__ == "__main__":
    unittest.main()
