# cs/views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Case
from .forms import CaseForm

def case_list(request):
    cases = Case.objects.all()
    return render(request, 'cs/case_list.html', {'cases': cases})

def case_detail(request, pk):
    case = get_object_or_404(Case, pk=pk)
    return render(request, 'cs/case_detail.html', {'case': case})

def case_create(request):
    if request.method == 'POST':
        form = CaseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('case_list')  # PRG 패턴
    else:
        form = CaseForm()
    return render(request, 'cs/case_form.html', {'form': form, 'mode': 'create'})

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

def case_delete(request, pk):
    case = get_object_or_404(Case, pk=pk)
    if request.method == 'POST':
        case.delete()
        return redirect('case_list')
    return render(request, 'cs/case_confirm_delete.html', {'case': case})

