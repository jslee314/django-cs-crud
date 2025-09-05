from django.db import models

# Create your models here.

class Case(models.Model):
    PRIORITY_CHOICES = [
        ('LOW', '낮음'),
        ('MED', '보통'),
        ('HIGH', '높음'),
    ]
    STATUS_CHOICES = [
        ('NEW', '신규'),
        ('INP', '처리중'),
        ('RES', '해결'),
        ('CLS', '종료'),
    ]

    title = models.CharField('제목', max_length=100)
    description = models.TextField('내용', blank=True)

    device_name = models.CharField('장비명', max_length=50, blank=True)
    assignee = models.CharField('CS담당자', max_length=50, blank=True)
    customer_name = models.CharField('고객명', max_length=50, blank=True)

    priority = models.CharField('우선순위', max_length=4, choices=PRIORITY_CHOICES, default='MED')
    status = models.CharField('상태', max_length=3, choices=STATUS_CHOICES, default='NEW')

    created_at = models.DateTimeField('등록시각', auto_now_add=True)
    updated_at = models.DateTimeField('수정시각', auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'[{self.get_status_display()}] {self.title}'