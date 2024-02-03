import os
import sys


class ImportHelper:
    """
    This class is used to import modules from other directories.
    """
    __instance = None
    __initalized: bool = False

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super(ImportHelper, cls).__new__(cls)
            cls.__instance.__initialized = False
        return cls.__instance

    def __init__(self, verbose: bool = False) -> None:
        if self.__initalized:
            return

        self.__initalized = True

        self.verbose: bool = verbose
        self.__crawl_directory_for_init_files()

    def __get_current_directory(self) -> str:
        current_directory = os.path.dirname(os.path.realpath(__file__))

        if self.verbose:
            print('os.path.dirname(os.path.realpath(__file__)): ' + current_directory)

        return current_directory

    def __insert_directory_to_path(self, directory: str) -> None:
        if self.verbose:
            print('insert directory to path: ' + directory)

        full_directory_path = os.path.abspath(os.path.join(self.__get_current_directory(), directory))
        if self.verbose:
            print('full directory: ' + full_directory_path)

        sys.path.insert(0, full_directory_path)

    def __crawl_directory_for_init_files(self) -> None:
        for root, dirs, files in os.walk(self.__get_current_directory()):
            for file in files:
                if file == '__init__.py':
                    if self.verbose:
                        print('found __init__.py in ' + root)

                    self.__insert_directory_to_path(root)
