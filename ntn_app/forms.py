from django import forms

from django.contrib.auth.models import User
from django.contrib.auth import authenticate


class RegistrationForm(forms.Form):
    name_of_institution = forms.CharField(
        max_length=200,
        required=True,
        label="Institution name",
        widget=forms.TextInput(
                attrs={
                    'class': "form-control",
                    'placeholder': "Institution name"
                }
        )
    )

    state = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(
                attrs={
                    'class': "form-control",
                    'placeholder': 'State'
                }
        )
    )

    website = forms.CharField(
        max_length=200,
        required=True,
        widget=forms.TextInput(
                attrs={
                    'class': "form-control",
                    'placeholder': 'Website'
                }
        )
    )

    name_of_contact_person = forms.CharField(
        max_length=200,
        required=True,
        widget=forms.TextInput(
                attrs={
                    'class': "form-control",
                    'placeholder': 'Name of contact person'
                }
        )
    )

    title = forms.CharField(
        max_length=70,
        required=True,
        widget=forms.TextInput(
                attrs={
                    'class': "form-control",
                    'placeholder': 'Title'
                }
        )
    )

    email = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.EmailInput(
                attrs={
                    'class': "form-control",
                    'placeholder': 'Email'
                }
        )
    )

    phone  = forms.CharField(
        required=False,
        max_length=16,
        label='Phone #',
        widget=forms.TextInput(
            attrs={
                'class': "form-control",
                'placeholder': 'Phone number'
            }
        )
    )

    password1  = forms.CharField(
        max_length=200,
        label='Password', 
        required = True,
        widget=forms.PasswordInput(
            attrs={
                'class': "form-control",
                'placeholder': 'Password'
            }
        )
    )

    password2  = forms.CharField(
        max_length=200,
        label='Password', 
        required = True,
        widget=forms.PasswordInput(
            attrs={
                'class': "form-control",
                'placeholder': 'Confirm Password'
            }
        )
    )


    # Customizes form validation for properties that apply to more
    # than one field.  Overrides the forms.Form.clean function.
    def clean(self):
        # Calls our parent (forms.Form) .clean function, gets a dictionary
        # of cleaned data as a result
        cleaned_data = super().clean()

        # We must return the cleaned data we got from our parent.
        return cleaned_data

    def clean_password2(self):
        # Confirms that the two password fields match

        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords did not match.")
        
        return password1

    # Customizes form validation for the username field.
    def clean_email(self):
        # Confirms that the username is not already present in the
        # User model database.
        email = self.cleaned_data.get('email')
        if User.objects.filter(email__exact=email):
            raise forms.ValidationError("Email already in use")

        # We must return the cleaned data we got from the cleaned_data
        # dictionary
        return email


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=20,
        required=True,
        widget=forms.TextInput(
                attrs={'class': "form-control"}
        )
    )
    password = forms.CharField(
        max_length=200,
        required=True,
        widget=forms.PasswordInput(
            attrs={
            'class': 'form-control'
            }
        )
    )

    # Customizes form validation for properties that apply to more
    # than one field.  Overrides the forms.Form.clean function.
    def clean(self):
        # Calls our parent (forms.Form) .clean function, gets a dictionary
        # of cleaned data as a result
        cleaned_data = super().clean()

        # Confirms that the two password fields match
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if not user:
            raise forms.ValidationError("Invalid username/password")

        # We must return the cleaned data we got from our parent.
        return cleaned_data
