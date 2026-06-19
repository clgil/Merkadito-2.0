from django.db import models
from django.utils.text import slugify


class Categoria(models.Model):
    """Categorías de negocios/productos - Ultraligero"""
    nombre = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    icono = models.CharField(max_length=50, blank=True, help_text='Nombre del icono Lucide')
    
    class Meta:
        verbose_name_plural = 'Categorías'
        ordering = ['nombre']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nombre)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.nombre


class Provincia(models.Model):
    """Provincias de Cuba"""
    nombre = models.CharField(max_length=100, unique=True)
    
    class Meta:
        ordering = ['nombre']
    
    def __str__(self):
        return self.nombre


class Municipio(models.Model):
    """Municipios de Cuba"""
    provincia = models.ForeignKey(Provincia, on_delete=models.CASCADE, related_name='municipios')
    nombre = models.CharField(max_length=100)
    latitud = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True, help_text='Latitud aproximada del municipio')
    longitud = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True, help_text='Longitud aproximada del municipio')
    
    class Meta:
        unique_together = ['provincia', 'nombre']
        ordering = ['nombre']
    
    def __str__(self):
        return f'{self.nombre}, {self.provincia}'


class ConsejoPopular(models.Model):
    """Consejos Populares de Cuba - División administrativa intermedia"""
    municipio = models.ForeignKey(Municipio, on_delete=models.CASCADE, related_name='consejos_populares')
    nombre = models.CharField(max_length=100)
    codigo = models.CharField(max_length=20, blank=True, help_text='Código identificador')
    
    class Meta:
        unique_together = ['municipio', 'nombre']
        ordering = ['nombre']
        verbose_name = 'Consejo Popular'
        verbose_name_plural = 'Consejos Populares'
    
    def __str__(self):
        return f'{self.nombre}, {self.municipio}'


class Barrio(models.Model):
    """Barrios/Zonas de Cuba - Nivel más granular para geolocalización"""
    consejo_popular = models.ForeignKey(ConsejoPopular, on_delete=models.CASCADE, related_name='barrios', null=True, blank=True)
    municipio = models.ForeignKey(Municipio, on_delete=models.CASCADE, related_name='barrios')
    nombre = models.CharField(max_length=100)
    latitud = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True, help_text='Latitud aproximada del barrio')
    longitud = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True, help_text='Longitud aproximada del barrio')
    referencia = models.TextField(max_length=300, blank=True, help_text='Puntos de referencia cercanos')
    
    class Meta:
        unique_together = ['municipio', 'nombre']
        ordering = ['nombre']
        indexes = [
            models.Index(fields=['municipio']),
            models.Index(fields=['consejo_popular']),
        ]
    
    def __str__(self):
        return f'{self.nombre}, {self.municipio}'


class Empresa(models.Model):
    """
    Empresa/Negocio - Modelo simplificado para Cuba
    Máximo 10 campos esenciales
    """
    nombre = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    descripcion = models.TextField(max_length=500, blank=True)
    
    # Contacto
    whatsapp = models.CharField(max_length=20, help_text='Número WhatsApp con código país')
    telefono = models.CharField(max_length=20, blank=True)
    
    # Ubicación geográfica cubana
    provincia = models.ForeignKey(Provincia, on_delete=models.SET_NULL, null=True)
    municipio = models.ForeignKey(Municipio, on_delete=models.SET_NULL, null=True)
    consejo_popular = models.ForeignKey(ConsejoPopular, on_delete=models.SET_NULL, null=True, blank=True)
    barrio = models.ForeignKey(Barrio, on_delete=models.SET_NULL, null=True, blank=True)
    direccion = models.CharField(max_length=300, blank=True)
    latitud = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True, help_text='Latitud exacta del negocio')
    longitud = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True, help_text='Longitud exacta del negocio')
    
    # Categoría
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, related_name='empresas')
    
    # Multimedia (optimizada)
    logo = models.ImageField(upload_to='logos/', blank=True, null=True, help_text='Max 1MB, WebP recomendado')
    
    # Estado
    activo = models.BooleanField(default=True)
    verificado = models.BooleanField(default=False)
    
    # Timestamps
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-creado_en']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['provincia', 'municipio']),
            models.Index(fields=['categoria']),
            models.Index(fields=['activo']),
        ]
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.nombre)
            slug = base_slug
            counter = 1
            while Empresa.objects.filter(slug=slug).exists():
                slug = f'{base_slug}-{counter}'
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.nombre
    
    def get_whatsapp_link(self):
        """Genera link directo a WhatsApp"""
        numero_limpio = self.whatsapp.replace('+', '').replace(' ', '').replace('-', '')
        return f'https://wa.me/{numero_limpio}'
