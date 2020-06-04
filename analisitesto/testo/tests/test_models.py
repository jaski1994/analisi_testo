from django.test import TestCase
from testo.models import Articolo, Termine, User, Blacklist


class Testo_Models_Test(TestCase):

    """
        Un test viene eseguendo un set di funzionalità per la nostra applicazione.per verificare Il corretto sviluppo
        dei casi di test trova problemi nella funzionalità di un'applicazione.

    """
    #Istanzio le cose comuni
    def setUp(self):
        """
        I metodi setUp () consentono di definire istruzioni che verranno eseguite prima e dopo ciascun metodo di prova
        """
        self.utente_test = User.objects.create_user(username='testuser1', password='Registration1')
        self.login = self.client.login(username='testuser1', password='Registration1')

        self.articolo_test = Articolo()
        self.articolo_test.titolo = "Titolo test"
        self.articolo_test.fonte = "Fonte test"
        self.articolo_test.data = "2020-01-01"
        self.articolo_test.testo = "Testo test"
        self.articolo_test.data_caricamento = "2020-05-23"
        self.articolo_test.quantita_termini = len(self.articolo_test.testo.split())
        self.articolo_test.autore = self.utente_test
        self.articolo_test.save()

        self.termine_test = Termine()
        self.termine_test.parola = "ciao"
        self.termine_test.occorrenze = 1
        self.termine_test.articolo = self.articolo_test
        self.termine_test.save()

        self.blacklist_test = Blacklist()
        self.blacklist_test.termine_bl = "Termine"
        self.blacklist_test.id_utente = self.utente_test
        self.blacklist_test.save()

    #Controllo che i campi dei miei modelli funzionino come dovrebbero
    def test_articolo_fields(self):
        articolo_test = Articolo()
        articolo_test.titolo = "Titolo test"
        articolo_test.fonte = "Fonte test"
        articolo_test.data = "2020-01-01"
        articolo_test.testo = "Testo test"
        articolo_test.data_caricamento = "2020-05-23"
        articolo_test.autore = self.utente_test
        articolo_test.save()

        record = Articolo.objects.get(id=articolo_test.id)
        self.assertEqual(record, articolo_test)

    def test_termine_fields(self):
        termine_test = Termine()
        termine_test.parola = "ciao"
        termine_test.occorrenze = 1
        termine_test.articolo = self.articolo_test
        termine_test.save()

        record = Termine.objects.get(id=termine_test.id)
        self.assertEqual(record, termine_test)

    def test_blacklist_fields(self):
        blacklist_test = Blacklist()
        blacklist_test.termine_bl = "TermineBlTest"
        blacklist_test.id_utente = self.utente_test
        blacklist_test.save()
        record = Blacklist.objects.get(termine_bl=blacklist_test.termine_bl, id_utente=self.utente_test)
        self.assertEqual(record, blacklist_test)

    #Test sul metodo __str__
    def test_articolomodel_str(self):
        self.assertEqual(self.articolo_test.__str__(), "Titolo test, Fonte test, 2020-01-01, Testo test, 2020-05-23, None, 2, None")

    def test_terminemodel_str(self):
        self.assertEqual(self.termine_test.__str__(), "ciao, 1")

    def test_blacklistmodel_str(self):
        self.assertEqual(self.blacklist_test.__str__(), "termine")

