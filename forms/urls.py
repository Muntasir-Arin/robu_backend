from django.urls import path
from .views import CreateApplicantView, RetrieveApplicantView, PatchApplicantView

urlpatterns = [
    path('create/', CreateApplicantView.as_view(), name='create_applicant'),
    path('retrieve/', RetrieveApplicantView.as_view(), name='retrieve_applicant'),
    path('patch/<int:pk>/', PatchApplicantView.as_view(), name='patch_applicant'),
]