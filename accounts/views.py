from accounts.forms import LJUserCreationForm
from django.urls import reverse_lazy
from django.views import generic

class SignUpView(generic.CreateView):
    form_class = LJUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'