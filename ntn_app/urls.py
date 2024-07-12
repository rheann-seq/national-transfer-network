from rest_framework.routers import DefaultRouter
from .views import ExcelUploadView, UniversityViewSet, CourseViewSet, ViewDataUpload
from . import views
from django.urls import path, include



router = DefaultRouter()
router.register(r'universities', UniversityViewSet)
router.register(r'courses', CourseViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/upload_excel/', ExcelUploadView.as_view(), name='upload_excel'),
    path('upload_data/', views.ViewDataUpload, name='upload'),
    path('add_course', views.add_course, name="add-course"),
    path('universities', views.universities, name="universities")
]
