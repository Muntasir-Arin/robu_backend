# views.py
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import applicants
from .serializers import ApplicantsSerializer

class ApplicantsCreateView(generics.CreateAPIView):
    serializer_class = ApplicantsSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Automatically set the user field from the request's authenticated user
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        # Override create method to customize the response
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class ApplicantsUpdateView(generics.UpdateAPIView):
    queryset = applicants.objects.all()
    serializer_class = ApplicantsSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        # Override update method to customize the response
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

class ApplicantsDeleteView(generics.DestroyAPIView):
    queryset = applicants.objects.all()
    serializer_class = ApplicantsSerializer
    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        # Override destroy method to customize the response
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
