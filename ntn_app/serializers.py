from rest_framework import serializers
from .models import Course, University

class UniversitySerializer(serializers.ModelSerializer):
    university_type = serializers.ChoiceField(choices=University.UNIVERSITY_TYPES)
    class Meta:
        model = University
        fields = '__all__'

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'       

class ExcelFileSerializer(serializers.Serializer):
    file = serializers.FileField()         