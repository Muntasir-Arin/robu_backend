# serializers.py
from rest_framework import serializers
from .models import Applicant, IntraEventFormSubmission
from accounts.serializers import RobuSerializer, UserNameSerializer


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



class IntraEventFormSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = IntraEventFormSubmission
        exclude = ['user', 'approved_by']
        read_only_fields = ['payment_status']

class IntraEventFormSerializer(serializers.ModelSerializer):
    user = UserNameSerializer()  
    class Meta:
        model = IntraEventFormSubmission
        fields = '__all__'