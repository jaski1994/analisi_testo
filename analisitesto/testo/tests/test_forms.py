from django.test import TestCase
from testo.forms import ArticoloForm, ArticoloSearchForm, RegisterForm, BlacklistForm
from testo.models import Articolo

class Testo_Forms_Test(TestCase):

    """
        Un test viene eseguendo un set di funzionalità per la nostra applicazione.per verificare Il corretto sviluppo
        dei casi di test trova problemi nella funzionalità di un'applicazione.
        con form test servono per vedere se i dati  messi negli fields sono giusti o se ci sono dei problemi
    """

    # Valid Form Data
    def test_userforms_valid(self):
        form = ArticoloForm(data={'titolo': "prova", 'fonte': "la stampa", 'data': "2019-01-01", 'testo': "funziona", 'n_cart': 0})
        self.assertTrue(form.is_valid())

    # Invalid Form Data
    def test_userforms_invalid(self):
        form = ArticoloForm(data={'titolo': "prova", 'fonte': "", 'data': "01-01"})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 4)

    # Valid Form Data
    def test_articolo_searchforms_valid(self):
        form_search = ArticoloSearchForm(data={'tank': "*", 'titolo': "corona virus", 'autore': "marco", 'fonte': "stampa", 'data': "2019-04-01"})
        self.assertTrue(form_search.is_valid())

    # Invalid Form Data
    def test_articolo_searchforms_invalid(self):
        form_search = ArticoloSearchForm(data={'titolo': "corona virus", 'autore': "marco", 'fonte': "stampa", 'data': "01-01-2019"})
        self.assertFalse(form_search.is_valid())
        self.assertEqual(len(form_search.errors), 2)

    # Valid Form Data
    def test_articolo_registerforms_valid(self):
        form_registration = RegisterForm(data={'username': "marco", 'email': "marco@gmail.it", 'password1': "Registration1", 'password2': "Registration1"})
        self.assertTrue(form_registration.is_valid())

    # Invalid Form Data
    def test_articolo_registerforms_invalid(self):
        form_registration = RegisterForm(data={'username': "marco", 'email': "marc", 'password1': "Registration1", 'password2': "Registration2"})
        self.assertFalse(form_registration.is_valid())
        self.assertEqual(len(form_registration.errors), 2)

    # Valid Form Data
    def test_black_list_forms_valid(self):
        form_black_list = BlacklistForm(data={'termine_bl': "mela"})
        self.assertTrue(form_black_list.is_valid())

    # Invalid Form Data
    def test_black_list_forms_invalid(self):
        form_black_list = BlacklistForm(data={})
        self.assertFalse(form_black_list.is_valid())
        self.assertEqual(len(form_black_list.errors), 1)
