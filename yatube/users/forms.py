from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


User = get_user_model()


class CreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('photo', 'first_name', 'last_name', 'username', 'email',
                  'phone', 'about', )

    def clean_username(self):
        username = self.cleaned_data['username']

        try:
            self.Meta.model.objects.get(username=username)
        except self.Meta.model.DoesNotExist:
            return username

        raise forms.ValidationError(
            self.error_messages['duplicate_username'],
            code='duplicate_username',
        )
