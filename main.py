import os
import csv

from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2 import service_account
from googleapiclient.errors import HttpError


class GoogleDriveUploader:
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

    def write_file_contents(self, file_contents, filename):
        try:
            with open(filename, 'w') as file:
                file.write(file_contents)
            print(f'Successfully wrote file contents to {filename}')
        except Exception as e:
            print(f'An error occurred while writing file contents: {e}')


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
                    self.buffer.append(parsed_row)
        except FileNotFoundError:
            print(f'CSV file not found: {self.file_path}')
        except Exception as e:
            print(f'An error occurred while parsing the CSV file: {e}')


class Grapher:
    def __init__(self, buffer):
        self.buffer = buffer

    def draw_graph(self):
        if not self.buffer:
            print('No data in the buffer. Please parse a CSV file first.')
            return

        flattened_buffer = [value for row in self.buffer for value in row]
        if not flattened_buffer:
            print('No values in the buffer. Unable to draw the graph.')
            return

        min_value = min(flattened_buffer)

        print('Graph:')
        for row in self.buffer:
            graph_row = ''.join(['-' * (value - min_value + 1) for value in row])
            print(graph_row)


if __name__ == "__main__":

    credentials_file = os.path.join(os.getcwd(), "creds.json")
    print(credentials_file)
    uploaded_fn = 'uploaded_file.csv'
    csv_file = os.path.join(os.getcwd(), uploaded_fn)
    destination_folder_name = 'MyUploads'

    uploader = GoogleDriveUploader(credentials_file)
    folder_id = uploader.create_folder(destination_folder_name)
    file_id = uploader.upload_file(csv_file, uploaded_fn, folder_id)
    downloaded_fn = "downloaded_file.csv"
    uploader.write_file_contents(
        uploader.get_file_contents(uploaded_fn), downloaded_fn)

    parser = CSVParser(downloaded_fn)
    parser.parse_csv()

    grapher = Grapher(parser.buffer)
    grapher.draw_graph()
