import nltk
from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn

class Text_elaborator():
    """
        Classe che tokenizza il testo, elimina le stopword, estrae i dati necessari ed esegue il calcolo della complessità
    """

    # Variabili pubbliche
    terms_count = 0
    terms_with_frequency = dict()
    average_frequency = 0
    chars_to_avoid = 0

    # Variabili private
    _symbols = """:,•,’,«,»,``,`,','',",”,;,/,£,$,%,&,(,),[,],#,-,–,_,+,*,<,>,\,|,="""
    _phrases_number = 0
    _characters_count = 0
    _common_words= list()

    # TOKENIZATION
    def tokenize(self, text):
        """
        Tokenizza il testo

        Args:
            text: testo inserito dall'utente

        Returns:
            testo tokenizzato
        """
        tokens = nltk.word_tokenize(text)
        tokens = [x.split("'") for x in tokens]
        tokens = [y for x in tokens for y in x]
        return tokens

    def eliminate_stopwords(self, tokens):
        """
        Elimina le stopword dal testo

        Args:
            tokens: testo tokenizzato

        Returns:
            testo senza stopword
        """
        text_no_stopwords = list()
        for t in tokens:
            t_low = t.lower()
            if not t_low in stopwords.words('italian') and t_low not in self._symbols:
                text_no_stopwords.append(t_low)
        return text_no_stopwords

    def count_phrases(self, text_no_stopwords):
        """
        Conta il numero di frasi ed elimina punti, punti interrogativi e punti esclamativi

        Args:
            text_no_stopwords: testo senza stopword

        Returns:
            testo senza stopword, punti, punti interrogativi e punti esclamativi
        """
        text_no_stopwords_no_points = text_no_stopwords
        self.terms_with_frequency = None
        self.terms_with_frequency = dict()
        for t in text_no_stopwords:
            if t in ".?!":
                self._phrases_number += 1
                text_no_stopwords_no_points.remove(t)

        return text_no_stopwords_no_points

    def count_occurrences_and_characters(self, text_nostopwords_no_points):
        """
        Conta le occorrenze di ogni termine e il totale dei caratteri

        Args:
            text_nostopwords_no_points: testo senza stopword, punti, punti interrogativi e punti esclamativi

        Returns:
            testo pulito
        """
        clean_text = text_nostopwords_no_points
        count = 0
        for t in clean_text:
            count += 1
            if len(t) <= self.chars_to_avoid or t == "..." or t == "..":
                clean_text.remove(t)
            else:
                self.terms_with_frequency[t] = clean_text.count(t)
                self._characters_count += len(t)
        return clean_text

    def elaborate_text(self, text):
        """
        Effettua la pulizia del testo e calcola i relativi dati

        Returns:
            text: testo "sporco"
        """
        tokens = self.tokenize(text)
        text_no_stopwords = self.eliminate_stopwords(tokens)
        text_no_stopwords_no_points = self.count_phrases(text_no_stopwords)
        clean_text = self.count_occurrences_and_characters(text_no_stopwords_no_points)
        self.terms_count = len(clean_text)
        if len(self.terms_with_frequency) == 0:
            self.average_frequency = 0
        else:
            self.average_frequency = round(self.terms_count / len(self.terms_with_frequency))

    def calculate_complexity(self):
        """
        Calcola la complessità del testo

        Returns:
            valore di complessità
        """
        if self._phrases_number == 0:
            self._phrases_number = 1

        # Creazione liste di parole comuni e non comuni
        non_common_words_list = list()
        common_words_list = list()
        for term in self.terms_with_frequency.keys():
            if term in self._common_words:
                common_words_list.append(term)
            else:
                non_common_words_list.append(term)

        #Formula di complessità che prende ispirazione da Dale-Chall readability formula modificata appositamente per la nostra piattaforma
        #utilizziamo un dataset di parole comuni trovato come open data la cui debolezza è la dimensione limitata
        #per compensare questa debolezza abbiamo pesato di più la presenza di parole comuni all'interno della nostra formula
        #questa formula è l'unica che è riuscita a passare i nostri test di qualità a differenza delle altre due che non li hanno passati
        if self.terms_count == 0 or self.terms_with_frequency == 0:
            return 0
        else:
            #return (10 * (self.characters_count / self.term_count) + 300 * (self.phrases_number / self.terms_with_frequency.__len__()))
            #return ((4.71 * (self.characters_count / self.term_count) + 0.5 * (self.term_count / self.phrases_number)) *2)
            return ((0.1579 * (non_common_words_list.__len__()) / ((common_words_list.__len__()+1)*1.5) * 100)) + (0.0496 * (self.terms_count / self._phrases_number))

def get_synonyms(term):
    """
    Funzione che trova i sinonimi di un termine

    Args:
        term: termine di cui cercare i sinonimi
    Returns:
        i sinonimi del termine in ingresso
    """
    term_lemmas = wn.lemmas(term, lang="ita")
    if term_lemmas == []:
        return ["Non sono stati trovati sinonimi per questo termine"]
    else:
        synonyms_lemma = term_lemmas[0].synset()
        synonyms_lemmas_ita = synonyms_lemma.lemmas(lang="ita")
        synonyms = list()
        for lemma in synonyms_lemmas_ita:
            if lemma.name() == term:
                pass
            else:
                lemma_str = str(lemma.name())
                lemma = lemma_str.replace('_', ' ')
                synonyms.append(lemma)
    if synonyms == []:
        return ["Non sono stati trovati sinonimi per questo termine"]
    return synonyms