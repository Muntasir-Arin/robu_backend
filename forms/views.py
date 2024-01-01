from rest_framework import generics
from rest_framework.response import Response
from .models import Applicant, CreatedModel, DeptChoice
from .serializers import ApplicantSerializer, ApplicantDetailSerializer, DeptChoiceSerializer

class CreateApplicantView(generics.CreateAPIView):
    serializer_class = ApplicantSerializer

    def perform_create(self, serializer):
        table_name = self.request.data.get('name')
        Applicant._meta.db_table = table_name
        applicant_instance = serializer.save()

        CreatedModel.objects.create(name=table_name)

        dept_table_name = f"dept_{CreatedModel.objects.get(name=applicant_instance._meta.db_table).created_at.year}"
        DeptChoice._meta.db_table = dept_table_name
        DeptChoice.objects.create(name=dept_table_name)

class RetrieveApplicantView(generics.RetrieveAPIView):
    queryset = Applicant.objects.all()
    serializer_class = ApplicantDetailSerializer

    def get(self, request, *args, **kwargs):
        table_name = self.request.data.get('table_name')
        Applicant._meta.db_table = table_name
        return self.retrieve(request, *args, **kwargs)

class PatchApplicantView(generics.UpdateAPIView):
    queryset = Applicant.objects.all()
    serializer_class = ApplicantSerializer
