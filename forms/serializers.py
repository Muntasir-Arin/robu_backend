# serializers.py
from rest_framework import serializers
from .models import Applicant
from accounts.serializers import RobuSerializer


class InterviewSerializer(serializers.ModelSerializer):
    user = RobuSerializer()  

    class Meta:
        model = Applicant
        fields = '__all__'

class ApplicantsSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Applicant
        exclude = ['status', 'interviewed', 'application_date', 'interview_time', 'assigned_department', 'feedback']
