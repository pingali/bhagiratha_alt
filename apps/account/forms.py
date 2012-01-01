from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from uni_form.helpers import FormHelper, Submit, Reset
from captcha.fields import ReCaptchaField 
from django.conf import settings 

class SignupForm(UserCreationForm):
    
    email = forms.EmailField(label="Email")
    captcha = ReCaptchaField(label="Please enter text you see or hear")

    @property
    def helper(self):
        form = SignupForm()
        helper = FormHelper()
        reset = Reset('','Reset')
        helper.add_input(reset)
        submit = Submit('','Sign Up')
        helper.add_input(submit)
        helper.form_action = '/account/signup'
        helper.form_method = 'POST'
        return helper


class LoginForm(forms.Form):
    
    username = forms.CharField(label="Username", max_length=30)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    next     = forms.CharField(label="next", widget=forms.HiddenInput, required=False)
    captcha = ReCaptchaField(label="Please enter text you see or hear")

    @property
    def helper(self):
        form = LoginForm()
        helper = FormHelper()
        reset = Reset('','Reset')
        helper.add_input(reset)
        submit = Submit('','Log In')
        helper.add_input(submit)
        helper.form_action = '/account/login'
        helper.form_method = 'POST'
        return helper

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            self.user_cache = authenticate(username=username, password=password)
            if self.user_cache is None:
                raise forms.ValidationError("Please enter a correct username and password. Note that both fields are case-sensitive.")
            elif not self.user_cache.is_active:
                raise forms.ValidationError("This account is inactive.")
        return self.cleaned_data

