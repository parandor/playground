import numpy as np

class IOHandler:
    @staticmethod
    def write_file_contents(filename, contents):
        try:
            with open(filename, 'w') as file:
                file.write(contents)
        except IOError as e:
            print(f"An error occurred while writing to the file: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    @staticmethod
    def write_numpy(filename, array):
        try:
            with open(filename, 'w') as file:
                np.savetxt(file, array, fmt='%d')
        except IOError as e:
            print(f"An error occurred while writing to the file: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")