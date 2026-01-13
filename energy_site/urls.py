from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.http import HttpResponse
from django.contrib.sitemaps import views as sitemap_views

from main import views as main_views
from accounts import views as accounts_views
from main.sitemaps import StaticViewSitemap

# --- SITEMAP FIX ---
sitemaps = {"static": StaticViewSitemap}

def sitemap_xml(request):
    response = sitemap_views.sitemap(request, sitemaps=sitemaps)
    response.render()
    xml = response.content.decode("utf-8").replace("https://example.com", settings.SITE_DOMAIN)
    return HttpResponse(xml, content_type="application/xml")

urlpatterns = [
    path("admin/", admin.site.urls),

    # Публічні сторінки
    path("", main_views.home, name="home"),
    path("tariffs/", main_views.tariffs, name="tariffs"),
    path("contacts/", main_views.contacts, name="contacts"),
    path("about/", main_views.about, name="about"),
    path("why/", main_views.why, name="why"),
    path("how/", main_views.how, name="how"),
    path("documentation/", main_views.documentation, name="documentation"),
    path("consumer/", main_views.consumer, name="consumer"),
    path("contract_docs/", main_views.contract_docs, name="contract_docs"),
    path("start/", main_views.start, name="start"),
    path("complaints/", main_views.complaints, name="complaints"),
    path("documentation_overview/", main_views.documentation_overview, name="documentation_overview"),
    path("appeals/", main_views.appeals, name="appeals"),
    path("robots.txt", TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),
    path("sitemap.xml", sitemap_xml, name="sitemap"),

    # --- ЕЛЕКТРОННИЙ КАБІНЕТ ---
    path("register/", accounts_views.register_view, name="register"),
    path("login/", accounts_views.login_view, name="login"),
    path("logout/", accounts_views.logout_view, name="logout"),
    path("cabinet/", accounts_views.cabinet_view, name="cabinet"),
    path("cabinet/profile/", accounts_views.profile_view, name="profile"),

    # Контрагенти
    path("cabinet/contragents/", accounts_views.contragents_list, name="contragents"),
    path("cabinet/contragents/add/", accounts_views.edit_contragent_view, name="add_contragent"),
    path("cabinet/contragents/edit/<int:contragent_id>/", accounts_views.edit_contragent_view, name="edit_contragent"),
    path("cabinet/contragents/delete/<int:contragent_id>/", accounts_views.delete_contragent_view, name="delete_contragent"),

    # Договори
    path("cabinet/agreements/", accounts_views.agreements_list, name="agreements"),
    path("cabinet/agreements/add/", accounts_views.edit_agreement_view, name="add_agreement"),
    path("cabinet/agreements/edit/<int:agreement_id>/", accounts_views.edit_agreement_view, name="edit_agreement"),
    path("cabinet/agreements/delete/<int:agreement_id>/", accounts_views.delete_agreement_view, name="delete_agreement"),

    # Документи (перегляд клієнтом)
    path("cabinet/documents/", accounts_views.documents_list, name="documents"),
    path("cabinet/documents/upload/", accounts_views.upload_document_view, name="upload_document"),

    # Користувачі
    path("cabinet/users/", accounts_views.users_list_view, name="users_list"),
    path("cabinet/users/add/", accounts_views.add_user_view, name="add_user"),
    path("cabinet/users/edit/<int:user_id>/", accounts_views.edit_user_view, name="edit_user"),
    path("cabinet/users/delete/<int:user_id>/", accounts_views.delete_user_view, name="delete_user"),

   # API
    path("api/auth/register/", accounts_views.api_register, name="api_register"),
    path("api/users/me/", accounts_views.api_me, name="api_me"),
    
    # ВИПРАВЛЕНО ТУТ: замість views пишемо accounts_views
    path('cabinet/documents/delete/<int:doc_id>/', accounts_views.delete_document_view, name='delete_document'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)