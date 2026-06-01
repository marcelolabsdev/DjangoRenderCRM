from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('contactos/', views.contacto_list, name='contacto_list'),
    path('contactos/nuevo/', views.contacto_create, name='contacto_create'),
    path('contactos/<int:pk>/', views.contacto_detail, name='contacto_detail'),
    path('contactos/<int:pk>/editar/', views.contacto_edit, name='contacto_edit'),
    path('contactos/<int:pk>/eliminar/', views.contacto_delete, name='contacto_delete'),
    path('oportunidades/', views.oportunidad_list, name='oportunidad_list'),
    path('oportunidades/nuevo/', views.oportunidad_create, name='oportunidad_create'),
    path('oportunidades/<int:pk>/editar/', views.oportunidad_edit, name='oportunidad_edit'),
    path('empresas/', views.empresa_list, name='empresa_list'),
    path('empresas/nuevo/', views.empresa_create, name='empresa_create'),
    path('empresas/<int:pk>/editar/', views.empresa_edit, name='empresa_edit'),
]
