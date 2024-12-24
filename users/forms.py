# users/forms.py
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    # is_admin = forms.BooleanField(required=False, initial=False, label="Is Admin",
    #                               widget=forms.CheckboxInput(attrs={'class': 'reg-checkbox'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class EditUserForm(forms.ModelForm):
    old_password = forms.CharField(widget=forms.PasswordInput, label="Old Password")
    new_password1 = forms.CharField(widget=forms.PasswordInput, label="New Password", help_text=( "<ul>"
            "<li>Your password can’t be too similar to your other personal information.</li>"
            "<li>Your password must contain at least 8 characters.</li>"
            "<li>Your password can’t be a commonly used password.</li>"
            "<li>Your password can’t be entirely numeric.</li>"
            "</ul>"))
    new_password2 = forms.CharField(widget=forms.PasswordInput, label="New Password confirmation", help_text= "Enter the same password as before, for verification.")

    class Meta:
        model = User
        fields = ['username']  # Позволяет редактировать никнейм

    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')
        if not self.instance.check_password(old_password):
            raise forms.ValidationError("Old password does not match")
        return old_password

    def clean(self):
        cleaned_data = super().clean()
        new_password1 = cleaned_data.get("new_password1")
        new_password2 = cleaned_data.get("new_password2")
        if new_password1 and new_password2 and new_password1 != new_password2:
            self.add_error("new_password2", "New password does not match")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        new_password = self.cleaned_data.get("new_password1")
        if new_password:
            user.set_password(new_password)
        if commit:
            user.save()
        return user