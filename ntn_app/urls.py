from rest_framework.routers import DefaultRouter
from .views import UniversityViewSet, CourseViewSet
from django.urls import path, include


router = DefaultRouter()
router.register(r'universities', UniversityViewSet)
router.register(r'courses', CourseViewSet)

urlpatterns = [
    path('', include(router.urls))
]
