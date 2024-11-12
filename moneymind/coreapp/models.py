from django.db import models
from django.core.validators import RegexValidator

# This is the model for the user's profile and persons
class GenderIdentity(models.Model):
    """Clase que representa la identidad de género de un usuario."""
    id_genders = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True, verbose_name='Identidad de género')

    class Meta:
        db_table = 'genders'
        verbose_name = 'Identidad de género'
        verbose_name_plural = 'Identidades de género'

    def __str__(self):
        return self.name
    
class MaritalStatus(models.Model):
    """Clase que representa el estado civil de una persona."""
    id_marital_statuses = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True, verbose_name='Estado civil')

    class Meta:
        db_table = 'marital_statuses'
        verbose_name = 'Estado civil'
        verbose_name_plural = 'Estados civiles'

    def __str__(self):
        return self.name
    
class Typesdocs(models.Model):
    """Clase que representa el tipo de documento de identificación de una persona"""
    id_typedoc = models.CharField(verbose_name = 'Código del tipo de documento', max_length=2, primary_key=True)
    doc_type = models.CharField(verbose_name = 'Descripción', max_length=100, unique = True, null = False)

    class Meta:
        db_table = 'typesdocs'
        verbose_name = 'Tipo de documento'
        verbose_name_plural = 'Tipos de documentos'

    def __str__(self):
        return f'{self.id_typedoc} - {self.doc_type}'
    
class Country(models.Model):
    """Clase que representa un país."""
    id_code = models.CharField(max_length=2, primary_key=True, verbose_name='Código del país')
    name = models.CharField(max_length=100, verbose_name='Nombre del país')
    phone_code = models.CharField(max_length=10, verbose_name='Código telefónico')
    flag = models.URLField(max_length=200, null=True, verbose_name='URL de la bandera')
    
    class Meta:
        db_table = 'countries'
        verbose_name_plural = "countries"

    def __str__(self):
        return self.name
    
class Person(models.Model):
    """Clase que representa una persona"""
    SEX_BIO = [
        ('01', 'Hombre'),
        ('02', 'Mujer'),
        ('03', 'Indeterminado intersexual'),
    ]
    EMAIL_TYPES = [
        ('01', 'gmail'),
        ('02', 'hotmail'),
        ('03', 'yahoo'),
        ('04', 'outlook'),
        ('05', 'icloud'),
    ]
    id_person = models.AutoField(primary_key=True, verbose_name='Identificador de persona')
    name = models.CharField(max_length=40, verbose_name='Nombre de persona')
    surname = models.CharField(max_length=40, verbose_name='Apellido de persona')
    type_email = models.CharField(max_length=2, choices=EMAIL_TYPES, default='01', verbose_name='Tipo de correo electrónico')
    email = models.EmailField(max_length=100, unique=True, verbose_name='Correo electrónico')
    country = models.ForeignKey(Country, on_delete=models.CASCADE, verbose_name='País')
    birthdate = models.DateField(verbose_name='Fecha de nacimiento')
    marital_status = models.ForeignKey(MaritalStatus, on_delete=models.CASCADE, verbose_name='Estado civil')
    type_doc = models.ForeignKey(Typesdocs, on_delete=models.CASCADE, verbose_name='Tipo de documento')
    doc_number = models.CharField(max_length=20, validators=[RegexValidator(regex='^[0-9]*$', message='Solo se permiten números')], unique=True, verbose_name='Número de documento')
    phone_number = models.CharField(max_length=20, validators=[RegexValidator(regex='^[0-9]*$', message='Solo se permiten números')], verbose_name='Número de teléfono')
    address = models.CharField(max_length=100, verbose_name='Dirección')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de actualización')

    class Meta:
        db_table = 'persons'
        verbose_name = 'Persona'
        verbose_name_plural = 'Personas'

    def __str__(self):
        return f'{self.name} {self.surname}'
    
class UserProfile(models.Model):
    """Clase que representa el perfil de un usuario."""
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE, verbose_name='Usuario')
    person = models.OneToOneField(Person, on_delete=models.CASCADE, verbose_name='Persona')
    is_active = models.BooleanField(default=True, verbose_name='Activo')
    is_staff = models.BooleanField(default=False, verbose_name='Staff')

    class Meta:
        db_table = 'user_profiles'
        verbose_name = 'Perfil de usuario'
        verbose_name_plural = 'Perfiles de usuario'
    
    def __str__(self):
        return self.user.username