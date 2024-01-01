from djoser.serializers import UserCreateSerializer
from accounts.models import User
from rest_framework import serializers

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('name', 'date_of_birth', 'student_id', 'secondary_email', 'phone_number', 'avatar', 'rs_status', 'facebook_profile', 'linkedin_link', 'bracu_start' )

class RobuSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'name', 'date_of_birth', 'student_id', 'secondary_email', 'phone_number',
                  'position', 'department', 'avatar', 'rs_status', 'facebook_profile', 'linkedin_link',
                  'robu_start', 'robu_end', 'bracu_start')

class PublicUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'name', 'date_of_birth', 'student_id',
                  'position', 'department', 'avatar', 'rs_status', 'facebook_profile', 'linkedin_link',
                  'robu_start', 'robu_end')



class UserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('id', 'email', 'name', 'password')

class PanelSerializer(serializers.Serializer):
    year = serializers.IntegerField()
    president = serializers.IntegerField()
    vp = serializers.IntegerField()
    ags = serializers.IntegerField()
    gso = serializers.IntegerField()
    gsa = serializers.IntegerField()