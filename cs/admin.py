from django.contrib import admin
from .models import Case

@admin.register(Case)
class CaseAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'device_name', 'assignee', 'customer_name', 'priority', 'status', 'created_at')
    list_filter = ('priority', 'status')
    search_fields = ('title', 'description', 'device_name', 'assignee', 'customer_name')