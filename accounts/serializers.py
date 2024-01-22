from djoser.serializers import UserCreateSerializer
from accounts.models import User
from rest_framework import serializers
from django.core.signing import TimestampSigner
from django.conf import settings
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('name', 'is_verified', 'date_of_birth', 'insta_link', 'position', 'robu_department','is_admin', 'student_id', 'secondary_email', 'phone_number', 'avatar', 'rs_status', 'facebook_profile', 'linkedin_link', 'bracu_start' , 'blood_group', 'gender', 'org')
        read_only_fields = ('robu_department','is_admin','position', 'is_verified')
        
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

    # def create(self, validated_data):
    #     user = super().create(validated_data)
    #     user.is_verified = False
    #     user.save()
    #     self.send_verification_email(user)
    #     return user

    def send_verification_email(self, user):
        signer = TimestampSigner()
        user_id = urlsafe_base64_encode(force_bytes(user.id))
        token = signer.sign(user_id)
        token = token.decode('utf-8')
        user.verification_token = token
        user.save()

        subject = 'Verify your email'
        message = render_to_string('email/verification_email.txt', {'user': user, 'token': token})
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [user.email]
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)


class PanelSerializer(serializers.Serializer):
    year = serializers.IntegerField()
    president = serializers.IntegerField()
    vp = serializers.IntegerField()
    ags = serializers.IntegerField()
    gso = serializers.IntegerField()
    gsa = serializers.IntegerField()