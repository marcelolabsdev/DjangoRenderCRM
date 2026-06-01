from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count, Q
from django.contrib import messages
from .models import Empresa, Contacto, Oportunidad, Actividad
from .forms import EmpresaForm, ContactoForm, OportunidadForm, ActividadForm


@login_required
def dashboard(request):
    total_contactos = Contacto.objects.count()
    contactos_activos = Contacto.objects.filter(estado='activo').count()
    total_oportunidades = Oportunidad.objects.exclude(etapa__in=['cerrado_ganado', 'cerrado_perdido']).count()
    valor_pipeline = Oportunidad.objects.exclude(etapa__in=['cerrado_ganado', 'cerrado_perdido']).aggregate(total=Sum('valor'))['total'] or 0
    ganado = Oportunidad.objects.filter(etapa='cerrado_ganado').aggregate(total=Sum('valor'))['total'] or 0
    oportunidades_recientes = Oportunidad.objects.select_related('contacto', 'empresa')[:5]
    actividades_recientes = Actividad.objects.select_related('contacto')[:5]

    oportunidades_por_etapa = Oportunidad.objects.values('etapa').annotate(
        cantidad=Count('id'),
        valor_total=Sum('valor')
    ).order_by('etapa')

    context = {
        'total_contactos': total_contactos,
        'contactos_activos': contactos_activos,
        'total_oportunidades': total_oportunidades,
        'valor_pipeline': valor_pipeline,
        'ganado': ganado,
        'oportunidades_recientes': oportunidades_recientes,
        'actividades_recientes': actividades_recientes,
        'oportunidades_por_etapa': oportunidades_por_etapa,
    }
    return render(request, 'crm/dashboard.html', context)


@login_required
def contacto_list(request):
    queryset = Contacto.objects.select_related('empresa')
    estado = request.GET.get('estado')
    buscar = request.GET.get('q')
    if estado:
        queryset = queryset.filter(estado=estado)
    if buscar:
        queryset = queryset.filter(Q(nombre__icontains=buscar) | Q(email__icontains=buscar))
    context = {'contactos': queryset, 'estado_actual': estado, 'buscar': buscar}
    return render(request, 'crm/contacto_list.html', context)


@login_required
def contacto_create(request):
    if request.method == 'POST':
        form = ContactoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Contacto creado exitosamente.')
            return redirect('contacto_list')
    else:
        form = ContactoForm()
    return render(request, 'crm/contacto_form.html', {'form': form, 'titulo': 'Nuevo Contacto'})


@login_required
def contacto_detail(request, pk):
    contacto = get_object_or_404(Contacto, pk=pk)
    actividades = contacto.actividades.all()
    oportunidades = contacto.oportunidades.select_related('empresa')
    if request.method == 'POST':
        actividad_form = ActividadForm(request.POST)
        if actividad_form.is_valid():
            actividad = actividad_form.save(commit=False)
            actividad.contacto = contacto
            actividad.save()
            messages.success(request, 'Actividad agregada.')
            return redirect('contacto_detail', pk=pk)
    else:
        actividad_form = ActividadForm()
    context = {
        'contacto': contacto,
        'actividades': actividades,
        'oportunidades': oportunidades,
        'actividad_form': actividad_form,
    }
    return render(request, 'crm/contacto_detail.html', context)


@login_required
def contacto_edit(request, pk):
    contacto = get_object_or_404(Contacto, pk=pk)
    if request.method == 'POST':
        form = ContactoForm(request.POST, instance=contacto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Contacto actualizado.')
            return redirect('contacto_detail', pk=pk)
    else:
        form = ContactoForm(instance=contacto)
    return render(request, 'crm/contacto_form.html', {'form': form, 'titulo': 'Editar Contacto'})


@login_required
def contacto_delete(request, pk):
    contacto = get_object_or_404(Contacto, pk=pk)
    if request.method == 'POST':
        contacto.delete()
        messages.success(request, 'Contacto eliminado.')
        return redirect('contacto_list')
    return render(request, 'crm/contacto_confirm_delete.html', {'contacto': contacto})


@login_required
def oportunidad_list(request):
    queryset = Oportunidad.objects.select_related('contacto', 'empresa')
    etapa = request.GET.get('etapa')
    if etapa:
        queryset = queryset.filter(etapa=etapa)
    context = {'oportunidades': queryset, 'etapa_actual': etapa}
    return render(request, 'crm/oportunidad_list.html', context)


@login_required
def oportunidad_create(request):
    if request.method == 'POST':
        form = OportunidadForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Oportunidad creada exitosamente.')
            return redirect('oportunidad_list')
    else:
        form = OportunidadForm()
    return render(request, 'crm/oportunidad_form.html', {'form': form, 'titulo': 'Nueva Oportunidad'})


@login_required
def oportunidad_edit(request, pk):
    oportunidad = get_object_or_404(Oportunidad, pk=pk)
    if request.method == 'POST':
        form = OportunidadForm(request.POST, instance=oportunidad)
        if form.is_valid():
            form.save()
            messages.success(request, 'Oportunidad actualizada.')
            return redirect('oportunidad_list')
    else:
        form = OportunidadForm(instance=oportunidad)
    return render(request, 'crm/oportunidad_form.html', {'form': form, 'titulo': 'Editar Oportunidad'})


@login_required
def empresa_list(request):
    empresas = Empresa.objects.annotate(num_contactos=Count('contactos')).order_by('nombre')
    return render(request, 'crm/empresa_list.html', {'empresas': empresas})


@login_required
def empresa_create(request):
    if request.method == 'POST':
        form = EmpresaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Empresa creada exitosamente.')
            return redirect('empresa_list')
    else:
        form = EmpresaForm()
    return render(request, 'crm/empresa_form.html', {'form': form, 'titulo': 'Nueva Empresa'})


@login_required
def empresa_edit(request, pk):
    empresa = get_object_or_404(Empresa, pk=pk)
    if request.method == 'POST':
        form = EmpresaForm(request.POST, instance=empresa)
        if form.is_valid():
            form.save()
            messages.success(request, 'Empresa actualizada.')
            return redirect('empresa_list')
    else:
        form = EmpresaForm(instance=empresa)
    return render(request, 'crm/empresa_form.html', {'form': form, 'titulo': 'Editar Empresa'})
