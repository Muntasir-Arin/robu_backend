# serializers.py
from rest_framework import serializers
from .models import Applicant, Dept
from accounts.serializers import RobuSerializer

class DeptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dept
        fields = '__all__'

class ApplicantsSerializer(serializers.ModelSerializer):
    user = RobuSerializer()  
    dept_choice = DeptSerializer(many=True)

    class Meta:
        model = Applicant
        fields = '__all__'
