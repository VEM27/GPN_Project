import os
import shutil
from datetime import timedelta
from django.conf import settings
from django.utils import timezone
from datetime import datetime, timezone as dt_timezone


def delete_old_folders():
    base_path = settings.PPTX_OUTPUTS_PATH  # Папка, где создаются временные папки
    now = timezone.now()

    for folder in os.listdir(base_path):
        folder_path = os.path.join(base_path, folder)

        if not os.path.isdir(folder_path):
            continue

        # Время создания папки (Windows: реально время создания)
        created_timestamp = os.path.getctime(folder_path)
        created_time = datetime.fromtimestamp(
            created_timestamp, tz=dt_timezone.utc
        )

        # Если папка старше 2 часов — удаляем
        if now - created_time > timedelta(hours=2):
            try:
                shutil.rmtree(folder_path)
                print(f"Удалена папка: {folder_path}")
            except Exception as e:
                print(f"Ошибка при удалении {folder_path}: {e}")
