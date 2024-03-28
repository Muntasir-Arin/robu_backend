from rest_framework import generics, permissions
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Applicant, IntraEventFormSubmission
from .serializers import  ApplicantsSerializer, InterviewSerializer, IntraEventFormSerializer, IntraEventFormSubmissionSerializer
from rest_framework.views import APIView
from django.core.mail import send_mail
from django.conf import settings


class IsAdminOrInterviewer(permissions.BasePermission):
    def has_permission(self, request, view):
        # Check if the user is an admin or president
        return request.user.is_admin_or_panel or request.user.is_admin_or_dads

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
    
class ApplicantsUpdateView(generics.UpdateAPIView, generics.RetrieveAPIView):
    queryset = Applicant.objects.all()
    serializer_class = ApplicantsSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'custom_id'

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

class ApplicantsDeleteView(generics.DestroyAPIView):
    queryset = Applicant.objects.all()
    serializer_class = ApplicantsSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'custom_id'

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ApplicantsInfoView(generics.ListAPIView):
    serializer_class = ApplicantsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_id = self.request.user.id
        return Applicant.objects.filter(user_id=user_id)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        
        data = [{'id': applicant.custom_id} for applicant in queryset]
        return Response(data)
    

class InterviewUpdateView(generics.UpdateAPIView, generics.RetrieveAPIView):
    queryset = Applicant.objects.all()
    serializer_class = InterviewSerializer
    permission_classes = [IsAuthenticated, IsAdminOrInterviewer]
    lookup_field = 'custom_id'
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
    

#Event ----------------------------------------------------------------------------------
class IntraEventFormSubmissionCreateUpdateView(generics.CreateAPIView, generics.UpdateAPIView):
    queryset = IntraEventFormSubmission.objects.all()
    serializer_class = IntraEventFormSubmissionSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class UserSpecificSubmissionsView(generics.ListAPIView):
    serializer_class = IntraEventFormSubmissionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_id = self.request.user.id
        event_name = self.request.query_params.get('event_name', None)
        return IntraEventFormSubmission.objects.filter(user_id=user_id, event_name=event_name)

class AllSubmissionsView(generics.ListAPIView):
    serializer_class = IntraEventFormSerializer
    permission_classes = [IsAuthenticated, IsAdminOrInterviewer]

    def get_queryset(self):
        event_name = self.request.query_params.get('event_name', None)
        return IntraEventFormSubmission.objects.filter(event_name=event_name)

class PendingSubmissionsView(generics.ListAPIView):
    serializer_class = IntraEventFormSerializer
    permission_classes = [IsAuthenticated, IsAdminOrInterviewer]

    def get_queryset(self):
        event_name = self.request.query_params.get('event_name', None)
        return IntraEventFormSubmission.objects.filter(event_name=event_name, payment_status='Pending')
    
class IntraEventFormSubmissionRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = IntraEventFormSubmission.objects.all()
    serializer_class = IntraEventFormSerializer
    permission_classes = [IsAuthenticated, IsAdminOrInterviewer]
    def perform_update(self, serializer):
        serializer.save(approved_by=self.request.user.name)
    def get_serializer(self, *args, **kwargs):
        serializer = super().get_serializer(*args, **kwargs)
        if 'approved_by' in serializer.fields:
            serializer.fields['approved_by'].read_only = True
        return serializer
    

class UnauthorizedEventFormSubmission(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data.copy()
        data.pop('user', None)

        serializer = IntraEventFormSubmissionSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

#------------------------------------------------------------------
class UpdatePaymentStatus(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated, IsAdminOrInterviewer]
    serializer_class = IntraEventFormSerializer
    queryset = IntraEventFormSubmission.objects.all()

    def update(self, request, *args, **kwargs):
        transaction_id = request.data.get('transaction_id', None)
        if transaction_id is None:
            return Response({'error': 'Transaction ID not provided'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            form_submission = self.get_queryset().get(transaction_id=transaction_id)
        except IntraEventFormSubmission.DoesNotExist:
            return Response({'error': 'Transaction ID not found'}, status=status.HTTP_404_NOT_FOUND)

        form_submission.payment_status = 'Approved'
        form_submission.save()

        # Send email notification
        gsuit_1_email = form_submission.gsuit_1
        if gsuit_1_email:
            send_mail(
                subject='Payment Confirmed',
                message='Your payment has been confirmed.',
                from_email=None,  # Use the default email address specified in settings.py
                recipient_list=[gsuit_1_email],
                fail_silently=False,
            )

        serializer = self.get_serializer(form_submission)
        return Response({'Payment Confirmed'}, status=status.HTTP_200_OK)
    
class SendEmailAPIView(APIView):
    def post(self, request):
        email_address = request.data.get('emailAddress')
        email_subject = request.data.get('emailSubject')
        email_body = request.data.get('emailBody')

        try:
            send_mail(
                email_subject,
                email_body,
                settings.DEFAULT_FROM_EMAIL,
                [email_address],
                fail_silently=False,
            )
            return Response({'success': True, 'message': 'Email sent successfully.'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'success': False, 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)