from django import forms

class ChemForm(forms.Form):
    ingre_name = forms.CharField()

    def __init__(self, *args, **kwargs):
        super(ChemForm, self).__init__(*args, **kwargs)
        self.fields['ingre_name'].label = ""


class UploadFileForm(forms.Form):
    file = forms.FileField(widget=forms.FileInput(attrs={'label':'','capture': 'camera','accept':'image/x-png,image/gif,image/jpeg','style':'display:none;','id':'file','onchange':'loadFile(event)'}))

    def __init__(self, *args, **kwargs):
        super(UploadFileForm, self).__init__(*args, **kwargs)
        self.fields['file'].label = ""
