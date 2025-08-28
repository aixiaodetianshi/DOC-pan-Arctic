# Python 脚本（批量下载 Earth Engine 导出的 CSV 文件）  # English: script


import os
import io
import pickle
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

LOCAL_FOLDER = r"D:\UZH\2025\NPP\pan_Arctic_temperature_2m\batch"
DRIVE_FOLDER_NAME = "Arctic_catchment_temperature_2m"
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

def authenticate_drive():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('client_secret_223769127144-a3ifpmrd57jqq9rk0do29sd7a01ib54p.apps.googleusercontent.com.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return build('drive', 'v3', credentials=creds)

def get_drive_folder_id(service, folder_name):
    results = service.files().list(
        q=f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder'",
        spaces='drive',
        fields="files(id, name)"
    ).execute()
    items = results.get('files', [])
    if not items:
        raise Exception(f"Folder '{folder_name}' not found.")
    if len(items) > 1:
        print(f"警告：找到多个同名文件夹，默认使用第一个：{items[0]['id']}")
    return items[0]['id']

def download_files(service, folder_id, local_path):
    os.makedirs(local_path, exist_ok=True)
    page_token = None

    while True:
        response = service.files().list(
            q=f"'{folder_id}' in parents and mimeType='text/csv'",
            spaces='drive',
            fields='nextPageToken, files(id, name)',
            pageToken=page_token
        ).execute()

        for file in response.get('files', []):
            file_id = file['id']
            file_name = file['name']
            local_file = os.path.join(local_path, file_name)

            if os.path.exists(local_file):
                print(f"{file_name} 已存在，跳过。")
                continue

            print(f"正在下载：{file_name}")
            request = service.files().get_media(fileId=file_id)
            with io.FileIO(local_file, 'wb') as fh:
                downloader = MediaIoBaseDownload(fh, request)
                done = False
                while not done:
                    status, done = downloader.next_chunk()
                    if status:
                        print(f"  进度：{int(status.progress() * 100)}%")

        page_token = response.get('nextPageToken', None)
        if not page_token:
            break

if __name__ == '__main__':
    print("连接 Google Drive ...")
    service = authenticate_drive()
    print("查找目标文件夹 ...")
    folder_id = get_drive_folder_id(service, DRIVE_FOLDER_NAME)
    print("开始下载 CSV 文件 ...")
    download_files(service, folder_id, LOCAL_FOLDER)
    print("✅ 所有文件下载完成。")
