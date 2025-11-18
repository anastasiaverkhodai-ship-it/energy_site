from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegisterForm
from .models import Document
from .models import TariffDocument


def home(request):
    return render(request, 'main/home.html')

def tariffs(request):
    return render(request, 'main/tariffs.html')

def contacts(request):
    return render(request, 'main/contacts.html')

def about(request):
    return render(request, "main/about.html")   # краще покласти в папку main/

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Реєстрація успішна! Можете увійти.')
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})
def why(request):
    return render(request, 'main/why.html')
def how(request):
    return render(request, 'main/how.html')
def documentation(request):
    return render(request, 'main/documentation.html')
def consumer(request):
    # Беремо PDF за назвою
    document = None
    try:
        document = Document.objects.get(title="Звіт про звернення за 2020 рік")
    except Document.DoesNotExist:
        pass
    return render(request, 'main/consumer.html', {'document': document})
def contract_docs(request):
    return render(request, 'main/contract_docs.html')
def start(request):
    return render(request, 'main/start.html')
def complaints(request):
    return render(request, 'main/complaints.html')
def documentation_overview(request):
    return render(request, 'main/documentation_overview.html')
def appeals(request):
    document = Document.objects.get(
        title="Інформація щодо дотримання загальних та гарантованих стандартів якості надання послуг за 2018 рік"
    )
    return render(request, 'main/appeals.html', {"document": document})

from django.shortcuts import render, get_object_or_404
from .models import TariffDocument

def tariffs_view(request):
    # Беремо документ 2021 року
    doc_2021 = get_object_or_404(TariffDocument, year=2021)
    
    return render(request, "tariffs.html", {
        "doc_2021": doc_2021
    })
