from django.urls import path
from .views import ApplicantsCreateView, ApplicantsUpdateView, ApplicantsDeleteView, ApplicantsInfoView, InterviewUpdateView

urlpatterns = [
    path('applicants/', ApplicantsCreateView.as_view(), name='create-applicant'),
    path('applicants/info/', ApplicantsInfoView.as_view(), name='applicants-info'),
    path('applicants/<str:custom_id>/', ApplicantsUpdateView.as_view(), name='view/update-applicant'),
    path('applicants/<str:custom_id>/delete/', ApplicantsDeleteView.as_view(), name='delete-applicant'),
    path('applicants/<str:custom_id>/interview/', InterviewUpdateView.as_view(), name='update-interview'), #/api/applicants/22101525_spring20699/interview/
]
