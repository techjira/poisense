from django import forms

# text box form
class ChemForm(forms.Form):
    ingre_name = forms.CharField()

    def __init__(self, *args, **kwargs):
        super(ChemForm, self).__init__(*args, **kwargs)
        self.fields['ingre_name'].label = ""

# image upload form
class UploadFileForm(forms.Form):
    file = forms.FileField(widget=forms.FileInput(attrs={'label':'','capture': 'camera','accept':'image/x-png,image/gif,image/jpeg','style':'display:none;','id':'file','onchange':'loadFile(event)'}))

    def __init__(self, *args, **kwargs):
        super(UploadFileForm, self).__init__(*args, **kwargs)
        self.fields['file'].label = ""

#for food allergy
class UploadAllergyFileForm(forms.Form):
    Allergy_file = forms.FileField(widget=forms.FileInput(attrs={'label':'','capture': 'camera','accept':'image/x-png,image/gif,image/jpeg','style':'display:none;','id':'file','onchange':'loadFile(event)'}))

    def __init__(self, *args, **kwargs):
        super(UploadAllergyFileForm, self).__init__(*args, **kwargs)
        self.fields['Allergy_file'].label = ""
