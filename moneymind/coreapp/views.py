from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic import CreateView, UpdateView, DetailView, TemplateView
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from .models import UserProfile, Person
from .forms import CustomUserCreationForm, PersonForm
from django.contrib.auth.models import User

# Create your views here.
class HomeView(TemplateView):
    template_name = 'index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'MoneyMind'
        return context
    
class CustomLoginView(LoginView):
    """Vista personalizada para el login"""
    template_name = 'registration/login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('dashboard')

class RegisterView(SuccessMessageMixin, CreateView):
    """Vista para el registro de usuarios"""
    template_name = 'registration/register.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('dashboard')
    success_message = "¡Registro exitoso!"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'person_form' not in context:
            context['person_form'] = PersonForm()
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        person_form = PersonForm(request.POST)
        
        if form.is_valid() and person_form.is_valid():
            return self.form_valid(form, person_form)
        else:
            return self.form_invalid(form, person_form)

    def form_valid(self, form, person_form):
        user = form.save()
        person = person_form.save()
        
        UserProfile.objects.create(
            user=user,
            person=person,
            is_active=True
        )
        
        from django.contrib.auth import login
        login(self.request, user)
        
        return redirect(self.success_url)

    def form_invalid(self, form, person_form):
        return self.render_to_response(
            self.get_context_data(
                form=form,
                person_form=person_form
            )
        )

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard')
        return super().dispatch(request, *args, **kwargs)

class DashboardView(LoginRequiredMixin, TemplateView):
    """Vista del dashboard para usuarios autenticados"""
    template_name = 'dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_profile'] = self.request.user.userprofile
        return context

class ProfileDetailView(LoginRequiredMixin, DetailView):
    """Vista para ver el perfil del usuario"""
    model = UserProfile
    template_name = 'profile/detail.html'
    context_object_name = 'user_profile'
    
    def get_object(self):
        return self.request.user.userprofile

class ProfileUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """Vista para actualizar el perfil del usuario"""
    model = Person
    form_class = PersonForm
    template_name = 'profile/update.html'
    success_message = "Perfil actualizado exitosamente"
    
    def get_object(self):
        return self.request.user.userprofile.person
    
    def get_success_url(self):
        return reverse_lazy('profile-detail')