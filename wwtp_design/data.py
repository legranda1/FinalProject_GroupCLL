from fun import *
import os


class InputReader:
    def __init__(self, xlsx_file_name="input_data.xlsx"):
        """
        For initializing an InputReader object with the given
        attributes and methods
        :param xlsx_file_name: STR of the corresponding .xlsx file name
        :return: None
        """
        self.wwtp_params = pd.DataFrame()
        self.get_input_data(xlsx_file_name)

    def get_input_data(self, xlsx_file_name):
        """
        Reads input data from an Excel file and store it in the
        wwtp_params DataFrame
        :param xlsx_file_name: STR of the corresponding .xlsx file name
        :return: None if there is no error and -1 (INT) if
        there is an error
        """
        try:
            file_path = os.path.join("..", xlsx_file_name)
            self.wwtp_params = pd.read_excel(file_path,
                                             skiprows=[0],
                                             index_col=0,
                                             header=[0])
        except FileNotFoundError:
            return -1
