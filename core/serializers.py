from rest_framework import serializers
from .models import User, PatientDashboardMetrics, PhysioDashboardMetrics, ChatMessage, Physiotherapist, PhysioAppointment, Payment

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role']

class PatientDashboardMetricsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientDashboardMetrics
        fields = '__all__'

class PhysioDashboardMetricsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhysioDashboardMetrics
        fields = '__all__'

class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = '__all__'

class PhysiotherapistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Physiotherapist
        fields = '__all__'

class PhysioAppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhysioAppointment
        fields = '__all__'

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
