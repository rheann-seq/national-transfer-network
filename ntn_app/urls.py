from rest_framework.routers import DefaultRouter
from .views import ExcelUploadView, UniversityViewSet, CourseViewSet, UploadDataView, TwoYearUpload, FourYearUpload

from . import views
from django.urls import path, include



router = DefaultRouter()
router.register(r'universities', UniversityViewSet)
router.register(r'courses', CourseViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/upload_excel/', ExcelUploadView.as_view(), name='upload_excel'),
     path('upload-data/', UploadDataView.as_view(), name='upload_data'),
    path('two_year_upload/', views.TwoYearUpload, name='upload-two-years'),
    path('four_year_upload/', views.FourYearUpload, name='upload-four-years'),
    path('add_course', views.add_course, name="add-course"),
    path('', views.login_view, name="login"),
    path('institution_register', views.inst_register_view, name="institution-register"),
    path('entry_page', views.entry_page_view, name="entry")
]
