from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from tasks.views import TaskViewSet

# DRF Router'ду орнотуу
router = DefaultRouter()
router.register(r'tasks', TaskViewSet)

urlpatterns = [
    # 1. Административдик панель
    path('admin/', admin.site.urls),

    # 2. ⭐ АУТЕНТИФИКАЦИЯ ЖАНА АВТОРИЗАЦИЯ URL'ДЕРИ (Login/Logout/Password Reset)
    # Бул мурунку 404 катасын чечет.
    path('accounts/', include('django.contrib.auth.urls')),

    # 3. КАНБАН ЖАНА ПРОФИЛЬ (Tasks/Profile/Teams) URL'ДЕРИ
    path('', include('tasks.urls')),

    # 4. REST API ЭНДПОЙНТТАРЫ (/api/tasks/)
    path('api/', include(router.urls)),

    # 5. API ДОКУМЕНТАЦИЯСЫ (Swagger UI)
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]