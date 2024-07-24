from django.db import models
from django.contrib.auth.models import User

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
    # equivalent_course = models.ManyToManyField('self', blank=True)
    equivalent_course = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name_of_institution = models.CharField(max_length=255, blank=False)
    state = models.CharField(max_length=100, blank=False)
    website = models.URLField(max_length=200, blank=False)
    title = models.CharField(max_length=100, blank=False)
    phone = models.CharField(max_length=20, blank=False)

    def __str__(self):
        return self.user.username

