from django.shortcuts import redirect
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include('ferramentas.hub.urls', namespace='hub')),
    path('retencao_alunos/', include('ferramentas.retencao_alunos.urls', namespace='retencao_alunos')),
    path('atividades_complementares/', include('ferramentas.aacc_app.urls', namespace='aacc_app')),
    path('ferramenta_graduacao_si/', include('ferramentas.ferramenta_graduacao_si.table.urls', namespace='ferramenta_graduacao_si')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) 