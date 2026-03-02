from rest_framework import viewsets, permissions
from .models import PayRun, Payment, PayRecordRegister, Form16, Form16Entry
from .serializers import PayRunSerializer, PaymentSerializer, PayRecordRegisterSerializer, Form16Serializer, Form16EntrySerializer

class PayRunViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PayRunSerializer
    queryset = PayRun.objects.all()

class PaymentViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()

class PayRecordRegisterViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PayRecordRegisterSerializer
    queryset = PayRecordRegister.objects.all()

class Form16ViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = Form16Serializer
    queryset = Form16.objects.all()

class Form16EntryViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = Form16EntrySerializer
    queryset = Form16Entry.objects.all()
