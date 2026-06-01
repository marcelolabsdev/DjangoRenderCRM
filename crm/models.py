from django.db import models


class Empresa(models.Model):
    nombre = models.CharField(max_length=200)
    sector = models.CharField(max_length=100, blank=True)
    sitio_web = models.URLField(blank=True)
    direccion = models.TextField(blank=True)

    class Meta:
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class Contacto(models.Model):
    ESTADO_CHOICES = [
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
        ('lead', 'Lead'),
    ]

    nombre = models.CharField(max_length=200)
    email = models.EmailField()
    telefono = models.CharField(max_length=50, blank=True)
    empresa = models.ForeignKey(Empresa, on_delete=models.SET_NULL, null=True, blank=True, related_name='contactos')
    notas = models.TextField(blank=True)
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='lead')
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-fecha_creacion']

    def __str__(self):
        return f"{self.nombre} ({self.get_estado_display()})"


class Oportunidad(models.Model):
    ETAPA_CHOICES = [
        ('prospecto', 'Prospecto'),
        ('cualificado', 'Cualificado'),
        ('propuesta', 'Propuesta'),
        ('cerrado_ganado', 'Cerrado Ganado'),
        ('cerrado_perdido', 'Cerrado Perdido'),
    ]

    titulo = models.CharField(max_length=200)
    valor = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    etapa = models.CharField(max_length=20, choices=ETAPA_CHOICES, default='prospecto')
    contacto = models.ForeignKey(Contacto, on_delete=models.CASCADE, related_name='oportunidades')
    empresa = models.ForeignKey(Empresa, on_delete=models.SET_NULL, null=True, blank=True, related_name='oportunidades')
    fecha_cierre_estimada = models.DateField(null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-fecha_creacion']
        verbose_name_plural = 'oportunidades'

    def __str__(self):
        return f"{self.titulo} - {self.get_etapa_display()}"


class Actividad(models.Model):
    TIPO_CHOICES = [
        ('llamada', 'Llamada'),
        ('email', 'Email'),
        ('reunion', 'Reunion'),
        ('nota', 'Nota'),
    ]

    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES, default='nota')
    descripcion = models.TextField()
    fecha = models.DateTimeField()
    contacto = models.ForeignKey(Contacto, on_delete=models.CASCADE, related_name='actividades')

    class Meta:
        ordering = ['-fecha']

    def __str__(self):
        return f"{self.get_tipo_display()} - {self.contacto.nombre}"
