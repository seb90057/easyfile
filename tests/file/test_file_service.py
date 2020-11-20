import unittest
from easy_file.file.file import File
from easy_file.file.csv_file import CsvFile
from easy_file.file.file_service import get_cls_file
import pkg_resources


class FileServiceTest(unittest.TestCase):

    def setUp(self) -> None:
        csv_file_path = pkg_resources.resource_filename(__name__,
                                                        'data/test_csv_with_header.csv')
        txt_file_path = pkg_resources.resource_filename(__name__,
                                                        'data/test_csv_with_header.txt')
        self.csv_file = File(csv_file_path)
        self.txt_file = File(txt_file_path)

    def test_get_cls_file(self):
        result_csv_file = get_cls_file(self.csv_file)
        self.assertEqual(result_csv_file.__class__.__name__, 'CsvFile')

        result_txt_file = get_cls_file(self.txt_file)
        self.assertEqual(result_txt_file.__class__.__name__, 'File')