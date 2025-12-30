from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from .forms import RegisterForm
from .models import Document, TariffDocument


def home(request):
    return render(request, "main/home.html")


def tariffs(request):
    return render(request, "main/tariffs.html")


def contacts(request):
    return render(request, "main/contacts.html")


def about(request):
    return render(request, "main/about.html")


def why(request):
    return render(request, "main/why.html")


def how(request):
    return render(request, "main/how.html")


def documentation(request):
    return render(request, "main/documentation.html")


def consumer(request):
    document = None
    try:
        document = Document.objects.get(title="Звіт про звернення за 2020 рік")
    except Document.DoesNotExist:
        pass

    return render(request, "main/consumer.html", {"document": document})


def contract_docs(request):
    return render(request, "main/contract_docs.html")


def start(request):
    return render(request, "main/start.html")


def complaints(request):
    return render(request, "main/complaints.html")


def documentation_overview(request):
    return render(request, "main/documentation_overview.html")


def tariffs_view(request):
    doc_2021 = get_object_or_404(TariffDocument, year=2021)
    return render(request, "main/tariffs.html", {"doc_2021": doc_2021})


def appeals(request):
    return render(request, "main/appeals.html")


# ✅ React cabinet entrypoint (для /cabinet/*)
def cabinet(request, path=None):
    return render(request, "cabinet/index.html")


# ⚠️ Старий register у main (краще прибрати з urls)
# Якщо все ще потрібен — залишай, але НЕ називай його 'register' у urls, бо буде конфлікт.
def legacy_register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Реєстрація успішна! Можете увійти.")
            return redirect("home")
    else:
        form = RegisterForm()
    return render(request, "register.html", {"form": form})
