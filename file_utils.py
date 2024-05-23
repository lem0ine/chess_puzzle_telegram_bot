import requests
import os
def download_file(url, local_filename):
    if os.path.exists(local_filename) and os.path.getsize(local_filename) > 0:
        return
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
