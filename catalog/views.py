from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django import forms
from django.contrib import messages
from .models import DesignRequest, Category


# ---------- Главная страница ----------
def index(request):
    """Главная страница — видна всем: гостям, пользователям, админу."""
    return render(request, 'index.html')


# ---------- Личный кабинет пользователя ----------
@login_required
def user_dashboard(request):
    """Показывает заявки текущего пользователя."""
    requests = DesignRequest.objects.filter(user=request.user)
    return render(request, 'catalog/user_dashboard.html', {'requests': requests})


# ---------- Форма для создания заявки ----------
class DesignRequestForm(forms.ModelForm):
    class Meta:
        model = DesignRequest
        fields = ['title', 'description', 'category', 'attachment']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }


@login_required
def request_create(request):
    """Создание новой заявки."""
    if request.method == 'POST':
        form = DesignRequestForm(request.POST, request.FILES)
        if form.is_valid():
            new_request = form.save(commit=False)
            new_request.user = request.user
            new_request.save()
            messages.success(request, "Заявка успешно создана!")
            return redirect('user_dashboard')
    else:
        form = DesignRequestForm()
    return render(request, 'catalog/request_form.html', {'form': form})


# ---------- Удаление своей заявки ----------
@login_required
def request_delete(request, pk):
    """Удаление заявки — только своей!"""
    req = get_object_or_404(DesignRequest, pk=pk, user=request.user)
    if request.method == 'POST':
        req.delete()
        messages.success(request, "Заявка удалена.")
        return redirect('user_dashboard')
    return render(request, 'catalog/request_confirm_delete.html', {'request': req})


# ---------- Админка: все заявки ----------
@staff_member_required
def admin_dashboard(request):
    """Админ видит все заявки."""
    requests = DesignRequest.objects.all()
    return render(request, 'catalog/admin_dashboard.html', {'requests': requests})


# ---------- Форма для изменения статуса (админ) ----------
class StatusUpdateForm(forms.ModelForm):
    class Meta:
        model = DesignRequest
        fields = ['status']


@staff_member_required
def admin_update_status(request, pk):
    """Админ меняет статус заявки."""
    req = get_object_or_404(DesignRequest, pk=pk)
    if request.method == 'POST':
        form = StatusUpdateForm(request.POST, instance=req)
        if form.is_valid():
            form.save()
            messages.success(request, "Статус обновлён!")
            return redirect('admin_dashboard')
    else:
        form = StatusUpdateForm(instance=req)
    return render(request, 'catalog/admin_update_status.html', {'form': form, 'request': req})