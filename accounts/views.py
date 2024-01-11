from rest_framework import generics, permissions
from .models import User
from .serializers import PublicUserSerializer, RobuSerializer, UserProfileSerializer, PanelSerializer
from django.db.models import F
from django.db.models.functions import ExtractYear
from django.utils import timezone
from rest_framework.response import Response


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

class RobuUpdateView(generics.ListCreateAPIView, generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = RobuSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrPresident]

    def get_object(self):
        obj = self.get_queryset().get(id=self.kwargs["pk"])
        self.check_object_permissions(self.request, obj)
        return obj

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