import os
import csv

from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2 import service_account
from googleapiclient.errors import HttpError


class GoogleCloudInterface:
    def __init__(self, credentials_file):
        self.credentials_file = credentials_file
        self.drive_service = self._build_drive_service()

    def _build_drive_service(self):
        credentials = service_account.Credentials.from_service_account_file(
            self.credentials_file, scopes=[
                'https://www.googleapis.com/auth/drive']
        )
        return build('drive', 'v3', credentials=credentials)

    def create_folder(self, folder_name, parent_folder_id=None):
        folder_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder'
        }
        if parent_folder_id:
            folder_metadata['parents'] = [parent_folder_id]

        try:
            folder = self.drive_service.files().create(
                body=folder_metadata,
                fields='id'
            ).execute()
            folder_id = folder.get('id')
            print(f'Folder created successfully. Folder ID: {folder_id}')
            return folder_id
        except HttpError as e:
            print(f'An error occurred while creating the folder: {e}')
            return None

    def upload_file(self, file_path, file_name, folder_id):
        media = MediaFileUpload(file_path, mimetype='text/csv', resumable=True)

        file_metadata = {
            'name': file_name,
            'parents': [folder_id]
        }

        try:
            file = self.drive_service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id'
            ).execute()
            file_id = file.get('id')
            print(f'File uploaded successfully. File ID: {file_id}')
            return file_id
        except HttpError as e:
            print(f'An error occurred while uploading the file: {e}')
            return None

    def list_files(self):
        try:
            results = self.drive_service.files().list(
                pageSize=10,
                fields="nextPageToken, files(id, name, mimeType)"
            ).execute()
            items = results.get('files', [])

            if not items:
                print('No files found.')
            else:
                print('Files:')
                for item in items:
                    print(
                        f'{item["name"]} ({item["id"]}) - {item["mimeType"]}')
        except Exception as e:
            print(f'An error occurred while listing the files: {e}')

    def get_file_contents(self, file_name):
        try:
            results = self.drive_service.files().list(
                q=f"name='{file_name}'",
                fields="files(id)",
                pageSize=1
            ).execute()
            items = results.get('files', [])

            if not items:
                print(f'File not found: {file_name}')
            else:
                file_id = items[0]['id']
                response = self.drive_service.files().get_media(fileId=file_id).execute()
                return response.decode('utf-8')
        except Exception as e:
            print(f'An error occurred while printing file contents: {e}')
        return None

    def print_file_contents(self, file_name):
        print(self.get_file_contents(file_name))


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


class CSVParser:
    def __init__(self, file_path):
        self.file_path = file_path
        self.buffer = []

    def parse_csv(self):
        try:
            with open(self.file_path, 'r') as csv_file:
                csv_reader = csv.reader(csv_file)
                for row in csv_reader:
                    parsed_row = []
                    for value in row:
                        try:
                            parsed_row.append(int(value.strip(',')))
                        except ValueError:
                            pass  # Skip non-numeric values
                    if len(parsed_row) >= 1:
                        # Append first number found only
                        self.buffer.append(parsed_row[0])
        except FileNotFoundError:
            print(f'CSV file not found: {self.file_path}')
        except Exception as e:
            print(f'An error occurred while parsing the CSV file: {e}')


class Grapher:
    def __init__(self, buffer):
        self.buffer = buffer

    def draw_graph(self):
        min_value = min(self.buffer)
        for value in self.buffer:
            hyphens = '-' * int(value - min_value + 1)
            print(hyphens)


class PeakDetector:
    def __init__(self, series):
        self.series = series
        # print(series)

    def apply_moving_average(self, window_size=3):
        smoothed_series = []
        for i in range(len(self.series)):
            window_start = max(0, i - window_size + 1)
            window_end = i + 1
            window_values = [
                item for item in self.series[window_start:window_end]]
            window_average = sum(window_values) / len(window_values)
            smoothed_series.append(window_average)
        return smoothed_series

    def find_peaks(self):
        peaks = []
        for i in range(1, len(self.series) - 1):
            if self.series[i] > self.series[i - 1] and \
                    self.series[i] > self.series[i + 1]:
                peaks.append(self.series[i])
        return peaks

    def find_troughs(self):
        troughs = []
        for i in range(1, len(self.series) - 1):
            if self.series[i] < self.series[i - 1] and \
                    self.series[i] < self.series[i + 1]:
                troughs.append(self.series[i])
        return troughs


if __name__ == "__main__":

    credentials_file = os.path.join(os.getcwd(), "creds.json")
    print(credentials_file)
    uploaded_fn = 'uploaded_file.csv'
    csv_file = os.path.join(os.getcwd(), uploaded_fn)
    destination_folder_name = 'MyUploads'

    gci = GoogleCloudInterface(credentials_file)
    folder_id = gci.create_folder(destination_folder_name)
    file_id = gci.upload_file(csv_file, uploaded_fn, folder_id)

    downloaded_fn = "downloaded_file.csv"
    IOHandler.write_file_contents(
        downloaded_fn, gci.get_file_contents(uploaded_fn))

    parser = CSVParser(downloaded_fn)
    parser.parse_csv()

    # print(parser.buffer)
    grapher = Grapher(parser.buffer)
    grapher.draw_graph()

    peak_detector = PeakDetector(parser.buffer)
    smoothed_numbers = peak_detector.apply_moving_average(window_size=3)
    peak_values = peak_detector.find_peaks()
    trough_values = peak_detector.find_troughs()

    print("Smoothed Numbers:", smoothed_numbers)
    print("Peaks:", peak_values)
    print("Troughs:", trough_values)

    sgrapher = Grapher(smoothed_numbers)
    sgrapher.draw_graph()
