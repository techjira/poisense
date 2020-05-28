from django import forms
from poisenseapp.models import Foodcontain, User, UserAllergyinfo
from django_select2 import forms as s2forms
from django.contrib.auth.password_validation import validate_password
from django.core import validators

# text box form
class ChemForm(forms.Form):
    ingre_name = forms.CharField()

    def __init__(self, *args, **kwargs):
        super(ChemForm, self).__init__(*args, **kwargs)
        self.fields['ingre_name'].label = ""

# image upload form
class UploadFileForm(forms.Form):
    file = forms.FileField(widget=forms.FileInput(attrs={'label':'','capture': 'camera','accept':'image/x-png,image/gif,image/jpeg','style':'display:none;','id':'file','onchange':'loadFile(event)','onclick':'myFunction()'}))

    def __init__(self, *args, **kwargs):
        super(UploadFileForm, self).__init__(*args, **kwargs)
        self.fields['file'].label = ""

#for food allergy
class UploadAllergyFileForm(forms.Form):
    Allergy_file = forms.FileField(widget=forms.FileInput(attrs={'label':'','capture': 'camera','accept':'image/x-png,image/gif,image/jpeg','style':'display:none;','id':'file','onchange':'loadFile(event)','onclick':'myFunction()'}))

    def __init__(self, *args, **kwargs):
        super(UploadAllergyFileForm, self).__init__(*args, **kwargs)
        self.fields['Allergy_file'].label = ""

#for user login
class UserForm(forms.Form):
    username = forms.CharField(max_length=128, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Username",'autofocus': ''}))
    password = forms.CharField(max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder': "Password"}))

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = ""
        self.fields['password'].label = ""

#for user registration
class RegisterForm(forms.Form):
    username = forms.CharField(max_length=128, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Username",'autofocus': ''}))
    # 0521suqin
    password1 = forms.CharField(max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder': "Password",'autofocus': '','onfocus': "inputFocus()"}))
    password2 = forms.CharField(max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder': "Password(repeat)",'autofocus': ''}))

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = ""
        self.fields['password1'].label = ""
        self.fields['password2'].label = ""

# for user adding the allergy information
class AllergyInfoForm(forms.ModelForm):

    kid_allergy = forms.ModelMultipleChoiceField(queryset=Foodcontain.objects.distinct('allergycategory'),
                                        to_field_name="allergycategory", required=False, label="Choose Common Allergens", widget=forms.CheckboxSelectMultiple(attrs={'class': 'filled-in','vertical-align':'middle'}))
    class Meta:
        model = UserAllergyinfo
        fields = ['kid_name','kid_allergy','personalised_allergy']
        widgets = {
            'kid_allergy': forms.ModelMultipleChoiceField(queryset=Foodcontain.objects.distinct('allergycategory'),
                                       to_field_name="allergycategory",widget=forms.CheckboxSelectMultiple(attrs={'class': 'filled-in','vertical-align':'middle'})),
            'kid_name': forms.TextInput(attrs={'class': 'form-control', 'autofocus': '', 'name':'name','id':'name'}),
            'personalised_allergy': forms.TextInput(attrs={'class': 'form-control', 'autofocus': ''})
        }
        labels = {
            'personalised_allergy':"Your Personalised Allergies"
        }
