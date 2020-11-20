from easy_file.file import file_cls_list


def get_cls_file(file):
    extension = file.extension

    for file_cls in file_cls_list:
        ext_list = file_cls.extension
        if extension in ext_list:
            return file_cls(file.path)

    return file
