from rest_framework import viewsets, generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.utils.text import slugify
from .models import Profile, Payslip, Document, AdminNotification, WikiCategory, WikiPage, UserNotification
from .serializers import (
    ProfileSerializer, PayslipSerializer, 
    DocumentSerializer, AdminNotificationSerializer,
    WikiCategorySerializer, WikiPageSerializer,
    UserNotificationSerializer
)

class UserNotificationViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserNotificationSerializer

    def get_queryset(self):
        return UserNotification.objects.filter(user=self.request.user).order_by('-created_at')

class UserProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        profile, created = Profile.objects.get_or_create(user=request.user)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

    def patch(self, request):
        profile, created = Profile.objects.get_or_create(user=request.user)
        serializer = ProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PayslipViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PayslipSerializer

    def get_queryset(self):
        queryset = Payslip.objects.filter(user=self.request.user)
        month = self.request.query_params.get('month')
        year = self.request.query_params.get('year')
        if month:
            queryset = queryset.filter(month=month)
        if year:
            queryset = queryset.filter(year=year)
        return queryset

class DocumentViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = DocumentSerializer

    def get_queryset(self):
        return Document.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class GetProfileByEmailView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, email):
        from django.contrib.auth.models import User
        from rest_framework.authtoken.models import Token
        
        user, created = User.objects.get_or_create(
            email=email,
            defaults={'username': email.split('@')[0]}
        )
        
        profile, _ = Profile.objects.get_or_create(user=user)
        token, _ = Token.objects.get_or_create(user=user)
        
        serializer = ProfileSerializer(profile)
        data = serializer.data
        data['token'] = token.key
        return Response(data)

class AdminNotificationView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AdminNotificationSerializer
    queryset = AdminNotification.objects.filter(is_active=True)

class WikiCategoryViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    serializer_class = WikiCategorySerializer
    queryset = WikiCategory.objects.all()
    
    def perform_create(self, serializer):
        name = serializer.validated_data.get('name')
        serializer.save(slug=slugify(name))

class WikiPageViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    serializer_class = WikiPageSerializer
    queryset = WikiPage.objects.all()
    lookup_field = 'slug'

    def perform_create(self, serializer):
        title = serializer.validated_data.get('title')
        slug = slugify(title)
        if WikiPage.objects.filter(slug=slug).exists():
            import uuid
            slug = f"{slug}-{uuid.uuid4().hex[:6]}"
        
        # Only set author if user is authenticated, otherwise set to None
        author = self.request.user if self.request.user.is_authenticated else None
        serializer.save(author=author, slug=slug)
