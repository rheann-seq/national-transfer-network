from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Course, University
from .serializers import CourseSerializer, UniversitySerializer, ExcelFileSerializer
import pandas as pd

class UniversityViewSet(viewsets.ModelViewSet):
    queryset =  University.objects.all()
    print(str(queryset.query))
    serializer_class = UniversitySerializer

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    print(str(queryset.query))
    serializer_class = CourseSerializer    

def TwoYearUpload(request):
    return render(request,'ntn_app/2year_upload.html')

def FourYearUpload(request):
    return render(request,'ntn_app/4year_upload.html')


def add_course(request):
    return render(request, 'ntn_app/add_course.html')

class ExcelUploadView(APIView):
    print('called the excel upload function')
    parser_classes = (MultiPartParser, FormParser,)

    def post(self, request, *args, **kwargs):
        file_serializer = ExcelFileSerializer(data=request.data)
        if file_serializer.is_valid():
            excel_file = request.FILES['file']
            df = pd.read_excel(excel_file)

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
