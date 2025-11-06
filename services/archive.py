import os
import zipfile
from datetime import date
from config import Config

def archive_files(paths: list[str], label: str) -> str:
   
    os.makedirs(Config.STORAGE_ARCHIVE, exist_ok=True)

    zip_name = f"archive_{label}_{date.today().isoformat()}.zip"
    zip_path = os.path.join(Config.STORAGE_ARCHIVE, zip_name)

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for file_path in paths:
            arcname = os.path.basename(file_path)
            zf.write(file_path, arcname=arcname)

    return zip_path
