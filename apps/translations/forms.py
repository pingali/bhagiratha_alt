#-*- coding: utf-8 -*-

from django import forms
from uni_form.helpers import FormHelper, Submit, Reset
from uni_form.layout import Layout,Fieldset, Div, Row, HTML
from models import Translation

class TranslationForm(forms.ModelForm):
    
    class Meta: 
        model = Translation
        exclude = ('user', 'document', 'language', 'created_at', 'updated_at', 'iteration', 'status') 

    def __init__(self, *args, **kwargs):
        super(TranslationForm, self).__init__(*args, **kwargs) 
        self.set_helper() 

    def set_helper(self):
        helper = FormHelper()
        reset = Reset('','Reset')
        helper.add_input(reset)
        submit = Submit('','Submit')
        helper.add_input(submit)
        helper.form_action = ''
        helper.form_method = 'POST'
        helper.form_class="blueForms"
        self.helper = helper
