from rest_framework.routers import DefaultRouter
from .views import ExcelUploadView, UniversityViewSet, CourseViewSet, TwoYearUpload, FourYearUpload
from . import views
from django.urls import path, include



router = DefaultRouter()
router.register(r'universities', UniversityViewSet)
router.register(r'courses', CourseViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/upload_excel/', ExcelUploadView.as_view(), name='upload_excel'),
    path('two_year_upload/', views.TwoYearUpload, name='upload1'),
    path('four_year_upload/', views.FourYearUpload, name='upload2'),
    path('add_course', views.add_course, name="add-course"),
    path('', views.login_view, name="login")
]
