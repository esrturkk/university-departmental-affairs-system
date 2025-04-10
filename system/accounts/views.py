from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.contrib.auth import login
from .models import CustomUser, Role
from .forms import StaffForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.hashers import make_password

# Create your views here.

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        login_type = self.request.GET.get('type', 'academic')
        login_type_mapping = {
            'academic': 'Akademik',
            'administrative': 'İdari'
        }
        
        context['login_type'] = login_type_mapping.get(login_type)
        return context

    def form_valid(self, form):
        user = form.get_user()

        login_type = self.request.GET.get('type', 'academic')
        login_type_mapping = {
            'academic': 'Akademik',
            'administrative': 'İdari'
        }

        role_type = user.role.type if user.role else None

        if login_type_mapping.get(login_type) != role_type:
            messages.error(self.request, 'Giriş tipi ile rolünüz uyuşmuyor.')
            return self.form_invalid(form)

        login(self.request, user)
        return super().form_valid(form)

class AuthorizationRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        user = self.request.user
        return (
            user.is_authenticated and 
            hasattr(user, 'role') and 
            user.role and 
            user.role.title in ['Bölüm Başkanı', 'Bölüm Sekreteri']
        )

    def handle_no_permission(self):
        user = self.request.user

        if not user.is_authenticated:
            return redirect('home')

        if hasattr(user, 'role') and user.role and user.role.title == 'Öğretim Elemanı':
            return redirect('dashboard')

class StaffListView(AuthorizationRequiredMixin, ListView):
    model = CustomUser
    template_name = 'staff.html'
    context_object_name = 'users'

class StaffDetailView(DetailView):
    model = CustomUser
    template_name = 'staff_detail.html'
    context_object_name = 'user'

class StaffCreateView(AuthorizationRequiredMixin, CreateView):
    model = CustomUser
    template_name = 'staff_new.html'
    context_object_name = 'users'
    form_class = StaffForm

    def get_form(self, form_class=None):
        form = super().get_form(form_class)

        if self.request.user.role.title != 'Bölüm Başkanı':
            form.fields['role'].disabled = True
            form.fields['role'].initial = Role.objects.get(title='Öğretim Elemanı')

        return form

    def form_valid(self, form):
        user = form.save(commit=False)
        user.save()
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('staff')

class StaffUpdateView(AuthorizationRequiredMixin, UpdateView):
    model = CustomUser
    template_name = 'staff_edit.html'
    context_object_name = 'users'
    form_class = StaffForm

    def get_form(self, form_class=None):
        form = super().get_form(form_class)

        if self.request.user.role.title != 'Bölüm Başkanı':
            form.fields['role'].disabled = True

        return form

    def form_valid(self, form):
        user = form.save(commit=False)
        user.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('staff')

class StaffDeleteView(AuthorizationRequiredMixin, DeleteView):
    model = CustomUser
    template_name = 'staff_delete.html'
    context_object_name = 'users'
    success_url = reverse_lazy('staff')

    def dispatch(self, request, *args, **kwargs):
        if not self.test_func():
            return self.handle_no_permission()

        if request.user.role.title != 'Bölüm Başkanı':
            return redirect('dashboard')

        return super().dispatch(request, *args, **kwargs)
