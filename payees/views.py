from rest_framework import viewsets, permissions
from .models import Payee, BankDetail, BankDetailAcknowledgement
from .serializers import PayeeSerializer, BankDetailSerializer, BankDetailAcknowledgementSerializer

class PayeeViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PayeeSerializer
    queryset = Payee.objects.all()

class BankDetailViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BankDetailSerializer
    queryset = BankDetail.objects.all()

class BankDetailAcknowledgementViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BankDetailAcknowledgementSerializer
    queryset = BankDetailAcknowledgement.objects.all()
