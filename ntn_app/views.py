from django.shortcuts import render
from rest_framework import viewsets
from .models import Course, University
from .serializers import CourseSerializer, UniversitySerializer

class UniversityViewSet(viewsets.ModelViewSet):
    queryset =  University.objects.all()
    serializer_class = UniversitySerializer

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer    

