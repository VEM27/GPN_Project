from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('ak_ts_analysis.urls')),  # тут подключаем urls твоего приложения
    path('importer/', include('importer.urls')),  # подключаем urls из приложения
]
