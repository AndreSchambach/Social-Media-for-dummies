# Importiere das Formularmodul aus Django
from django import forms
from django.contrib.auth.models import User

# Definiere das Formular für das Erstellen eines Beitrags
HOBBY_CHOICES = [
    ('Angeln', 'Angeln'),
    ('Anime schauen', 'Anime schauen'),
    ('Antiquitäten sammeln', 'Antiquitäten sammeln'),
    ('Astronomie/Sternbeobachtung', 'Astronomie/Sternbeobachtung'),
    ('Autogramme sammeln', 'Autogramme sammeln'),
    ('Autoreparaturen', 'Autoreparaturen'),
    ('Backen', 'Backen'),
    ('Badminton spielen', 'Badminton spielen'),
    ('Basketball spielen', 'Basketball spielen'),
    ('Bierbrauen', 'Bierbrauen'),
    ('Blogs schreiben', 'Blogs schreiben'),
    ('Bogenschießen', 'Bogenschießen'),
    ('Brettspiele spielen', 'Brettspiele spielen'),
    ('Camping', 'Camping'),
    ('Comics/Mangas lesen', 'Comics/Mangas lesen'),
    ('Computerprogrammierung', 'Computerprogrammierung'),
    ('Drohnen fliegen', 'Drohnen fliegen'),
    ('E-Sport', 'E-Sport'),
    ('Elektronik basteln', 'Elektronik basteln'),
    ('Fantasy-Sport', 'Fantasy-Sport'),
    ('Filme schauen', 'Filme schauen'),
    ('Fitnessstudio besuchen', 'Fitnessstudio besuchen'),
    ('Fotografieren', 'Fotografieren'),
    ('Freiwilligenarbeit', 'Freiwilligenarbeit'),
    ('Fußball spielen', 'Fußball spielen'),
    ('Gamen/Videospiele spielen', 'Gamen/Videospiele spielen'),
    ('Gartenarbeit', 'Gartenarbeit'),
    ('Gärtnern', 'Gärtnern'),
    ('Genealogie/Familienforschung', 'Genealogie/Familienforschung'),
    ('Geocaching', 'Geocaching'),
    ('Golf', 'Golf'),
    ('Grillen', 'Grillen'),
    ('Häkeln', 'Häkeln'),
    ('Heimwerken', 'Heimwerken'),
    ('Historische Reenactments', 'Historische Reenactments'),
    ('Holzarbeiten', 'Holzarbeiten'),
    ('Jagen', 'Jagen'),
    ('Kajakfahren', 'Kajakfahren'),
    ('Kampfsport (z.B. Karate, Judo)', 'Kampfsport (z.B. Karate, Judo)'),
    ('Kanufahren', 'Kanufahren'),
    ('Kitesurfen', 'Kitesurfen'),
    ('Klettern/Bouldern', 'Klettern/Bouldern'),
    ('Kochen', 'Kochen'),
    ('Konzertbesuche', 'Konzertbesuche'),
    ('LARP (Live Action Role-Playing)', 'LARP (Live Action Role-Playing)'),
    ('Laufen/Joggen', 'Laufen/Joggen'),
    ('Lesen', 'Lesen'),
    ('Malen/Zeichnen', 'Malen/Zeichnen'),
    ('Meditation', 'Meditation'),
    ('Metallarbeiten', 'Metallarbeiten'),
    ('Modellautos sammeln', 'Modellautos sammeln'),
    ('Modelleisenbahnen', 'Modelleisenbahnen'),
    ('Modellbau', 'Modellbau'),
    ('Motorradfahren', 'Motorradfahren'),
    ('Münzen sammeln', 'Münzen sammeln'),
    ('Museumsbesuche', 'Museumsbesuche'),
    ('Nähen', 'Nähen'),
    ('Nordic Walking', 'Nordic Walking'),
    ('Puzzeln', 'Puzzeln'),
    ('Radfahren', 'Radfahren'),
    ('Reisen', 'Reisen'),
    ('Reiten', 'Reiten'),
    ('Schießen', 'Schießen'),
    ('Schmuckherstellung', 'Schmuckherstellung'),
    ('Schreiben', 'Schreiben'),
    ('Schwimmen', 'Schwimmen'),
    ('Segeln', 'Segeln'),
    ('Serien/TV schauen', 'Serien/TV schauen'),
    ('Skifahren', 'Skifahren'),
    ('Singen', 'Singen'),
    ('Snowboarden', 'Snowboarden'),
    ('Sprachen lernen', 'Sprachen lernen'),
    ('Stricken', 'Stricken'),
    ('Surfen', 'Surfen'),
    ('Tanzen', 'Tanzen'),
    ('Tennis spielen', 'Tennis spielen'),
    ('Theater besuchen', 'Theater besuchen'),
    ('Tischtennis spielen', 'Tischtennis spielen'),
    ('Töpfern', 'Töpfern'),
    ('Vogelbeobachtung', 'Vogelbeobachtung'),
    ('Volleyball spielen', 'Volleyball spielen'),
    ('Weinverkostung', 'Weinverkostung'),
    ('Whiskyverkostung', 'Whiskyverkostung')
]

class HobbyFilterForm(forms.Form):
    hobbies = forms.MultipleChoiceField(
        choices=HOBBY_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Filter nach Hobbies"
    )

class BeitragFormular(forms.Form):
    titel = forms.CharField(max_length=100, required=True)
    bild = forms.ImageField(required=False)
    kommentar = forms.CharField(widget=forms.Textarea, required=False)
    hobby = forms.ChoiceField(choices=HOBBY_CHOICES, required=False)

# Definiere das Formular für die Bearbeitung des Benutzerprofils
class ProfilFormular(forms.Form):
    # Definiere ein optionales Biografiefeld, das ein mehrzeiliges Texteingabefeld (Textarea) verwendet
    bio = forms.CharField(widget=forms.Textarea, required=False)
    
    # Definiere ein optionales Bildfeld für das Profilbild, das eine Bilddatei erwartet
    profilbild = forms.ImageField(required=False)

# Formular zur Benutzerregistrierung
class RegistrierungsFormular(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)  # Passwortfeld mit Maskierung

    class Meta:
        model = User  # Verwende das User-Modell von Django
        fields = ['username', 'password', 'email']  # Felder, die im Formular angezeigt werden


class ProfilFormular(forms.Form):
    bio = forms.CharField(widget=forms.Textarea, required=False)
    social_media = forms.CharField(widget=forms.Textarea, required=False)
    profilbild = forms.ImageField(required=False)
    bannerbild = forms.ImageField(required=False)

class KommentarForm(forms.Form):
    text = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3, 'cols': 40}),
        label='Kommentar'
    )