import unittest
from easy_file.file.csv_file import CsvFile
import pkg_resources
import csv
import pandas as pd
from pandas.testing import assert_frame_equal
import datetime
from easy_file.cast.constant.cdate import CDate
from easy_file.cast.constant.cboolean import CBoolean
from easy_file.cast.constant.cinteger import CInteger
from easy_file.cast.constant.cfloat import CFloat
from easy_file.cast.constant.cstring import CString


class CsvFileTest(unittest.TestCase):

    def setUp(self) -> None:
        file_path_big = pkg_resources.resource_filename(__name__, 'data/test_csv_with_header.csv')
        self.file_big = CsvFile(file_path_big)
        self.file_big.set_dialect()

        file_path_big_without_header = pkg_resources.resource_filename(__name__,
                                                        'data/test_csv_without_header.csv')
        self.file_big_without_header = CsvFile(file_path_big_without_header)
        self.file_big_without_header.set_dialect()

        file_path_big_with_issue_first_line = pkg_resources.resource_filename(__name__,
                                                        'data/test_csv_without_header_fake_first_line.csv')
        self.file_big_with_issue_first_line = CsvFile(file_path_big_with_issue_first_line)
        self.file_big_with_issue_first_line.set_dialect()

        file_path_light = pkg_resources.resource_filename(__name__, 'data/test_csv_with_header_light.csv')
        self.file_light = CsvFile(file_path_light)
        self.file_light.dialect = self.file_big.dialect
        self.file_light.headers = ['cord_uid', 'date']
        self.file_light.headers_cast = {'cord_uid': {'type': CString},
                                        'date': {'type': CDate}}
        self.file_light.has_header = True

    def test_get_headers(self):
        result = self.file_big.get_headers()
        expected_result = ['cord_uid', 'sha', 'source_x', 'title', 'doi', 'pmcid', '', 'license', 'abstract', '', 'authors', 'journal', '', 'who_covidence_id', '', 'pdf_json_files', 'pmc_json_files', 'url']
        self.assertListEqual(expected_result, result)

        result = self.file_big_without_header.get_headers()
        expected_result = ['header_{}'.format(i) for i in range(0, len(self.file_big_without_header.headers))]
        self.assertListEqual(expected_result, result)

        result = self.file_big_with_issue_first_line.get_headers()
        expected_result = ['header_{}'.format(i) for i in range(0, len(self.file_big_without_header.headers))]
        self.assertListEqual(expected_result, result)


    def test_get_headers_cast(self):
        result = self.file_big.get_headers_cast()
        expected_result = {
            'cord_uid': {
                'type': CString
            },
            'sha': {
                'type': CString
            },
            'source_x': {
                'type': CString
            },
            'title': {
                'type': CString
            },
            'doi': {
                'type': CString
            },
            'pmcid': {
                'type': CString
            },
            '': {
                'type': CInteger
            },
            'license': {
                'type': CString
            },
            'abstract': {
                'type': CString
            },
            'authors': {
                'type': CString
            },
            'journal': {
                'type': CString
            },
            'who_covidence_id': {
                'type': CFloat
            },
            'pdf_json_files': {
                'type': CString
            },
            'pmc_json_files': {
                'type': CString
            },
            'url': {
                'type': CString}
        }
        self.assertDictEqual(expected_result, result)

    def test_set_dialect(self):
        self.assertEqual(self.file_big.delimiter, ';')
        self.assertEqual(self.file_big.quotechar, '"')
        self.assertEqual(self.file_big.escapechar, None)

    def test_get_expected_column_number(self):
        _, csv_file_sample = self.file_big.get_sample(line_number=100)
        lines_sample = list(csv.reader(csv_file_sample, dialect=self.file_big.dialect))
        expected_col_nb = self.file_big.get_expected_column_number(lines_sample)
        self.assertEqual(18, expected_col_nb)

    def test_get_lines(self):
        good_lines = self.file_big.get_lines()
        self.assertEqual(97, len(good_lines))
        self.assertEqual(1, len(self.file_big.bad_lines))

    def test_get_or_create_df(self):
        result = self.file_light.get_or_create_df()
        expected_result = pd.DataFrame(data = {'line_number': [1, 2],
                                               'cord_uid': ['ug7v899j',
                                                            '02tnwd4m'],
                                               'date': ['27 01 1983',
                                                        '2010-04-10']})

        assert_frame_equal(expected_result, result, check_dtype=False)

    def test_get_converted_df(self):
        g, b = self.file_light.get_converted_df()
        expected_result = pd.DataFrame(data = {'line_number': [1, 2],
                                               'cord_uid': ['ug7v899j',
                                                            '02tnwd4m'],
                                               'date': [datetime.date(year=1983,
                                                                      month=1,
                                                                      day=27),
                                                        datetime.date(year=2010,
                                                                      month=4,
                                                                      day=10)]})
        assert_frame_equal(expected_result, g)