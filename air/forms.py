from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

User = get_user_model()


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]

    def clean_email(self):
        """Ensure email is unique."""
        email = self.cleaned_data.get("email")
        normalized_email = email.lower()
        if User.objects.filter(email__iexact=normalized_email).exists():
            raise forms.ValidationError("Email already registered")
        return email

    def clean(self):
        """Perform complex validation logic for the form."""
        cleaned_data = super().clean()

        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        # Check that both passwords match
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords don't match")

        # Validate password strength using Django's built-in validators
        if password:
            try:
                validate_password(password)
            except ValidationError as e:
                # Add validation errors to the 'password' field
                self.add_error("password", e)

        return cleaned_data

    def save(self, commit=True):
        """Override save to handle password hashing."""
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
