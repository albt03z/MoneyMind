from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Person, UserProfile
from django.core.validators import RegexValidator, EmailValidator

class PersonForm(forms.ModelForm):
    """Formulario para los datos personales"""
    class Meta:
        model = Person
        fields = [
            'name', 'surname', 'type_email', 'email', 'country',
            'birthdate', 'marital_status', 'type_doc', 'doc_number',
            'phone_number', 'address'
        ]
        widgets = {
            'birthdate': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'surname': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'doc_number': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_doc_number(self):
        doc_number = self.cleaned_data.get('doc_number')
        if not doc_number.isdigit():
            raise forms.ValidationError('El número de documento solo puede contener números')
        return doc_number
    
    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if not phone_number.isdigit():
            raise forms.ValidationError('El número de teléfono solo puede contener números')
        return phone_number
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Person.objects.filter(email=email).exists():
            raise forms.ValidationError('Ya existe una persona con este correo electrónico')
        return email
    
    def emailvalidator(self):
        email = self.cleaned_data.get('email')
        if not EmailValidator(email):
            raise forms.ValidationError('El correo electrónico no es válido')
        return email
    
    def clean_doc_number(self):
        doc_number = self.cleaned_data.get('doc_number')
        if Person.objects.filter(doc_number=doc_number).exists():
            raise forms.ValidationError('Ya existe una persona con este número de documento')
        return doc_number
    
class CustomUserCreationForm(UserCreationForm):
    """Formulario personalizado para la creación de usuarios"""
    password1 = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput,
        help_text="""
        Tu contraseña debe cumplir con:
        • Al menos 8 caracteres
        • No puede ser similar a tu información personal
        • Debe contener al menos una letra mayúscula
        • Debe contener al menos un número
        • Debe contener al menos un carácter especial
        """
    )
    password2 = forms.CharField(
        label='Confirmar contraseña',
        widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        if len(password) < 8:
            raise forms.ValidationError('La contraseña debe tener al menos 8 caracteres')
        if not any(char.isupper() for char in password):
            raise forms.ValidationError('La contraseña debe contener al menos una mayúscula')
        if not any(char.isdigit() for char in password):
            raise forms.ValidationError('La contraseña debe contener al menos un número')
        if not any(char in '!@#$%^&*()' for char in password):
            raise forms.ValidationError('La contraseña debe contener al menos un carácter especial')
        return password
    
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 != password2:
            raise forms.ValidationError('Las contraseñas no coinciden')
        return password2
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Ya existe un usuario con este nombre de usuario')
        return username
    
class CustomUserUpdateForm(forms.ModelForm):
    """Formulario personalizado para la actualización de usuarios"""
    class Meta:
        model = User
        fields = ('username', 'email')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Ya existe un usuario con este nombre de usuario')
        return username
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Ya existe un usuario con este correo electrónico')
        return email
    
class CustomUserPasswordForm(forms.ModelForm):
    """Formulario personalizado para la actualización de la contraseña de un usuario"""
    password1 = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput,
        help_text="""
        Tu contraseña debe cumplir con:
        • Al menos 8 caracteres
        • No puede ser similar a tu información personal
        • Debe contener al menos una letra mayúscula
        • Debe contener al menos un número
        • Debe contener al menos un carácter especial
        """
    )
    password2 = forms.CharField(
        label='Confirmar contraseña',
        widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ('password1', 'password2')

    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        if len(password) < 8:
            raise forms.ValidationError('La contraseña debe tener al menos 8 caracteres')
        if not any(char.isupper() for char in password):
            raise forms.ValidationError('La contraseña debe contener al menos una mayúscula')
        if not any(char.isdigit() for char in password):
            raise forms.ValidationError('La contraseña debe contener al menos un número')
        if not any(char in '!@#$%^&*()' for char in password):
            raise forms.ValidationError('La contraseña debe contener al menos un carácter especial')
        return password
    
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 != password2:
            raise forms.ValidationError('Las contraseñas no coinciden')
        return password2
    
class loginForm(forms.Form):
    """Formulario para el inicio de sesión"""
    username = forms.CharField(
        label='Nombre de usuario',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError('El usuario no existe')
        return username
    
    def verify_credentials(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = User.objects.get(username=username)
        if not user.check_password(password):
            raise forms.ValidationError('Usuario o contraseña son incorrecta')
        return password
    
    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        user = UserProfile.objects.get(username=username)
        if user.is_active == False:
            raise forms.ValidationError('El usuario está inactivo')
        return cleaned_data