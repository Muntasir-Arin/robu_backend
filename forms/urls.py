from django.urls import path
from .views import ApplicantsCreateView, ApplicantsUpdateView, ApplicantsDeleteView, ApplicantsInfoView, InterviewUpdateView

urlpatterns = [
    path('applicants/', ApplicantsCreateView.as_view(), name='create-applicant'),
    path('applicants/<int:pk>/', ApplicantsUpdateView.as_view(), name='update-applicant'),
    path('applicants/<int:pk>/delete/', ApplicantsDeleteView.as_view(), name='delete-applicant'),
    path('applicants/info/', ApplicantsInfoView.as_view(), name='applicants-info'),
     path('applicants/<int:pk>/interview/', InterviewUpdateView.as_view(), name='update-interview'),
]
