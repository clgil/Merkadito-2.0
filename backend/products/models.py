from django.db import models
from businesses.models import Empresa


class Producto(models.Model):
    """
    Producto - Modelo ultraligero para Cuba
    Máximo 10 campos esenciales
    """
    MONEDA_CHOICES = [
        ('CUP', 'CUP - Peso Cubano'),
        ('USD', 'USD - Dólar Americano'),
        ('MLC', 'MLC - Moneda Libremente Convertible'),
        ('EUR', 'EUR - Euro'),
    ]
    
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='productos')
    nombre = models.CharField(max_length=200)
    descripcion_corta = models.TextField(max_length=300, blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    moneda = models.CharField(max_length=3, choices=MONEDA_CHOICES, default='CUP')
    
    # Multimedia optimizada
    imagen = models.ImageField(
        upload_to='productos/',
        blank=True,
        null=True,
        help_text='Max 1MB, WebP recomendado'
    )
    
    categoria = models.CharField(max_length=100, blank=True, help_text='Categoría del producto')
    disponible = models.BooleanField(default=True)
    
    # Timestamps
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-creado_en']
        indexes = [
            models.Index(fields=['empresa']),
            models.Index(fields=['disponible']),
            models.Index(fields=['categoria']),
        ]
    
    def __str__(self):
        return self.nombre