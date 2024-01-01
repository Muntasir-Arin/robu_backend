from rest_framework import serializers
from .models import Applicant, DeptChoice

class DeptChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeptChoice
        fields = ('id', 'name')

class ApplicantSerializer(serializers.ModelSerializer):
    interview_date = serializers.DateField(required=False)
    interview_time = serializers.TimeField(required=False)

    class Meta:
        model = Applicant
        fields = ('id', 'student', 'experience', 'interview_date', 'interview_time', 'interviewed')

class ApplicantDetailSerializer(ApplicantSerializer):
    department_choices = DeptChoiceSerializer(many=True, read_only=True)
