from django import forms
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget

class NewsletterCreatorForm(forms.Form):
    subject = forms.CharField(label="Assunto:", widget=forms.TextInput(attrs={'class': 'vTextField'}))
    receivers = forms.CharField(label="Para:", widget=forms.TextInput(attrs={'class': 'vTextField'}))
    message = forms.CharField(widget=SummernoteWidget(), label="Conteúdo do e-mail:")