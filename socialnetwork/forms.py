from django import forms
from django.contrib.auth.models import User
from socialnetwork.models import *
from models import *
from django.forms import ModelForm
from django.core.validators import validate_email, RegexValidator

MAX_UPLOAD_SIZE = 2500000

class RegistrationForm(forms.Form):
    first_name = forms.CharField(max_length=20)
    last_name  = forms.CharField(max_length=20)
    email      = forms.CharField(max_length = 40,
                                 validators = [validate_email])
    username   = forms.CharField(max_length = 20,
                                 validators = [RegexValidator(r'^[0-9a-zA-Z]*$',
                                 message='Enter only letters and numbers')])
    password1  = forms.CharField(max_length = 200,
                                 label='Password',
                                 widget = forms.PasswordInput())
    password2  = forms.CharField(max_length = 200,
                                 label='Confirm password',
                                 widget = forms.PasswordInput())

    # Customizes form validation for properties that apply to more
    # than one field.  Overrides the forms.Form.clean function.
    def clean(self):
        # Calls our parent (forms.Form) .clean function, gets a dictionary
        # of cleaned data as a result
        cleaned_data = super(RegistrationForm, self).clean()

        # Confirms that the two password fields match
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords did not match.")

        # We must return the cleaned data we got from our parent.
        return cleaned_data


    # Customizes form validation for the username field.
    def clean_username(self):
        # Confirms that the username is not already present in the
        # User model database.
        username = self.cleaned_data.get('username')
        if User.objects.filter(username__exact=username):
            raise forms.ValidationError("Username is already taken.")

        # We must return the cleaned data we got from the cleaned_data
        # dictionary
        return username

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['age', 'bio', 'picture', 'content_type']

    def clean_picture(self):
        picture = self.cleaned_data['picture']

        #Catch for no picture
        if not picture:
            return None
        try:
            #Validates picture
            if not picture.content_type or not picture.content_type.startswith('image'):
                raise forms.ValidationError('File type is not image')
            if picture.size > MAX_UPLOAD_SIZE:
                raise forms.ValidationError('File too big (max size is {0} bytes)'.format(MAX_UPLOAD_SIZE))
            return picture
        #Catch for content_type AttributeError
        except AttributeError:
            return None

class AddPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['text', 'user']

class AddRelationshipForm(forms.ModelForm):
    class Meta:
        model = Relationship
        fields = ['follower', 'followed']