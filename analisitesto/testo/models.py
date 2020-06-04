from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

# Create your models here.
from django.db.models import Q


class Articolo(models.Model):
    """
       modello per articolo con i diversi attributi
    """
    titolo = models.CharField(max_length=100)
    fonte = models.CharField(max_length=50)
    data = models.DateField()
    testo = models.TextField()
    data_caricamento = models.DateField(default=datetime.now)
    frequenza_media = models.CharField(max_length=6, default=None, null=True)
    quantita_termini = models.CharField(max_length=8, default=None, null=True)
    complessita = models.IntegerField(default=None, null=True)
    autore = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
         return '{titolo}, {fonte}, {data}, {testo}, {data_caricamento}, {frequenza_media}, {quantita_termini}, {complessita}'\
             .format(titolo=self.titolo, fonte=self.fonte, data=self.data, testo=self.testo, data_caricamento=self.data_caricamento,
                     frequenza_media=self.frequenza_media, quantita_termini=self.quantita_termini, complessita=self.complessita)

    class Meta:
        verbose_name_plural = 'Articolo'


class Termine(models.Model):
    """
       modello per i termini e le relative frequenze
    """
    articolo = models.ForeignKey('Articolo', on_delete=models.CASCADE)
    parola = models.CharField(max_length=30)
    occorrenze = models.IntegerField(default=None, null=True)


    def __str__(self):
        return '{parola}, {occorrenze}'.format(parola=self.parola, occorrenze=self.occorrenze)


class Blacklist(models.Model):
    """
        modello per la blacklist dei termini di un utente
    """
    id_utente = models.ForeignKey(User, on_delete=models.CASCADE)
    termine_bl = models.CharField(max_length=200)

    class Meta:
        unique_together = ('id_utente', 'termine_bl')


    def __str__(self):
        return '{termine_bl}'.format(termine_bl=self.termine_bl)



    def save(self, *args, **kwargs):
        """
            Controlla che il termine sia già presente all'interno della tabella del database
        """
        self.termine_bl = self.termine_bl.lower()
        termine_black = Blacklist.objects.filter(Q(termine_bl=self.termine_bl.lower(), id_utente=self.id_utente))
        if termine_black:
            return 1
        else:
            return super(Blacklist, self).save(*args, **kwargs)
