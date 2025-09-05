from django.shortcuts import render

# cs/views.py (임시)
from django.http import HttpResponse

def case_list(request):
    return HttpResponse("case list (stub)")

def case_detail(request, pk):
    return HttpResponse(f"case detail (stub) #{pk}")

def case_create(request):
    return HttpResponse("case create (stub)")

def case_update(request, pk):
    return HttpResponse(f"case update (stub) #{pk}")

def case_delete(request, pk):
    return HttpResponse(f"case delete (stub) #{pk}")