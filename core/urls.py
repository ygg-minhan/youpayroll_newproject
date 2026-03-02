from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from .views import (
    UserProfileView, PayslipViewSet, 
    DocumentViewSet, AdminNotificationView,
    GetProfileByEmailView, WikiCategoryViewSet,
    WikiPageViewSet, UserNotificationViewSet
)

router = DefaultRouter()
router.register(r'payslips', PayslipViewSet, basename='payslip')
router.register(r'documents', DocumentViewSet, basename='document')
router.register(r'wiki-categories', WikiCategoryViewSet, basename='wiki-category')
router.register(r'wiki-pages', WikiPageViewSet, basename='wiki-page')
router.register(r'user-notifications', UserNotificationViewSet, basename='user-notification')

urlpatterns = [
    path('login/', obtain_auth_token, name='api_login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('profile-by-email/<str:email>/', GetProfileByEmailView.as_view(), name='profile_by_email'),
    path('notifications/', AdminNotificationView.as_view(), name='notifications'),
    path('', include(router.urls)),
]
