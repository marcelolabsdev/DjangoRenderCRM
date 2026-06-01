from django import forms
from .models import Empresa, Contacto, Oportunidad, Actividad


class EmpresaForm(forms.ModelForm):
    class Meta:
        model = Empresa
        fields = ['nombre', 'sector', 'sitio_web', 'direccion']
        widgets = {
            'direccion': forms.Textarea(attrs={'rows': 3}),
        }


class ContactoForm(forms.ModelForm):
    class Meta:
        model = Contacto
        fields = ['nombre', 'email', 'telefono', 'empresa', 'notas', 'estado']
        widgets = {
            'notas': forms.Textarea(attrs={'rows': 3}),
        }


class OportunidadForm(forms.ModelForm):
    class Meta:
        model = Oportunidad
        fields = ['titulo', 'valor', 'etapa', 'contacto', 'empresa', 'fecha_cierre_estimada']
        widgets = {
            'fecha_cierre_estimada': forms.DateInput(attrs={'type': 'date'}),
        }


class ActividadForm(forms.ModelForm):
    class Meta:
        model = Actividad
        fields = ['tipo', 'descripcion', 'fecha', 'contacto']
        widgets = {
            'fecha': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'descripcion': forms.Textarea(attrs={'rows': 3}),
        }
