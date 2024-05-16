# file_utils.py

import requests

def download_file(url, local_filename):
    # Стриминг запроса, чтобы избежать загрузки всего файла в память
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    print(f"Файл {local_filename} был загружен.")

