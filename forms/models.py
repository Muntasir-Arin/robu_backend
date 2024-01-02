from django.db import models
from accounts.models import User

class applicants(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    about = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=100, blank=False, default='not selected')
    applicantion_date = models.DateField(auto_now_add=True)
    interviewed = models.BooleanField(default=False) 
    applicantion_date = models.DateField(auto_now_add=True)
    dept_choice = models.ManyToManyField('Dept', blank=True) 
    drive_link = models.CharField(max_length=200)


class Dept(models.Model):
    choice = models.TextField(null=True, blank=True)
    rank = models.IntegerField(blank=False)
    project = models.ForeignKey(applicants, on_delete=models.CASCADE, null=True, related_name='applicants')

