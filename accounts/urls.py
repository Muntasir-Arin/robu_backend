from django.urls import path, include
from .views import CurrentPanelListAPIView, MemberListView, PanelListAPIView, PrivateUserProfileView, PublicUserProfileView, ResendVerificationEmailView, RobuUpdateView, UserProfileUpdateView, VerifyEmailView

urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('update-profile/', UserProfileUpdateView.as_view(), name='update-profile'),
    path('profile/<int:student_id>/', PublicUserProfileView.as_view(), name='public-profile'),
    path('private-profile/<int:id>/', PrivateUserProfileView.as_view(), name='private-profile'),
    path('panels/', PanelListAPIView.as_view(), name='panel-list'),
    path('secure/', RobuUpdateView.as_view(), name='user-list'),
    path('secure/<int:pk>/', RobuUpdateView.as_view(), name='user-detail'),
    path('current-panels/', CurrentPanelListAPIView.as_view(), name='curr-panel-list'),
    path('member-list/', MemberListView.as_view(), name='member-list'),
    path('auth/verify-email/<int:user_id>/<str:token>/', VerifyEmailView.as_view(), name='verify-email'),
    path('auth/resend-verification/', ResendVerificationEmailView.as_view(), name='resend-verification'),
]