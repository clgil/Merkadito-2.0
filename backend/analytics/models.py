from django.db import models


class ClickWhatsApp(models.Model):
    """Registro de clicks a WhatsApp - Analítica ligera"""
    empresa = models.ForeignKey('businesses.Empresa', on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    ip = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.CharField(max_length=500, blank=True)
    
    class Meta:
        ordering = ['-fecha']
        indexes = [
            models.Index(fields=['empresa', 'fecha']),
        ]
    
    def __str__(self):
        return f'{self.empresa.nombre} - {self.fecha}'


class VistaEmpresa(models.Model):
    """Registro de vistas a empresa - Analítica ligera"""
    empresa = models.ForeignKey('businesses.Empresa', on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    ip = models.GenericIPAddressField(blank=True, null=True)
    
    class Meta:
        ordering = ['-fecha']
        indexes = [
            models.Index(fields=['empresa', 'fecha']),
        ]


class VistaProducto(models.Model):
    """Registro de vistas a producto - Analítica ligera"""
    producto = models.ForeignKey('products.Producto', on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    ip = models.GenericIPAddressField(blank=True, null=True)
    
    class Meta:
        ordering = ['-fecha']
        indexes = [
            models.Index(fields=['producto', 'fecha']),
        ]