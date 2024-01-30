from django.urls import path
from .views import AllSubmissionsView, ApplicantsCreateView, ApplicantsUpdateView, ApplicantsDeleteView, ApplicantsInfoView, InterviewUpdateView, IntraEventFormSubmissionCreateUpdateView, IntraEventFormSubmissionRetrieveUpdateDestroyView, PendingSubmissionsView, UserSpecificSubmissionsView

urlpatterns = [
    path('applicants/', ApplicantsCreateView.as_view(), name='create-applicant'),
    path('applicants/info/', ApplicantsInfoView.as_view(), name='applicants-info'),
    path('applicants/<str:custom_id>/', ApplicantsUpdateView.as_view(), name='view/update-applicant'),
    path('applicants/<str:custom_id>/delete/', ApplicantsDeleteView.as_view(), name='delete-applicant'),
    path('applicants/<str:custom_id>/interview/', InterviewUpdateView.as_view(), name='update-interview'), #/api/applicants/22101525_spring20699/interview/
    path('intra-event/create-update/', IntraEventFormSubmissionCreateUpdateView.as_view(), name='create-update-submission'),
    path('intra-event/user-specific/', UserSpecificSubmissionsView.as_view(), name='user-specific-submissions'),
    path('intra-event/all/', AllSubmissionsView.as_view(), name='all-submissions'),
    path('intra-event/pending/', PendingSubmissionsView.as_view(), name='pending-submissions'),
    path('intra-event/<int:pk>/', IntraEventFormSubmissionRetrieveUpdateDestroyView.as_view(), name='retrieve-update-destroy-submission'),
]
