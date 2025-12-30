from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

from main import views as main_views
from accounts import views as accounts_views

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from accounts.views import api_register, api_me

# --- SITEMAP FIX (Render-safe, без Sites адмінки) ---
from django.http import HttpResponse
from django.contrib.sitemaps import views as sitemap_views
from main.sitemaps import StaticViewSitemap

sitemaps = {
    "static": StaticViewSitemap,
}

def sitemap_xml(request):
    response = sitemap_views.sitemap(request, sitemaps=sitemaps)
    response.render()

    xml = response.content.decode("utf-8")
    xml = xml.replace("https://example.com", settings.SITE_DOMAIN)

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

    # ✅ Кабінет (React SPA)
    path("cabinet/", main_views.cabinet, name="cabinet"),
    path("cabinet/<path:path>", main_views.cabinet),  # для /cabinet/login, /cabinet/register, etc.

    # robots + sitemap
    path("robots.txt", TemplateView.as_view(
        template_name="robots.txt",
        content_type="text/plain"
    )),
    path("sitemap.xml", sitemap_xml, name="sitemap"),

    # API auth
    path("api/auth/login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/auth/register/", api_register),
    path("api/users/me/", api_me),

    # Авторизація/акаунт (старі django сторінки — можеш лишити)
    path("register/", accounts_views.register, name="register"),
    path("login/", accounts_views.login_view, name="login"),
    path("logout/", accounts_views.logout_view, name="logout"),
    path("profile/", accounts_views.profile, name="profile"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
