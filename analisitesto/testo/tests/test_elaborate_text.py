from django.test import TestCase
from testo.elaborate_text import *

class Elaborate_Text_Test(TestCase):
    """
    Classe che esegue i test sulle funzioni presenti in elaborate_text.py
    """


    def test_calculate_complexity_long_word(self):
        """
            Test della complessità con una singola parola lunga (con gli algoritmi di calcolo della complessità
            utilizzati in precedenza il test falliva)

        """
        elaborator = Text_elaborator()
        elaborator.elaborate_text("Precipitevolissimevolmente")
        self.assertLessEqual(elaborator.calculate_complexity(), 20)

    def test_terms_frequency_and_count(self):
        elaborator = Text_elaborator()
        elaborator.elaborate_text("parola Parola parola")
        self.assertEqual(elaborator.terms_with_frequency['parola'], 3)
        self.assertEqual(elaborator.terms_count, 3)

    def test_terms_frequency_and_count_no_words(self):
        elaborator = Text_elaborator()
        elaborator.elaborate_text("")
        self.assertEqual(elaborator.terms_with_frequency, {})
        self.assertEqual(elaborator.terms_count, 0)

    def test_phrase_number(self):
        elaborator = Text_elaborator()
        elaborator.elaborate_text("Prima frase. Seconda frase! Terza frase?")
        self.assertEqual(elaborator._phrases_number, 3)

    def test_characters_count(self):
        elaborator = Text_elaborator()
        elaborator.elaborate_text("Testo di ventidue caratteri")
        self.assertEqual(elaborator._characters_count, 22)

    def test_characters_count_no_characters(self):
        elaborator = Text_elaborator()
        elaborator.elaborate_text("")
        self.assertEqual(elaborator._characters_count, 0)

    def test_synonyms_non_existing_word(self):
        synonyms = get_synonyms("qwertyuiop")
        self.assertEqual(synonyms[0], "Non sono stati trovati sinonimi per questo termine")

    def test_synonyms_existing_word(self):
        synonyms = get_synonyms("folla")
        self.assertIn('affollamento', synonyms)
        self.assertIn('caterva', synonyms)
        self.assertIn('frotta', synonyms)
        self.assertIn('mucchio', synonyms)
        self.assertIn('nugolo', synonyms)
        self.assertIn('nuvolo', synonyms)
        self.assertIn('pienone', synonyms)
        self.assertIn('reggimento', synonyms)
        self.assertIn('sciame', synonyms)
        self.assertIn('stuolo', synonyms)

    def test_synonyms_existing_word_2(self):
        synonyms = get_synonyms("pazzia")
        self.assertIn('demenza', synonyms)
        self.assertIn('infermità mentale', synonyms)
        self.assertIn('insania', synonyms)