from django.db import models

# Create your models here.
class University(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=300, null=True, blank=True, default='UNKNOWN')

class Course(models.Model):
    course_ID = models.AutoField(primary_key=True)
    course_name = models.CharField(max_length=255)
    effective_term = models.CharField(max_length=10)
    credits = models.IntegerField()
    four_year_university = models.ForeignKey(University, related_name='university', on_delete=models.CASCADE, blank=True)
    two_year_university = models.ForeignKey(University, related_name='community_college', on_delete=models.CASCADE, blank=True)
    equivalent_course = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)