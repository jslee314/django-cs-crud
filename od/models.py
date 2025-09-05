from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class LogUpload(models.Model):
    file = models.FileField(upload_to='uploads/%Y/%m/%d/')
    original_name = models.CharField(max_length=255)
    uploaded_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.original_name

class AnalysisRun(models.Model):
    upload = models.ForeignKey(LogUpload, on_delete=models.CASCADE, related_name='runs')
    started_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(null=True, blank=True)
    summary = models.JSONField(default=dict, blank=True)  # 통계/카운트 요약
    ok = models.BooleanField(default=True)                # 심각 이상 여부

    def __str__(self):
        return f'Run#{self.id} for {self.upload.original_name}'

class AnomalyEvent(models.Model):
    run = models.ForeignKey(AnalysisRun, on_delete=models.CASCADE, related_name='events')
    kind = models.CharField(max_length=50)               # 예: gap, spike, cv_high 등
    severity = models.CharField(max_length=10, default='low')  # low/med/high
    index = models.IntegerField(null=True, blank=True)   # 몇 번째 측정/행
    message = models.TextField(blank=True)
    data = models.JSONField(default=dict, blank=True)    # 상세 수치

