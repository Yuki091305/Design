from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from .models import DesignRequest, Category
from .forms import UserRegistrationForm, DesignRequestForm, AdminStatusForm
from django.core.exceptions import PermissionDenied
def index(request):
    completed = DesignRequest.objects.filter(status='completed').order_by('-created_at')[:4]
    in_progress_count = DesignRequest.objects.filter(status='in_progress').count()
    return render(request, 'index.html', {
        'completed_requests': completed,
        'in_progress_count': in_progress_count
    })

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password2'])
            user.save()
            messages.success(request, "Регистрация успешна! Войдите.")
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'catalog/register.html', {'form': form})

@login_required
def user_dashboard(request):
    status = request.GET.get('status')
    qs = DesignRequest.objects.filter(user=request.user)
    if status:
        qs = qs.filter(status=status)
    return render(request, 'catalog/user_dashboard.html', {
        'requests': qs,
        'status_filter': status
    })

@login_required
def request_create(request):
    if request.user.is_staff:
        raise PermissionDenied("Администраторы не могут создавать заявки.")
    if request.method == 'POST':
        form = DesignRequestForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            messages.success(request, "Заявка создана!")
            return redirect('user_dashboard')
    else:
        form = DesignRequestForm()
    return render(request, 'catalog/request_form.html', {'form': form})

@login_required
def request_delete(request, pk):
    req = get_object_or_404(DesignRequest, pk=pk, user=request.user)
    if req.status != 'new':
        messages.error(request, "Удалять можно только заявки со статусом 'Новая'.")
        return redirect('user_dashboard')
    if request.method == 'POST':
        req.delete()
        messages.success(request, "Заявка удалена.")
        return redirect('user_dashboard')
    return render(request, 'catalog/request_confirm_delete.html', {'request': req})

@login_required
def request_detail(request, pk):
    req = get_object_or_404(DesignRequest, pk=pk, user=request.user)
    return render(request, 'catalog/request_detail.html', {'request': req})

@staff_member_required
def admin_dashboard(request):
    requests = DesignRequest.objects.all()
    return render(request, 'catalog/admin_dashboard.html', {'requests': requests})

@staff_member_required
def admin_update_status(request, pk):
    req = get_object_or_404(DesignRequest, pk=pk)
    if request.method == 'POST':
        form = AdminStatusForm(request.POST, request.FILES, instance=req)
        if form.is_valid():
            form.save()
            messages.success(request, "Статус обновлён!")
            return redirect('admin_dashboard')
    else:
        form = AdminStatusForm(instance=req)
    return render(request, 'catalog/admin_status_form.html', {'form': form, 'request': req})