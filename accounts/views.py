from django.conf import settings
from rest_framework import generics, permissions
from .models import User
from .serializers import PublicUserSerializer, RobuSerializer, UserProfileSerializer, PanelSerializer
from django.db.models import F
from django.db.models.functions import ExtractYear
from django.utils import timezone
from rest_framework.response import Response
from django.core.signing import TimestampSigner, BadSignature
from django.utils.http import urlsafe_base64_decode
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework import status
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj == request.user

class IsAdminOrPresident(permissions.BasePermission):
    def has_permission(self, request, view):
        # Check if the user is an admin or president
        return request.user.is_admin_or_president
    
class IsAdminOrInterviewer(permissions.BasePermission):
    def has_permission(self, request, view):
        # Check if the user is an admin or president
        return request.user.is_admin_or_panel or request.user.is_admin_or_dads

class UserProfileUpdateView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    def get_object(self):
        return self.request.user


class PublicUserProfileView(generics.RetrieveAPIView):
    serializer_class = PublicUserSerializer
    lookup_field = 'student_id'

    def get_queryset(self):
        # Filter profiles where position is not null
        return User.objects.exclude(position='Not a Member')


class MemberListView(generics.ListAPIView):
    serializer_class = PublicUserSerializer

    def get_queryset(self):
        filter = self.request.query_params.get('filter', 'members')
        if filter == 'members':
            return User.objects.exclude(position='Not a Member')
        elif filter == 'current':
            return User.objects.filter(robu_end__isnull=True).exclude(position='Not a Member')
        elif filter == 'alumni':
            return User.objects.filter(robu_end__isnull=False).exclude(position='Not a Member')
        elif filter == 'all':
            return User.objects
        else:
            return User.objects.none()  # Invalid filter, return an empty queryset
        

class PrivateUserProfileView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated, IsAdminOrInterviewer]
    queryset = User.objects.all()
    serializer_class = PublicUserSerializer
    lookup_field = 'id'

class RobuRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = RobuSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrPresident]

    def get_object(self):
        obj = self.get_queryset().get(id=self.kwargs["id"])
        self.check_object_permissions(self.request, obj)
        return obj

class RobuListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = RobuSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrPresident]

class PanelListAPIView(generics.ListAPIView):
    serializer_class = PanelSerializer
    def get_queryset(self):
        current_year = timezone.now().year
        positions = ['president', 'vp', 'ags', 'gso', 'gsa']
        queryset = User.objects.filter(_in=positions)
        queryset = (
            queryset
            .values(year=ExtractYear('robu_end'), position='position', user_id=F('student_id'))
        )
        current_year_result = (
            User.objects
            .filter(_in=positions, robu_end__isnull=True)
            .values(year=current_year, position='position', user_id=F('student_id'))
        )
        result = list(queryset) + list(current_year_result)
        return result
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    

class CurrentPanelListAPIView(generics.ListAPIView):
    serializer_class = PanelSerializer
    def get_queryset(self):
        current_year = timezone.now().year
        positions = ['president', 'vp', 'ags', 'gso', 'gsa']
        current_year_result = (
            User.objects
            .filter(_in=positions, robu_end__isnull=True)
            .values(year=current_year, position='position', user_id=F('student_id'))
        )
        result = list(current_year_result)
        return result
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    

#-----------------------------------------------------------------------------
class VerifyEmailView(APIView):
    def get(self, request, user_id, token):
        user = get_object_or_404(User, id=user_id)

        # Check if the token is valid
        if self.validate_verification_token(user, token):
            user.is_verified = True
            user.save()
            return Response({'detail': 'Email verified successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Invalid verification link'}, status=status.HTTP_400_BAD_REQUEST)

    def validate_verification_token(self, user, token):
        try:
            signer = TimestampSigner()
            user_id = signer.unsign(token, max_age=settings.VERIFICATION_TOKEN_EXPIRATION)
            user_id = force_str(urlsafe_base64_decode(user_id))
            return str(user_id) == str(user.id)
        except BadSignature:
            return False
        
class ResendVerificationEmailView(APIView):
    def get(self, request):
        user = request.user

        if not user.is_authenticated:
            return Response({'detail': 'User not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)

        if user.is_verified:
            return Response({'detail': 'User is already verified'}, status=status.HTTP_400_BAD_REQUEST)

        self.send_verification_email(user)
        return Response({'detail': 'Verification email sent successfully'}, status=status.HTTP_200_OK)

    def send_verification_email(self, user):
        signer = TimestampSigner()
        user_id = urlsafe_base64_encode(force_bytes(user.id))
        token = signer.sign(user_id)
        user.verification_token = token
        user.save()
        subject = 'Verify your email'
        message = render_to_string('email/verification_email.html', {'user': user, 'token': token})
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [user.email]
        send_mail(subject, message, from_email, recipient_list, html_message=message, fail_silently=False)
