from django.urls import path, include
from .views import (
    RegisterView,
    LoginView,
    PatientDashboardView,
    PhysioDashboardView,
    ChatMessagesView,
    SendMessageView,
    SearchPhysiotherapistsView,
    BookAppointmentView,
    MyAppointmentsView,
    InitiatePaymentView,
    ConfirmPaymentView,
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('patient/dashboard/', PatientDashboardView.as_view(), name='patient-dashboard'),
    path('physio/dashboard/', PhysioDashboardView.as_view(), name='physio-dashboard'),
    path('chat/<int:receiver_id>/', ChatMessagesView.as_view(), name='chat-messages'),
    path('chat/send/', SendMessageView.as_view(), name='send-message'),
    path('physios/', SearchPhysiotherapistsView.as_view(), name='search-physios'),
    path('appointments/book/', BookAppointmentView.as_view(), name='book-appointment'),
    path('appointments/mine/', MyAppointmentsView.as_view(), name='my-appointments'),
    path('payment/initiate/', InitiatePaymentView.as_view(), name='initiate-payment'),
    path('payment/confirm/', ConfirmPaymentView.as_view(), name='confirm-payment'),
]
