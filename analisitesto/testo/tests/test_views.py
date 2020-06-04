from django.test import TestCase, Client
from django.urls import reverse, resolve
from django.contrib.auth.models import User
from testo.models import Articolo, Termine, Blacklist

class TestViewsTesto(TestCase):

    """
        Un test viene eseguendo un set di funzionalità per la nostra applicazione.per verificare Il corretto sviluppo
        dei casi di test trova problemi nella funzionalità di un'applicazione.
    """

    #Istanzio quanto comune ed il cliente virtuale
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser1', password='Registration1')
        self.articolo1 = Articolo.objects.create(
            titolo="Titolo test 1",
            fonte="Fonte test 1",
            data="2020-01-01",
            testo="Ciao sono un test 1",
            data_caricamento="2020-05-23",
            quantita_termini=4,
            frequenza_media=1,
            complessita=10,
            autore_id=self.user.id
        )
        self.articolo1.save()

        self.articolo2 = Articolo.objects.create(
            titolo="Titolo test 2",
            fonte="Fonte test 2",
            data="2020-02-02",
            testo="Ciao sono un test 2",
            data_caricamento="2020-05-23",
            quantita_termini=4,
            frequenza_media=1,
            complessita=11,
            autore_id=self.user.id
        )
        self.articolo2.save()

        self.blacklist1 = Blacklist.objects.create(
            id_utente=self.user,
            termine_bl="prova"
        )
        self.blacklist1.save()

        self.termine1 = Termine.objects.create(
            articolo=self.articolo1,
            parola="termine",
            occorrenze=1
        )
        self.termine1.save()

    #Testo il caricamento della pagina di add
    def test_articolo_insert(self):
        self.client.login(username='testuser1', password='Registration1')
        url = reverse('testo:articolo-add')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'testo/articolo_add.html')

    #Testo l'invio dei dati dalla pagina di add
    def test_articolo_insert_POST_add(self):
        self.client.login(username='testuser1', password='Registration1')
        url = reverse('testo:articolo-add')
        response = self.client.post(url, data={
            'titolo': self.articolo1.titolo,
            'fonte': self.articolo1.fonte,
            'data': self.articolo1.data,
            'testo': self.articolo1.testo,
            'n_cart': 0
        })
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/testo/add', status_code=302, target_status_code=200)

    #Testo il caricamento della pagina dei dettagli di un articolo
    def test_articolo_details(self):
        self.client.login(username='testuser1', password='Registration1')
        response = self.client.get(reverse('testo:articolo-details', kwargs={'id': self.articolo1.id}))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'testo/articolo_details.html')

        response = self.client.get(reverse('testo:articolo-details', kwargs={'id': 99}))
        self.assertEqual(response.status_code, 404)

    #Testo che il login e la registrazione funzionino come devono
    def test_login(self):
        self.client.login(username='testuser1', password='Registration1')
        response = self.client.get(reverse('testo:login'))
        self.assertEqual(response.status_code, 200)

    def test_register_load_page(self):
        response = self.client.get(reverse('testo:register'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'register/register.html')

    def test_register(self):
        response = self.client.post(reverse('testo:register'), data={
            'username': "nuovoUser",
            'email': "nuovaEmail@gmail.it",
            'password1': "Registration1",
            'password2': "Registration1"
        })
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/testo/user/login', status_code=302, target_status_code=200)

    #Testo che la pagina di ricerca si carichi correttamente
    def test_articolo_meta_search_form(self):
        self.client.login(username='testuser1', password='Registration1')
        url = reverse('testo:articolo-meta-search')
        response = self.client.post(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'testo/articolo_meta_search.html')

    #Testo che la pagina di blacklist si carichi correttamente
    def test_blacklist(self):
        self.client.login(username='testuser1', password='Registration1')
        url = reverse('testo:user-blacklist')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'testo/blacklist.html')

    #Testo che un termine venga inserito correttamente nella blacklist
    def test_blacklist_POST_add(self):
        self.client.login(username='testuser1', password='Registration1')
        url = reverse('testo:user-blacklist')
        response = self.client.post(url, data={
            'termine_bl': self.blacklist1.termine_bl
        })
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/testo/blacklist', status_code=302, target_status_code=200)

    #Testo che un termine venga cancellato correttamente dalla blacklist
    def test_blacklist_delete(self):
        self.client.login(username='testuser1', password='Registration1')
        url = reverse('testo:blacklist-delete', kwargs={'termine_bl': "prova"})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/testo/blacklist', status_code=302, target_status_code=200)

    #Testo che la pagina di traduzione di un termine venga caricata correttamente
    def test_translate_termine(self):
        self.client.login(username='testuser1', password='Registration1')
        response = self.client.get(reverse('testo:translate-termine', kwargs={'id_term': self.termine1.id}))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'testo/translate_termine.html')

    #Testo che la funzione di logout funzioni
    def test_logout(self):
        self.client.login(username='testuser1', password='Registration1')
        response = self.client.get(reverse('testo:logout'))
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/testo/user/login', status_code=302, target_status_code=200)

    #Testo che la pagina di ricerca iniziale della comparazione funzioni
    def test_compare1(self):
        self.client.login(username='testuser1', password='Registration1')
        response = self.client.get(reverse('testo:articolo-compare'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'testo/compare1.html')

    #Testo che la seconda pagina di ricerca della comparazione funzioni
    def test_compare2(self):
        self.client.login(username='testuser1', password='Registration1')
        response = self.client.get(reverse('testo:articolo-compare2', kwargs={'id': self.articolo1.id}))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'testo/compare2.html')

    #Testo che la pagina di comparazione di due articoli funzioni
    def test_compare_details(self):
        self.client.login(username='testuser1', password='Registration1')
        response = self.client.get(reverse('testo:compare-details', kwargs={'id1': self.articolo1.id, 'id2':self.articolo2.id}))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'testo/compare_details.html')

    #Testo che la funzione di cancellazione di un articolo funzioni correttamente
    def test_articolo_delete(self):
        self.client.login(username='testuser1', password='Registration1')
        response = self.client.get(reverse('testo:delete', kwargs={'id': self.articolo1.id}))
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/testo/load_text', status_code=302, target_status_code=200)

    #Testo che la pagina di visualizzazione del profile venga caricata correttamente
    def test_profile_view(self):
        self.client.login(username='testuser1', password='Registration1')
        response = self.client.get(reverse('testo:profile'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'testo/user_data.html')

    #Testo che la pagina contenente i vari testi inseriti da un utente si carichi correttamente
    def test_load_text(self):
        self.client.login(username='testuser1', password='Registration1')
        response = self.client.get(reverse('testo:load-text'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'testo/load_text.html')

    #Testo che la pagina delle statistiche venga caricata correttamente
    def test_statistiche_articoli(self):
        self.client.login(username='testuser1', password='Registration1')
        response = self.client.get(reverse('testo:statistiche-articoli'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'testo/statistiche_articoli.html')

    def test_sinonimi_view(self):
        self.client.login(username='testuser1', password='Registration1')
        response = self.client.get(reverse('testo:sinonimi', kwargs={'id_term': self.termine1.id}))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'testo/sinonimi.html')
