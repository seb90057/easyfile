import unittest
from easy_file.file.file import File
import os
import pathlib
import pkg_resources


class FileTest(unittest.TestCase):

    def setUp(self) -> None:
        file_path = pkg_resources.resource_filename(__name__, 'data/test_csv_with_header.csv')
        self.file = File(file_path)

    def test_get_extension(self):
        result = self.file.extension
        expected_result = 'csv'
        self.assertEqual(expected_result, result)

    def test_get_row_number(self):
        result = self.file.row_number
        expected_result = 99
        self.assertEqual(expected_result, result)

    def test_get_first_line(self):
        result = self.file.get_first_line()
        expected_result = 'cord_uid;sha;source_x;title;doi;pmcid;;license;abstract;;authors;journal;;who_covidence_id;;pdf_json_files;pmc_json_files;url\n'
        self.assertEqual(expected_result, result)

    def test_get_sample(self):
        result_list = [
            self.file.get_sample(),
            self.file.get_sample(line_number=10),
            self.file.get_sample(excluded=[3])
            ]
        expected_result_list = [
            98,
            10,
            97
        ]
        for i, result in enumerate(result_list):
            self.assertEqual(expected_result_list[i], len(result[0]))
