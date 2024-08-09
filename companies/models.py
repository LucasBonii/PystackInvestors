from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Company(models.Model):
    existence_time_choices = (
        ('-6', 'Menos de 6 meses'),
        ('+6', 'Mais de 6 meses'),
        ('+1', 'Mais de 1 ano'),
        ('+5', 'Mais de 5 anos')
        
    )
    phase_choices = (
        ('I', 'Tenho apenas uma idea'),
        ('MVP', 'Possuo um MVP'),
        ('MVPP', 'Possuo um MVP com clientes pagantes'),
        ('E', 'Empresa pronta para escalar'),
    )
    area_choices = (
        ('ED', 'Ed-tech'),
        ('FT', 'Fintech'),
        ('AT', 'Agrotech'),
        
    )
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=50)
    cnpj = models.CharField(max_length=30)
    site = models.URLField()
    existence_time = models.CharField(max_length=2, choices=existence_time_choices, default='-6')
    description = models.TextField() 
    end_of_capture = models.DateField()
    percentual_equity = models.IntegerField() # Percentual esperado
    phase = models.CharField(max_length=4, choices=phase_choices, default='I')
    area = models.CharField(max_length=3, choices=area_choices)
    target_audience = models.CharField(max_length=3)
    value = models.DecimalField(max_digits=9, decimal_places=2) # Valor total a ser vendido
    pitch = models.FileField(upload_to='pitchs')
    logo = models.FileField(upload_to='logo')

    def __str__(self):
        return f'{self.user.username} | {self.name}'
    