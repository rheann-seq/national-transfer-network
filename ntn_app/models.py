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
    university = models.ForeignKey(University, on_delete=models.CASCADE)
    equivalent_course = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)