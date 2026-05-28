import time
from django.core.cache import cache
from .services.folder_cleanup import delete_old_folders

CHECK_INTERVAL = 60 * 30  # 30 минут в секундах


class FolderCleanupMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        last_run = cache.get("last_folder_cleanup")

        if not last_run or time.time() - last_run > CHECK_INTERVAL:
            delete_old_folders()
            cache.set("last_folder_cleanup", time.time(), None)

        return self.get_response(request)
