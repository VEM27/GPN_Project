from django.urls import path
from .views.web_views import upload_presentation
from django.urls import path
from .views import KT670Detail, ESISDetail, characteristicsDetail, licenceDetail, applicationsDetail, architectureAppDetail


urlpatterns = [
    path('', upload_presentation, name='upload_presentation'),
    path('api/kt670/', KT670Detail.as_view(), name='kt670-detail'),
    path('api/esis/', ESISDetail.as_view(), name='esis-detail'),
    path('api/characteristics/', characteristicsDetail.as_view(), name='characteristics-detail'),
    path('api/licenses/', licenceDetail.as_view(), name='licenses-detail'),
    path('api/applications/', applicationsDetail.as_view(), name='applications-detail'),
    path('api/architecture_app/', architectureAppDetail.as_view(), name='architecture_app-detail'),
]
