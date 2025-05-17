from django.contrib.auth.models import AbstractUser
from django.db import models

# ------------------ Users Table ------------------
class User(AbstractUser):
    ROLE_CHOICES = (
        ('patient', 'Patient'),
        ('physiotherapist', 'Physiotherapist'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

# ------------------ Physiotherapists Table ------------------
class Physiotherapist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    experience_years = models.IntegerField(default=0)

# ------------------ Patients Table ------------------
class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField()
    gender = models.CharField(max_length=10)

# ------------------ Physio Appointments Table ------------------
class PhysioAppointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    physiotherapist = models.ForeignKey(Physiotherapist, on_delete=models.CASCADE)
    scheduled_time = models.DateTimeField()
    status = models.CharField(max_length=20, choices=(('pending', 'Pending'), ('confirmed', 'Confirmed'), ('completed', 'Completed')))

# ------------------ Patient Dashboard Metrics ------------------
class PatientDashboardMetrics(models.Model):
    patient = models.OneToOneField(Patient, on_delete=models.CASCADE)
    exercise_progress = models.FloatField(default=0.0)
    streak_days = models.IntegerField(default=0)
    next_meeting = models.DateTimeField(null=True, blank=True)
    adherence_rate = models.FloatField(default=0.0)
    recovery_progress = models.JSONField(default=dict)  # store graphs data as JSON
    treatment_plan_progress = models.FloatField(default=0.0)
    upcoming_session_link = models.URLField(blank=True, null=True)

# ------------------ Physio Dashboard Metrics ------------------
class PhysioDashboardMetrics(models.Model):
    physiotherapist = models.OneToOneField(Physiotherapist, on_delete=models.CASCADE)
    active_patients_count = models.IntegerField(default=0)

# ------------------ Physio Patient History ------------------
class PhysioPatientHistory(models.Model):
    physiotherapist = models.ForeignKey(Physiotherapist, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    history_notes = models.TextField(blank=True)
    last_updated = models.DateTimeField(auto_now=True)

# ------------------ Exercise Tracking ------------------
class ExerciseTracking(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    exercise_name = models.CharField(max_length=255)
    completion_status = models.BooleanField(default=False)
    completion_date = models.DateField()
    accuracy_score = models.FloatField(default=0.0)

# ------------------ Treatment Plans ------------------
class TreatmentPlan(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    physiotherapist = models.ForeignKey(Physiotherapist, on_delete=models.CASCADE)
    plan_name = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    progress_percentage = models.FloatField(default=0.0)

# ------------------ Treatment Progress ------------------
class TreatmentProgress(models.Model):
    treatment_plan = models.ForeignKey(TreatmentPlan, on_delete=models.CASCADE)
    date = models.DateField()
    progress_notes = models.TextField(blank=True)
    pain_level = models.IntegerField(default=0)  # 0-10 scale

# ------------------ Patient Notifications ------------------
class PatientNotification(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

# ------------------ Patient Reviews ------------------
class PatientReview(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    physiotherapist = models.ForeignKey(Physiotherapist, on_delete=models.CASCADE)
    review_text = models.TextField()
    rating = models.IntegerField(default=5)
    created_at = models.DateTimeField(auto_now_add=True)

# ------------------ Chat Messages ------------------
class ChatMessage(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    message_text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

class Payment(models.Model):
    appointment = models.OneToOneField(PhysioAppointment, on_delete=models.CASCADE)
    amount = models.FloatField()
    payment_status = models.CharField(max_length=20, choices=(('pending', 'Pending'), ('success', 'Success'), ('failed', 'Failed')), default='pending')
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

