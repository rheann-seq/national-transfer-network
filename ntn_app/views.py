from django.shortcuts import render, redirect
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from django.template.loader import render_to_string
from django.http import HttpResponse
from weasyprint import HTML
from .models import ArticulationAgreement

from ntn_app.forms import LoginForm, RegistrationForm
from .models import Course, Profile, University
from .serializers import CourseSerializer, UniversitySerializer, ExcelFileSerializer, UploadDataSerializer, ArticulationAgreementSerializer
import pandas as pd

def entry_page_view(request):
    return render(request, 'ntn_app/entry_page.html')
class UniversityViewSet(viewsets.ModelViewSet):
    queryset =  University.objects.all()
    print(str(queryset.query))
    serializer_class = UniversitySerializer

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    print(str(queryset.query))
    serializer_class = CourseSerializer    

@login_required
def TwoYearUpload(request):
    return render(request,'ntn_app/2year_upload.html')

def FourYearUpload(request):
    return render(request,'ntn_app/4year_upload.html')


def add_course(request):
    return render(request, 'ntn_app/add_course.html')

def     logout_view(request):
    logout(request)
    return redirect(reverse('login'))


def inst_register_view(request):
    context = {}

    if request.method == "GET":
        context['form'] =  RegistrationForm()
        return render(request, 'ntn_app/register.html', context)

    # Creates a bound form from the request POST parameters and makes the 
    # form available in the request context dictionary.
    form = RegistrationForm(request.POST)
    context['form'] = form

    # Validates the form.
    if not form.is_valid():
        return render(request, 'ntn_app/register.html', context)


    # # At this point, the form data is valid.  Register and login the user.
    new_user = User.objects.create_user(
        username=form.cleaned_data['email'],
        password=form.cleaned_data['password1'],
        email=form.cleaned_data['email'],
        first_name=form.cleaned_data['name_of_contact_person']
    )
    new_user.save()

    new_profile = Profile(
        user = new_user,
        name_of_institution = form.cleaned_data['name_of_institution'],
        state = form.cleaned_data['state'],
        website = form.cleaned_data['website'],
        title = form.cleaned_data['title'],
        phone = form.cleaned_data['phone'],
    )

    new_profile.save()

    new_user = authenticate(username=form.cleaned_data['email'],
                            password=form.cleaned_data['password1'])

    login(request, new_user)
    
    return redirect(reverse('upload-two-years'))

def login_view(request):
    context = {}

    # Just display the registration form if this is a GET request.
    if request.method == 'GET':
        context['form'] = LoginForm()
        return render(request, 'ntn_app/login.html', context)

    # Creates a bound form from the request POST parameters and makes the 
    # form available in the request context dictionary.
    form = LoginForm(request.POST)
    context['form'] = form

    # Validates the form.
    if not form.is_valid():
        context['message'] = 'wrong username or password'
        return render(request, 'ntn_app/login.html', context)

    new_user = authenticate(username=form.cleaned_data['username'],
                            password=form.cleaned_data['password'])

    login(request, new_user)
    return redirect(reverse('upload-two-years'))


class ExcelUploadView(APIView):
    print('called the excel upload function')
    parser_classes = (MultiPartParser, FormParser,)

    def post(self, request, *args, **kwargs):
        file_serializer = ExcelFileSerializer(data=request.data)
        if file_serializer.is_valid():
            excel_file = request.FILES['file']
            df = pd.read_excel(excel_file)

            required_columns = [
                '2yearCollegeName', '2yearCollegeLocation', 'EffectiveTerm',
                'CC_Subject', 'Uni_Subject', 'Credits', '4yearCollegeName', '4yearCollegeLocation'
            ]

            # Check if all required columns are present
            if not all(column in df.columns for column in required_columns):
                missing_columns = [column for column in required_columns if column not in df.columns]
                return Response({"error": f"Missing columns: {', '.join(missing_columns)}"}, status=400)

            # Check if there is no data or all rows are empty
            if df[required_columns].dropna(how='all').empty:
                return Response({"error": "Please add some data before uploading."}, status=400)

            for index, row in df.iterrows():
                four_year_university, _ = University.objects.get_or_create(
                    name=row['4yearCollegeName'],
                    location=row['4yearCollegeLocation'],
                    defaults={'university_type': 'FOUR_YEAR'}
                )
                two_year_university, _ = University.objects.get_or_create(
                    name=row['2yearCollegeName'],
                    location=row['2yearCollegeLocation'],
                    defaults={'university_type': 'TWO_YEAR'}
                )
                #2 year course
                two_year_course = Course.objects.create(
                    course_name=row['CC_Subject'],
                    effective_term=row['EffectiveTerm'],
                    credits=row['Credits'],
                    university=four_year_university,
                )

                #4year course
                four_year_course = Course.objects.create(
                    course_name=row['CC_Subject'],
                    effective_term=row['EffectiveTerm'],
                    credits=row['Credits'],
                    university=two_year_university,
                    equivalent_course=two_year_course
                )

                # Update the 2-year course to link back to the 4-year course
                two_year_course.equivalent_course = four_year_course
                two_year_course.save()
            return Response({"message": "Data imported successfully"}, status=201)
        else:
            return Response(file_serializer.errors, status=400)

class UploadDataView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UploadDataSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data

            twoYearInstitutionName = data['twoYearInstitutionName']
            twoYearInstitutionLocation = data['twoYearInstitutionLocation']
            effective_term = data['effectiveTerm']
            cc_subject = data['ccSubject']
            uni_subject = data['uniSubject']
            credits = data['credits']
            fourYearInstitutionName = data['fourYearInstitutionName']
            fourYearInstitutionLocation = data['fourYearInstitutionLocation']

            try:
                four_year_university, _ = University.objects.get_or_create(
                    name=fourYearInstitutionName,
                    location=fourYearInstitutionLocation,
                    university_type='FOUR_YEAR'
                )
                two_year_university, _ = University.objects.get_or_create(
                    name=twoYearInstitutionName,
                    location=twoYearInstitutionLocation,
                    university_type='TWO_YEAR'
                )

                # 2-year course
                two_year_course = Course.objects.create(
                    course_name=cc_subject,
                    effective_term=effective_term,
                    credits=credits,
                    university=two_year_university,
                )

                # 4-year course
                four_year_course = Course.objects.create(
                    course_name=uni_subject,
                    effective_term=effective_term,
                    credits=credits,
                    university=four_year_university,
                    equivalent_course=two_year_course
                )

                # Update the 2-year course to link back to the 4-year course
                two_year_course.equivalent_course = four_year_course
                two_year_course.save()

                return Response({"message1": "Data uploaded successfully!"}, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from django.shortcuts import render, get_object_or_404, redirect
from .models import ArticulationAgreement

# def agreement_detail(request, pk):
#     agreement = get_object_or_404(ArticulationAgreement, pk=pk)
#     if request.method == 'POST':
#         agreement.home_institution_name = request.POST.get('home_institution_name')
#         agreement.partner_institution_name = request.POST.get('partner_institution_name')
#         agreement.program_from_institution_one = request.POST.get('program_from_institution_one')
#         agreement.program_at_institution_two = request.POST.get('program_at_institution_two')
#         agreement.associate_degree_program = request.POST.get('associate_degree_program')
#         agreement.institution_offering_associate_degree = request.POST.get('institution_offering_associate_degree')
#         agreement.bachelor_degree_program = request.POST.get('bachelor_degree_program')
#         agreement.institution_offering_bachelor_degree = request.POST.get('institution_offering_bachelor_degree')
#         agreement.degree_program = request.POST.get('degree_program')
#         agreement.field_of_study = request.POST.get('field_of_study')
#         agreement.credit_hours = request.POST.get('credit_hours')
#         agreement.university_name = request.POST.get('university_name')
#         agreement.gpa_requirement = request.POST.get('gpa_requirement')
#         agreement.final_degree_program = request.POST.get('final_degree_program')
#         agreement.final_institution = request.POST.get('final_institution')
#         agreement.save()
#         return redirect('agreement_detail', pk=agreement.pk)
#     return render(request, 'agreement_detail.html', {'agreement': agreement})

# def agreement_pdf(request, pk):
#     agreement = ArticulationAgreement.objects.get(pk=pk)
#     html_string = render_to_string('agreement_detail.html', {'agreement': agreement})
#     html = HTML(string=html_string)
#     pdf = html.write_pdf()

#     response = HttpResponse(pdf, content_type='application/pdf')
#     response['Content-Disposition'] = f'attachment; filename="agreement_{pk}.pdf"'
#     return response

class AgreementListCreateAPIView(APIView):
    def get(self, request, format=None):
        agreements = ArticulationAgreement.objects.all()
        serializer = ArticulationAgreementSerializer(agreements, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ArticulationAgreementSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AgreementDetailAPIView(APIView):
    def get(self, request, pk, format=None):
        agreement = get_object_or_404(ArticulationAgreement, pk=pk)
        serializer = ArticulationAgreementSerializer(agreement)
        return Response(serializer.data)

    def patch(self, request, pk, format=None):
        agreement = get_object_or_404(ArticulationAgreement, pk=pk)
        serializer = ArticulationAgreementSerializer(agreement, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AgreementPDFAPIView(APIView):
    def get(self, request, pk, format=None):
        agreement = get_object_or_404(ArticulationAgreement, pk=pk)
        html_string = render_to_string('ntn_app/agreement_detail.html', {'agreement': agreement})
        html = HTML(string=html_string)
        pdf = html.write_pdf()

        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="agreement_{pk}.pdf"'
        return response
