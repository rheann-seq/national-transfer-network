from django.db import models

# Create your models here.
class University(models.Model):
    UNIVERSITY_TYPES = [
        ('FOUR_YEAR', 'Four Year University'),
        ('TWO_YEAR', 'Two Year University'),
    ]
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=300, null=True, blank=True, default='UNKNOWN')
    university_type = models.CharField(max_length=10, choices=UNIVERSITY_TYPES)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

class Course(models.Model):
    course_ID = models.AutoField(primary_key=True)
    course_name = models.CharField(max_length=255)
    effective_term = models.CharField(max_length=10)
    credits = models.IntegerField()
    university = models.ForeignKey(University, on_delete=models.CASCADE)
    # four_year_university = models.ForeignKey(University, related_name='university', on_delete=models.CASCADE, blank=True)
    # two_year_university = models.ForeignKey(University, related_name='community_college', on_delete=models.CASCADE, blank=True)
    equivalent_course = models.ManyToManyField('self', blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

class Student(models.Model):
    name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

