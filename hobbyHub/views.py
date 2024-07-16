from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from hobbyHub.forms import BeitragFormular, ProfilFormular, RegistrierungsFormular, HobbyFilterForm, KommentarForm
from django.conf import settings
from datetime import datetime
from django.contrib.auth import login, authenticate
import json, os, uuid
from django.http import JsonResponse
from django.contrib.auth.models import User

daten_pfad = os.path.join(settings.BASE_DIR, 'hobbyHub', 'data')

# registriert einen neuen benutzer
def registrierung(request):
    if request.method == 'POST':
        form = RegistrierungsFormular(request.POST)
        if form.is_valid():
            user = form.save()
            password = form.cleaned_data.get('password')
            user.set_password(password)
            user.save()
            user = authenticate(username=user.username, password=password)
            login(request, user)
            return redirect('feed')
    else:
        form = RegistrierungsFormular()
    return render(request, 'hobbyHub/registrierung.html', {'form': form})

# lädt eine json-datei und gibt deren inhalt zurück
def lade_json(datei):
    with open(os.path.join(daten_pfad, datei), 'r', encoding='utf-8') as file:
        return json.load(file)

# speichert daten in eine json-datei
def speichere_json(datei, daten):
    with open(os.path.join(daten_pfad, datei), 'w') as file:
        json.dump(daten, file, indent=4, default=str)

# zeigt den feed an, gefiltert nach hobbies, falls angegeben
@login_required
def feed(request):
    beitraege = lade_json('posts.json')

    if request.method == 'POST':
        form = HobbyFilterForm(request.POST)
        if form.is_valid():
            ausgewaehlte_hobbies = form.cleaned_data['hobbies']
            if ausgewaehlte_hobbies:
                beitraege = [beitrag for beitrag in beitraege if beitrag['hobby'] in ausgewaehlte_hobbies]
    else:
        form = HobbyFilterForm()

    beitraege.sort(key=lambda x: x['erstellt_am'], reverse=True)
    for beitrag in beitraege:
        if 'comments' in beitrag:
            beitrag['comments'].sort(key=lambda x: x['erstellt_am'], reverse=True)

    return render(request, 'hobbyHub/feed.html', {'form': form, 'beitraege': beitraege})

# ermöglicht es, einen neuen beitrag hochzuladen
@login_required
def upload(request):
    if request.method == 'POST':
        form = BeitragFormular(request.POST, request.FILES)
        if form.is_valid():
            titel = form.cleaned_data.get('titel', 'Standard Titel')
            hobby = form.cleaned_data.get('hobby', 'Kein Hobby ausgewählt')
            kommentar = form.cleaned_data.get('kommentar', '')
            bild = form.cleaned_data.get('bild', None)

            if bild:
                ext = bild.name.split('.')[-1]
                bild_name = f"{uuid.uuid4()}.{ext}"
                bild_path = os.path.join(settings.MEDIA_ROOT, 'images', bild_name)
                with open(bild_path, 'wb+') as destination:
                    for chunk in bild.chunks():
                        destination.write(chunk)
                bild_path = 'images/' + bild_name
            else:
                bild_path = ''

            profilbild = None
            profiles = lade_json('profiles.json')
            for profile in profiles:
                if profile['benutzer'] == request.user.username:
                    profilbild = profile.get('profilbild')
                    break

            daten_pfad = os.path.join(settings.BASE_DIR, 'hobbyHub', 'data', 'posts.json')
            try:
                with open(daten_pfad, 'r') as file:
                    beitraege = json.load(file)
            except FileNotFoundError:
                beitraege = []

            beitrag = {
                'id': str(uuid.uuid4()),
                'benutzer': request.user.username,
                'bild': bild_path,
                'kommentar': kommentar,
                'titel': titel,
                'hobby': hobby,
                'likes': [],
                'erstellt_am': datetime.now().isoformat(),
                'profilbild': profilbild
            }
            beitraege.append(beitrag)

            with open(daten_pfad, 'w') as file:
                json.dump(beitraege, file, indent=4)

            return redirect('feed')
    else:
        form = BeitragFormular()

    return render(request, 'hobbyHub/upload.html', {'form': form})

# zeigt das profil des aktuellen benutzers an und erlaubt die bearbeitung
@login_required
def profil(request):
    profile = lade_json('profiles.json')
    posts = lade_json('posts.json')

    aktuelles_profil = next((p for p in profile if p['benutzer'] == request.user.username), None)

    benutzer_posts = [post for post in posts if post['benutzer'] == request.user.username]
    benutzer_posts.sort(key=lambda x: x['erstellt_am'], reverse=True)

    if request.method == 'POST':
        form = ProfilFormular(request.POST, request.FILES)
        if form.is_valid():
            profilbild = request.FILES.get('profilbild')
            bannerbild = request.FILES.get('bannerbild')
            if profilbild:
                ext = profilbild.name.split('.')[-1]
                profilbild_name = f"{uuid.uuid4()}.{ext}"
                profilbild_path = os.path.join(settings.MEDIA_ROOT, 'profile_images', profilbild_name)
                os.makedirs(os.path.dirname(profilbild_path), exist_ok=True)
                with open(profilbild_path, 'wb+') as destination:
                    for chunk in profilbild.chunks():
                        destination.write(chunk)
            if bannerbild:
                ext = bannerbild.name.split('.')[-1]
                bannerbild_name = f"{uuid.uuid4()}.{ext}"
                bannerbild_path = os.path.join(settings.MEDIA_ROOT, 'banner_images', bannerbild_name)
                os.makedirs(os.path.dirname(bannerbild_path), exist_ok=True)
                with open(bannerbild_path, 'wb+') as destination:
                    for chunk in bannerbild.chunks():
                        destination.write(chunk)
            if aktuelles_profil:
                aktuelles_profil['bio'] = form.cleaned_data['bio']
                aktuelles_profil['social_media'] = form.cleaned_data['social_media']
                if profilbild:
                    aktuelles_profil['profilbild'] = 'profile_images/' + profilbild_name
                if bannerbild:
                    aktuelles_profil['bannerbild'] = 'banner_images/' + bannerbild_name
            else:
                aktuelles_profil = {
                    'benutzer': request.user.username,
                    'bio': form.cleaned_data['bio'],
                    'social_media': form.cleaned_data['social_media'],
                    'profilbild': 'profile_images/' + profilbild_name if profilbild else '',
                    'bannerbild': 'banner_images/' + bannerbild_name if bannerbild else ''
                }
                profile.append(aktuelles_profil)
            speichere_json('profiles.json', profile)
            return redirect('profil')
    else:
        form = ProfilFormular(initial=aktuelles_profil)

    return render(request, 'hobbyHub/profil.html', {'form': form, 'profil': aktuelles_profil, 'beitraege': benutzer_posts})

# ermöglicht das bearbeiten des eigenen profils
@login_required
def profil_bearbeiten(request):
    profile = lade_json('profiles.json')
    aktuelles_profil = next((p for p in profile if p['benutzer'] == request.user.username), None)
    if request.method == 'POST':
        form = ProfilFormular(request.POST, request.FILES)
        if form.is_valid():
            profilbild = request.FILES.get('profilbild')
            bannerbild = request.FILES.get('bannerbild')
            if profilbild:
                ext = profilbild.name.split('.')[-1]
                profilbild_name = f"{uuid.uuid4()}.{ext}"
                profilbild_path = os.path.join(settings.MEDIA_ROOT, 'profile_images', profilbild_name)
                os.makedirs(os.path.dirname(profilbild_path), exist_ok=True)
                with open(profilbild_path, 'wb+') as destination:
                    for chunk in profilbild.chunks():
                        destination.write(chunk)
            if bannerbild:
                ext = bannerbild.name.split('.')[-1]
                bannerbild_name = f"{uuid.uuid4()}.{ext}"
                bannerbild_path = os.path.join(settings.MEDIA_ROOT, 'banner_images', bannerbild_name)
                os.makedirs(os.path.dirname(bannerbild_path), exist_ok=True)
                with open(bannerbild_path, 'wb+') as destination:
                    for chunk in bannerbild.chunks():
                        destination.write(chunk)
            if aktuelles_profil:
                aktuelles_profil['bio'] = form.cleaned_data['bio']
                aktuelles_profil['social_media'] = form.cleaned_data['social_media']
                if profilbild:
                    aktuelles_profil['profilbild'] = 'profile_images/' + profilbild_name
                if bannerbild:
                    aktuelles_profil['bannerbild'] = 'banner_images/' + bannerbild_name
            else:
                aktuelles_profil = {
                    'benutzer': request.user.username,
                    'bio': form.cleaned_data['bio'],
                    'social_media': form.cleaned_data['social_media'],
                    'profilbild': 'profile_images/' + profilbild_name if profilbild else '',
                    'bannerbild': 'banner_images/' + bannerbild_name if bannerbild else ''
                }
                profile.append(aktuelles_profil)
            speichere_json('profiles.json', profile)
            return redirect('profil')
    else:
        form = ProfilFormular(initial=aktuelles_profil)
    return render(request, 'hobbyHub/edit_profile.html', {'form': form})

# zeigt die logout-seite an
def logout_page(request):
    return render(request, 'hobbyHub/logout.html')

# fügt einen like zu einem beitrag hinzu oder entfernt ihn
@login_required
def like_post(request, post_id):
    beitraege = lade_json('posts.json')
    beitrag = next((b for b in beitraege if b['id'] == str(post_id)), None)
    if beitrag:
        if request.user.username not in beitrag['likes']:
            beitrag['likes'].append(request.user.username)
        else:
            beitrag['likes'].remove(request.user.username)
        speichere_json('posts.json', beitraege)
    return redirect('feed')

# zeigt das profil eines anderen benutzers an
@login_required
def benutzer_profil(request, benutzername):
    try:
        benutzer = User.objects.get(username=benutzername)
        profil = lade_json('profiles.json')
        benutzer_profil = next((p for p in profil if p['benutzer'] == benutzer.username), None)
        if not benutzer_profil:
            benutzer_profil = {'benutzer': benutzer.username, 'bio': '', 'profilbild': '', 'social_media': '', 'bannerbild': '', 'followers': []}
        
        beitraege = lade_json('posts.json')
        user_beitraege = [beitrag for beitrag in beitraege if beitrag['benutzer'] == benutzer.username]
        user_beitraege.sort(key=lambda x: x['erstellt_am'], reverse=True)

        return render(request, 'hobbyHub/benutzer_profil.html', {'benutzer_profil': benutzer_profil, 'beitraege': user_beitraege})
    except User.DoesNotExist:
        return redirect('feed')

# ermöglicht das folgen oder entfolgen eines benutzers
@login_required
def follow_user(request, benutzername):
    if request.method == 'POST':
        try:
            benutzer = User.objects.get(username=benutzername)
            profile = lade_json('profiles.json')
            benutzer_profil = next((p for p in profile if p['benutzer'] == benutzer.username), None)
            if benutzer_profil:
                if request.user.username in benutzer_profil.get('followers', []):
                    benutzer_profil['followers'].remove(request.user.username)
                else:
                    benutzer_profil.setdefault('followers', []).append(request.user.username)
                speichere_json('profiles.json', profile)
            return redirect('benutzer_profil', benutzername=benutzername)
        except User.DoesNotExist:
            return redirect('feed')
    return redirect('feed')

# testansicht zum anzeigen von beiträgen mit hobby-filter
def test_view(request):
    form = HobbyFilterForm()
    beitraege = lade_json('posts.json')
    
    if request.method == 'POST':
        form = HobbyFilterForm(request.POST)
        if form.is_valid():
            selected_hobbies = form.cleaned_data.get('hobbies')
            if selected_hobbies:
                beitraege = [beitrag for beitrag in beitraege if beitrag['hobby'] in selected_hobbies]

    return render(request, 'hobbyHub/test.html', {'form': form, 'beitraege': beitraege})

# fügt einem beitrag einen kommentar hinzu
@login_required
def add_comment(request, beitrag_id):
    if request.method == 'POST':
        form = KommentarForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            posts = lade_json('posts.json')
            for beitrag in posts:
                if beitrag['id'] == beitrag_id:
                    kommentar = {
                        'benutzer': request.user.username,
                        'text': text,
                        'erstellt_am': datetime.now().isoformat()
                    }
                    beitrag.setdefault('comments', []).append(kommentar)
                    break
            speichere_json('posts.json', posts)
            return redirect('feed')
    return redirect('feed')
