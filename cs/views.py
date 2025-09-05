# cs/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from .models import Case
from .forms import CaseForm

@login_required
def case_list(request):
    qs = Case.objects.all()
    q = request.GET.get('q', '')
    status = request.GET.get('status', '')
    priority = request.GET.get('priority', '')
    if q:
        qs = qs.filter(title__icontains=q) | qs.filter(description__icontains=q)
    if status:
        qs = qs.filter(status=status)
    if priority:
        qs = qs.filter(priority=priority)
    return render(request, 'cs/case_list.html', {
        'cases': qs, 'q': q, 'status': status, 'priority': priority
    })

@login_required
def case_detail(request, pk):
    case = get_object_or_404(Case, pk=pk)
    return render(request, 'cs/case_detail.html', {'case': case})

@login_required
def case_create(request):
    if request.method == 'POST':
        form = CaseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('case_list')  # PRG 패턴
    else:
        form = CaseForm()
    return render(request, 'cs/case_form.html', {'form': form, 'mode': 'create'})

@login_required
def case_update(request, pk):
    case = get_object_or_404(Case, pk=pk)
    if request.method == 'POST':
        form = CaseForm(request.POST, instance=case)
        if form.is_valid():
            form.save()
            return redirect('case_detail', pk=pk)
    else:
        form = CaseForm(instance=case)
    return render(request, 'cs/case_form.html', {'form': form, 'mode': 'update'})

@login_required
def case_delete(request, pk):
    case = get_object_or_404(Case, pk=pk)
    if request.method == 'POST':
        case.delete()
        return redirect('case_list')
    return render(request, 'cs/case_confirm_delete.html', {'case': case})

