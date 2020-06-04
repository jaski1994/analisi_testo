import email
from datetime import datetime

# import self as self
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from nltk.lm.vocabulary import _

from .models import Articolo, Blacklist
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, ReadOnlyPasswordHashField
from django.contrib.auth import authenticate, login



class ArticoloForm(forms.ModelForm):
    """
        form per articolo con i diversi field e insieme a crispy
    """

    CHARACTERS_CHOICES = [
        ('0', '0'),
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
    ]
    #helper = FormHelper()
    #helper.form_id = 'articolo-crispy-form'
    #helper.form_method = 'POST'
    #helper.add_input(Submit('submit', 'Save'))
    n_cart = forms.IntegerField(min_value=0, max_value=3, initial=0 , label="Non analizzare i termini con un numero di lettere inferiore a:", widget=forms.Select(choices=CHARACTERS_CHOICES))
    data = forms.DateField(label="Data (AAAA-MM-GG)")
    class Meta:
        model = Articolo
        fields = ('titolo', 'fonte', 'data', 'testo', 'n_cart')


class RegisterForm(UserCreationForm):
    """
          Form di registrazione per l'utente
    """

    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')



    def clean_email(self):
        """
             Controllo che l'email non sia presa da alcun utente
        """
        data = self.cleaned_data['email']
        if User.objects.filter(email=data).exists():
            raise forms.ValidationError("This email already exists")
        return data


class ArticoloSearchForm(forms.Form):
    """
       form viene customization e generato da django con i vari controlli
    """
    tank = forms.CharField(widget=forms.HiddenInput(), initial="*")
    titolo = forms.CharField(max_length=50, label='Inserire il titolo dell\'articolo', required=False,initial="")
    autore = forms.CharField(max_length=50, label='Inserire il nome del autore dell\'articolo', required=False,initial="")
    fonte = forms.CharField(max_length=50, label='Inserire il nome della fonte dell\'articolo', required=False,initial="")
    data = forms.DateField(label='Inserire la data del testo dell\'articolo', required=False)

    def is_valid(self):
        res = super().is_valid()
        return res

class BlacklistForm(forms.Form):
    """
        form per inserire dati nella blacklist
    """
    termine_bl = forms.CharField(label="Termine")
    class Meta:
        model = Blacklist
        fields = ('termine_bl')
