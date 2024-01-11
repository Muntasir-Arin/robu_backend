from djoser.serializers import UserCreateSerializer
from accounts.models import User
from rest_framework import serializers


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('name', 'date_of_birth', 'insta_link', 'robu_department', 'student_id', 'secondary_email', 'phone_number', 'avatar', 'rs_status', 'facebook_profile', 'linkedin_link', 'bracu_start' , 'blood_group', 'gender', 'org')
        read_only_fields = ('robu_department',)
        
class RobuSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class PublicUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'name', 'date_of_birth', 'student_id',
                  'position', 'department', 'avatar', 'rs_status', 'facebook_profile', 'linkedin_link',
                  'robu_start', 'robu_end', 'blood_group', 'gender',  'org')



class UserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('id', 'email', 'name', 'org', 'password')

class PanelSerializer(serializers.Serializer):
    year = serializers.IntegerField()
    president = serializers.IntegerField()
    vp = serializers.IntegerField()
    ags = serializers.IntegerField()
    gso = serializers.IntegerField()
    gsa = serializers.IntegerField()