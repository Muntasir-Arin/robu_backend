from django.urls import path, include
from .views import CurrentPanelListAPIView, GetUserPositionView, MemberListView, PanelListAPIView, PrivateUserProfileView, PublicUserProfileView, RobuUpdateView, UserProfileUpdateView

urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('update-profile/', UserProfileUpdateView.as_view(), name='update-profile'),
    path('profile/<int:student_id>/', PublicUserProfileView.as_view(), name='public-profile'),
    path('private-profile/<int:id>/', PrivateUserProfileView.as_view(), name='private-profile'),
    path('panels/', PanelListAPIView.as_view(), name='panel-list'),
    path('secure/', RobuUpdateView.as_view(), name='secure'),
    path('position/', GetUserPositionView.as_view(), name='position'),
    path('current-panels/', CurrentPanelListAPIView.as_view(), name='curr-panel-list'),
    path('member-list/', MemberListView.as_view(), name='member-list')  #/api/member-list/?filter=current
]