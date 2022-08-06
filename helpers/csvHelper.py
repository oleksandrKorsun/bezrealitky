import csv
import itertools
import os


class CsvHelper:
    read_mode = "r"
    append_mode = "a+"

    def __init__(self, filename):
        self.filename = filename

    def get_path_to_the_file(self):
        orig_path = os.getcwd()
        edit_orig_path = str(orig_path.split('test')[0])
        final = os.path.join(edit_orig_path, self.filename)
        return final

    def open_csv_as_list(self):
        with open(self.get_path_to_the_file(), self.read_mode, encoding='utf-8-sig') as f:
            reader = csv.reader(f)
            your_list = list(reader)
            final = list(itertools.chain(*your_list))
        return final

    def check_if_element_in_csv(self, item_for_check):
        csv_list = self.open_csv_as_list()
        if item_for_check in csv_list:
            return True
        else:
            return False

    def write_to_csv(self, text):
        with open(self.get_path_to_the_file(), self.append_mode, encoding='utf-8-sig') as f:
            f.write(text)
            f.close()