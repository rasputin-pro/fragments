from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import CreationForm


class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy('posts:index')
    template_name = 'users/signup.html'

    def form_valid(self, form):
        """ Automatically sign-in the user. """
        super(SignUp, self).form_valid(form)
        user = authenticate(
            self.request,
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password1'])
        if user is None:
            return self.render_to_response(
                self.get_context_data(form=form))
        login(self.request, user)
        return redirect(self.get_success_url())
