from django import forms
from .models import Case

class CaseForm(forms.ModelForm):
    class Meta:
        model = Case
        fields = ['title', 'description', 'device_name', 'assignee', 'customer_name', 'priority', 'status']
        widgets = {'description': forms.Textarea(attrs={'rows': 4})}
        labels = {
            'title': '제목', 'description': '내용',
            'device_name': '장비명', 'assignee': 'CS담당자', 'customer_name': '고객명',
            'priority': '우선순위', 'status': '상태',
        }