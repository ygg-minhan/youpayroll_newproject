from rest_framework import serializers
from .models import Payee, BankDetail, BankDetailAcknowledgement

class BankDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankDetail
        fields = '__all__'

class PayeeSerializer(serializers.ModelSerializer):
    bank_details = BankDetailSerializer(many=True, read_only=True)
    class Meta:
        model = Payee
        fields = '__all__'

class BankDetailAcknowledgementSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankDetailAcknowledgement
        fields = '__all__'
