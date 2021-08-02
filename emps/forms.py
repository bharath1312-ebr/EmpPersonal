from django import forms
from .models import EmpPersonal

class EmpPerModelForm(forms.ModelForm):
    class Meta:
        model = EmpPersonal
        fields = "__all__"

class EmpPersonalform(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter the name'}))
    mobile = forms.CharField()
    email = forms.CharField()
    age = forms.IntegerField()
    address = forms.CharField()
    country = forms.CharField()