"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('management/', admin.site.urls),
    path('', include('home.urls')),
    path('', include('apps.course.urls')),
    path('', include('account.urls')),
    path('', include('apps.membership.urls')),
    path('', include('user_sessions.urls', 'user_sessions')),
    path('', include('apps.chat.urls')),
    path('', include('apps.data.urls')),
    path('payment/', include('apps.payment.urls')),
    path('admin/', include('dashboard.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
