from django.contrib import admin
from django.urls import path
from main import views as main_views
from accounts import views as accounts_views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.views.generic import TemplateView


urlpatterns = [
    path('admin/', admin.site.urls),

    # Публічні сторінки
    
    path('', main_views.home, name='home'),
    path('tariffs/', main_views.tariffs, name='tariffs'),
    path('contacts/', main_views.contacts, name='contacts'),
    path('about/', main_views.about, name='about'),
    path('why/', main_views.why, name='why'),
     path('how/', main_views.how, name='how'),
     path('documentation/', main_views.documentation, name='documentation'),
     path('consumer/', main_views.consumer, name='consumer'),
     path('contract_docs/', main_views.contract_docs, name='contract_docs'),
     path('start/', main_views.start, name='start'),
     path('complaints/', main_views.complaints, name='complaints'),
     path('documentation_overview/', main_views.documentation_overview, name='documentation_overview'),
     path('appeals/', main_views.appeals, name='appeals'),
     path('robots.txt', TemplateView.as_view(
        template_name="robots.txt",
        content_type="text/plain"
    )),








    # Авторизація/акаунт
    path('register/', accounts_views.register, name='register'),
    path('login/', accounts_views.login_view, name='login'),
    path('logout/', accounts_views.logout_view, name='logout'),
    path('profile/', accounts_views.profile, name='profile'),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
