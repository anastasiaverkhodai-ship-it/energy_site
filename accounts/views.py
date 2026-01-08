from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Q
from django.contrib import messages
from django.core.exceptions import PermissionDenied

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import Contragent, Agreement
from .forms import UserRegisterForm

# ==========================================
# АВТЕНТИФІКАЦІЯ (Вхід, Вихід, Реєстрація)
# ==========================================

def login_view(request):
    """Вхід у систему з оформленням полів форми"""
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('cabinet')
    else:
        form = AuthenticationForm()
        for field in form.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    """Вихід із системи"""
    logout(request)
    return redirect('login')

def register_view(request):
    """Самостійна реєстрація нового користувача"""
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password']) 
            user.save()
            login(request, user) 
            return redirect('cabinet') 
    else:
        form = UserRegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

# ==========================================
# ГОЛОВНА ПАНЕЛЬ (Dashboard) ТА ПРОФІЛЬ
# ==========================================

@login_required
def cabinet_view(request):
    """Головна сторінка кабінету зі статистикою"""
    context = {
        'total_users': User.objects.count(),
        'total_contragents': Contragent.objects.count(),
        'total_agreements': Agreement.objects.count(),
        'total_docs': Agreement.objects.exclude(file='').exclude(file__isnull=True).count(),
        'recent_agreements': Agreement.objects.select_related('contragent').order_by('-id')[:5]
    }
    return render(request, 'accounts/cabinet.html', context)

@login_required
def profile_view(request):
    """Оновлення даних профілю користувача"""
    if request.method == 'POST':
        request.user.first_name = request.POST.get('first_name')
        request.user.last_name = request.POST.get('last_name')
        request.user.email = request.POST.get('email')
        request.user.save()
        messages.success(request, 'Профіль успішно оновлено!')
        return redirect('profile')
    return render(request, 'accounts/profile.html')

# ==========================================
# УПРАВЛІННЯ ДОКУМЕНТАМИ (Доступ Клієнт/Адмін)
# ==========================================

@login_required
def documents_list(request):
    if request.user.is_staff:
        # Адмін бачить ВСЕ
        documents = Agreement.objects.exclude(file='')
    else:
        # Клієнт бачить документи ТІЛЬКИ своєї компанії
        # Перевіряємо, чи взагалі у юзера є прив'язаний контрагент
        if hasattr(request.user, 'contragent'):
            documents = Agreement.objects.filter(contragent=request.user.contragent).exclude(file='')
        else:
            documents = Agreement.objects.none()  # Порожній список, якщо не прив'язаний
    
    return render(request, 'accounts/documents.html', {'documents': documents})
@login_required
def upload_document_view(request):
    """Дозволяє завантажувати скан-копії до бази"""
    # Тільки персонал може додавати документи (можна змінити для клієнтів)
    if not request.user.is_staff:
        return redirect('cabinet')
        
    contragents = Contragent.objects.all()
    if request.method == 'POST':
        number = request.POST.get('number')
        date = request.POST.get('date')
        contragent_id = request.POST.get('contragent')
        uploaded_file = request.FILES.get('file')
        
        contragent = get_object_or_404(Contragent, id=contragent_id)
        Agreement.objects.create(
            number=number,
            date=date,
            contragent=contragent,
            file=uploaded_file
        )
        messages.success(request, 'Документ успішно додано!')
        return redirect('documents')
    return render(request, 'accounts/upload_document.html', {'contragents': contragents})

# ==========================================
# УПРАВЛІННЯ КОНТРАГЕНТАМИ ТА ДОГОВОРАМИ (Тільки Адмін)
# ==========================================

@login_required
def contragents_list(request):
    if not request.user.is_staff:
        return redirect('cabinet')
    return render(request, 'accounts/contragents.html', {'contragents': Contragent.objects.all()})

@login_required
def edit_contragent_view(request, contragent_id=None):
    if not request.user.is_staff:
        return redirect('cabinet')
    instance = get_object_or_404(Contragent, id=contragent_id) if contragent_id else None
    if request.method == 'POST':
        name = request.POST.get('name')
        edrpou = request.POST.get('edrpou')
        manager = request.POST.get('manager')
        if instance:
            instance.name, instance.edrpou, instance.manager = name, edrpou, manager
            instance.save()
        else:
            Contragent.objects.create(name=name, edrpou=edrpou, manager=manager)
        return redirect('contragents')
    return render(request, 'accounts/edit_contragent.html', {'instance': instance})

@login_required
def delete_contragent_view(request, contragent_id):
    if not request.user.is_staff:
        return redirect('cabinet')
    get_object_or_404(Contragent, id=contragent_id).delete()
    return redirect('contragents')

@login_required
def agreements_list(request):
    if not request.user.is_staff:
        return redirect('cabinet')
    agreements = Agreement.objects.select_related('contragent').all()
    return render(request, 'accounts/agreements.html', {'agreements': agreements})

@login_required
def edit_agreement_view(request, agreement_id=None):
    if not request.user.is_staff:
        return redirect('cabinet')
    instance = get_object_or_404(Agreement, id=agreement_id) if agreement_id else None
    contragents = Contragent.objects.all()
    if request.method == 'POST':
        contragent = get_object_or_404(Contragent, id=request.POST.get('contragent'))
        if instance:
            instance.number = request.POST.get('number')
            instance.date = request.POST.get('date')
            instance.contragent = contragent
            if request.FILES.get('file'):
                instance.file = request.FILES.get('file')
            instance.save()
        else:
            Agreement.objects.create(
                number=request.POST.get('number'),
                date=request.POST.get('date'),
                contragent=contragent,
                file=request.FILES.get('file')
            )
        return redirect('agreements')
    return render(request, 'accounts/edit_agreement.html', {'instance': instance, 'contragents': contragents})

@login_required
def delete_agreement_view(request, agreement_id):
    if not request.user.is_staff:
        return redirect('cabinet')
    get_object_or_404(Agreement, id=agreement_id).delete()
    return redirect('agreements')

# ==========================================
# УПРАВЛІННЯ КОРИСТУВАЧАМИ (Тільки Адмін)
# ==========================================

@login_required
def users_list_view(request):
    if not request.user.is_staff:
        return redirect('cabinet')
    return render(request, 'accounts/users.html', {'users': User.objects.all()})

@login_required
def add_user_view(request):
    if not request.user.is_staff:
        return redirect('cabinet')
    form = UserRegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('users_list')
    return render(request, 'accounts/register.html', {'form': form, 'admin_mode': True})

@login_required
def edit_user_view(request, user_id):
    if not request.user.is_staff:
        return redirect('cabinet')
    u = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        u.username, u.email = request.POST.get('username'), request.POST.get('email')
        u.first_name, u.last_name = request.POST.get('first_name'), request.POST.get('last_name')
        u.save()
        return redirect('users_list')
    return render(request, 'accounts/edit_user.html', {'user_to_edit': u})

@login_required
def delete_user_view(request, user_id):
    if not request.user.is_staff:
        return redirect('cabinet')
    u = get_object_or_404(User, id=user_id)
    if u != request.user: u.delete()
    return redirect('users_list')

# ==========================================
# API ДЛЯ МОБІЛЬНОГО ДОДАТКА
# ==========================================

@api_view(["POST"])
@permission_classes([AllowAny])
def api_register(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if not username or not password:
        return Response({"detail": "Username та Password обов'язкові"}, status=400)
    if User.objects.filter(username=username).exists():
        return Response({"detail": "Користувач вже існує"}, status=400)
    user = User.objects.create_user(username=username, password=password)
    return Response({"id": user.id, "username": user.username}, status=201)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def api_me(request):
    return Response({
        "id": request.user.id,
        "username": request.user.username,
        "email": request.user.email
    })