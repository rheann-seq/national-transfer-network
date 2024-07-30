from rest_framework.routers import DefaultRouter
from .views import AgreementDetailAPIView, AgreementListCreateAPIView, AgreementPDFAPIView, ExcelUploadView, UniversityViewSet, CourseViewSet, UploadDataView, TwoYearUpload, FourYearUpload

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
    path('login_institution', views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path('institution_sign_up', views.inst_register_view, name="institution-register"),
    path('', views.entry_page_view, name="entry"),
    path('api/agreements/', AgreementListCreateAPIView.as_view(), name='agreement_list_create_api'),
    path('api/agreements/<int:pk>/', AgreementDetailAPIView.as_view(), name='agreement_detail_api'),
    path('api/agreements/<int:pk>/pdf/', AgreementPDFAPIView.as_view(), name='agreement_pdf_api'),
    # path('agreement/<int:pk>/', views.agreement_detail, name='agreement_detail'),
    # path('agreement/<int:pk>/pdf/', views.agreement_pdf, name='agreement_pdf'),
]
