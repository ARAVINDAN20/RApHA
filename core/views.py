from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

from .models import Patient, Physiotherapist, PhysioAppointment, Payment, ChatMessage, User, PatientDashboardMetrics, PhysioDashboardMetrics
from .serializers import (
    UserSerializer,
    PatientDashboardMetricsSerializer,
    PhysioDashboardMetricsSerializer,
    ChatMessageSerializer,
    PhysiotherapistSerializer,
    PhysioAppointmentSerializer,
    PaymentSerializer

)

# Register View
class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        role = request.data.get('role')

        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, email=email, password=password, role=role)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

# Login View (JWT Token + Role Based)
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            role = user.role

            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'role': role
            })
        else:
            return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)

# Patient Dashboard View
class PatientDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            patient_metrics = PatientDashboardMetrics.objects.get(patient__user=request.user)
            serializer = PatientDashboardMetricsSerializer(patient_metrics)
            return Response(serializer.data)
        except PatientDashboardMetrics.DoesNotExist:
            return Response({'error': 'Metrics not found for this patient'}, status=404)

# Physio Dashboard View
class PhysioDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            physio_metrics = PhysioDashboardMetrics.objects.get(physiotherapist__user=request.user)
            serializer = PhysioDashboardMetricsSerializer(physio_metrics)
            return Response(serializer.data)
        except PhysioDashboardMetrics.DoesNotExist:
            return Response({'error': 'Metrics not found for this physiotherapist'}, status=404)

# Chat Messages View (Get conversation)
class ChatMessagesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, receiver_id):
        messages = ChatMessage.objects.filter(
            sender=request.user, receiver__id=receiver_id
        ) | ChatMessage.objects.filter(
            sender__id=receiver_id, receiver=request.user
        )
        messages = messages.order_by('timestamp')
        serializer = ChatMessageSerializer(messages, many=True)
        return Response(serializer.data)

# Send Chat Message View
class SendMessageView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        receiver_id = request.data.get('receiver_id')
        message_text = request.data.get('message_text')

        if not receiver_id or not message_text:
            return Response({'error': 'receiver_id and message_text are required'}, status=400)

        try:
            receiver = User.objects.get(id=receiver_id)
        except User.DoesNotExist:
            return Response({'error': 'Receiver not found'}, status=404)

        chat_message = ChatMessage.objects.create(
            sender=request.user,
            receiver=receiver,
            message_text=message_text
        )
        serializer = ChatMessageSerializer(chat_message)
        return Response(serializer.data, status=201)

# Search Physiotherapists View
class SearchPhysiotherapistsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        physiotherapists = Physiotherapist.objects.all()
        serializer = PhysiotherapistSerializer(physiotherapists, many=True)
        return Response(serializer.data)

# Book Appointment View
class BookAppointmentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        physio_id = request.data.get('physio_id')
        scheduled_time = request.data.get('scheduled_time')  # ISO format datetime

        if not physio_id or not scheduled_time:
            return Response({'error': 'physio_id and scheduled_time are required'}, status=400)

        try:
            patient = request.user.patient
            physiotherapist = Physiotherapist.objects.get(id=physio_id)
        except (Patient.DoesNotExist, Physiotherapist.DoesNotExist):
            return Response({'error': 'Invalid patient or physiotherapist'}, status=404)

        appointment = PhysioAppointment.objects.create(
            patient=patient,
            physiotherapist=physiotherapist,
            scheduled_time=scheduled_time,
            status='pending'
        )
        serializer = PhysioAppointmentSerializer(appointment)
        return Response(serializer.data, status=201)

# My Appointments View (Patient's Bookings)
class MyAppointmentsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            patient = request.user.patient
        except Patient.DoesNotExist:
            return Response({'error': 'Not a patient'}, status=403)

        appointments = PhysioAppointment.objects.filter(patient=patient)
        serializer = PhysioAppointmentSerializer(appointments, many=True)
        return Response(serializer.data)

# Initiate Payment (creates pending payment entry)
class InitiatePaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        appointment_id = request.data.get('appointment_id')
        amount = request.data.get('amount')

        if not appointment_id or not amount:
            return Response({'error': 'appointment_id and amount are required'}, status=400)

        try:
            appointment = PhysioAppointment.objects.get(id=appointment_id)
        except PhysioAppointment.DoesNotExist:
            return Response({'error': 'Appointment not found'}, status=404)

        payment, created = Payment.objects.get_or_create(appointment=appointment, defaults={'amount': amount})

        serializer = PaymentSerializer(payment)
        return Response(serializer.data, status=201 if created else 200)

# Confirm Payment (simulate success)
class ConfirmPaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        payment_id = request.data.get('payment_id')
        transaction_id = request.data.get('transaction_id')

        if not payment_id or not transaction_id:
            return Response({'error': 'payment_id and transaction_id are required'}, status=400)

        try:
            payment = Payment.objects.get(id=payment_id)
        except Payment.DoesNotExist:
            return Response({'error': 'Payment not found'}, status=404)

        payment.payment_status = 'success'
        payment.transaction_id = transaction_id
        payment.save()

        serializer = PaymentSerializer(payment)
        return Response(serializer.data)