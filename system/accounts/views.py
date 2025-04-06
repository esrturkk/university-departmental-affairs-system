from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.http import HttpResponseRedirect

# Create your views here.

class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('home')
    template_name = 'registration/signup.html'

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

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
            return HttpResponseRedirect(self.request.path_info)

        return super().form_valid(form)
