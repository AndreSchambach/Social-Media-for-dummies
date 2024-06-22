from django.shortcuts import render
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
import os, json

#1. os.listdir() -> Alle Dateien im Ordner
#2. Überprüfen was die größte Zahl ist (hier os.path.splitext(name)[1])
#3. Größte Zahl +1 als neue ID
#4. Dateiendung wieder hinzufügen (als string)
#5. myfile.name oder name verändern myfile.name = änderung

#Wenn eine Datei hochgeladen wird: 
#1. überprüft welche Dateinamen schon vergeben sind 
#2. Die Datei mit einer ID versehen die noch nicht vergeben ist 
#3. Die Datei mit der entsprechenden ID als Name gespeichert
#Wichtiger befehl: os.path.splitext(name)[1] anstelle von name der Bildname

#json datei mit Bildname + Kommentar {Bild.png: "hallo"}


def upload(request):
    print(os.getcwd())

    if request.method == "POST" and request.FILES.get("file"):
        myfile = request.FILES["file"]
        text = request.POST.get("text")
        titel = request.POST.get("titel")
        filter_values = request.POST.getlist("filter")  # Mehrere Checkbox-Werte

        fs = FileSystemStorage(os.path.join(os.getcwd(), "uploadApp/data"))
        dataPath = os.path.join(os.getcwd(), "uploadApp/data")

        if not os.path.exists(dataPath):
            os.makedirs(dataPath)

        dateien = os.listdir(dataPath)
        name = 0

        for dat in dateien:
            try:
                numb = int(os.path.splitext(dat)[0])
                if numb > name:
                    name = numb
            except ValueError:
                continue  # Wenn der Dateiname keine Zahl ist, überspringen

        # Generiere neuen Dateinamen
        myfile.name = str(name + 1) + "." + myfile.name.split(".")[-1]
        filename = fs.save(myfile.name, myfile)

        # Daten aus JSON-Datei laden oder leeres Dictionary erstellen
        data = {}
        data_file_path = 'uploadApp/data.json'
        if os.path.exists(data_file_path):
            with open(data_file_path, 'r') as file:
                data = json.loads(file.read())

        # Sicherstellen, dass text, titel und filter nicht None sind
        if text is None:
            text = ""
        if titel is None:
            titel = ""
        if not filter_values:
            filter_values = []

        # Daten hinzufügen
        data[filename] = [titel, text, filter_values]

        # Daten in JSON-Datei speichern
        with open(data_file_path, 'w') as file:
            json.dump(data, file, indent=2)

        titelliste = []
        dateiliste = []
        filterliste = []
        textliste = []

        # Daten für die Vorlage vorbereiten
        for datei, werte in data.items():
            if len(werte) == 3:
                titelliste.append(werte[0])  
                dateiliste.append(datei)     
                filterliste.append(werte[2]) 
                textliste.append(werte[1]) 

        return render(request, r"uploadApp/test.html",
                      {}
                      )
    else:
        return render(request, r"uploadApp/upload.html", 
                      {}
                      )





def home(request):
    print(os.getcwd())

    if request.method == "POST" and request.FILES.get("file"):
        myfile = request.FILES["file"]
        text = request.POST.get("text")
        fs = FileSystemStorage(os.path.join(os.getcwd(), "uploadApp/data"))
        dataPath = os.path.join(os.getcwd(), "uploadApp/data")

        Bilder = os.listdir(dataPath)
        name = 0

        for pic in Bilder:
            try:
                numb = int(os.path.splitext(pic)[0])
                if numb > name:
                    name = numb
            except ValueError:
                continue  # Wenn der Dateiname keine Zahl ist, überspringen

        myfile.name = str(name + 1) + "." + myfile.name.split(".")[-1]
        filename = fs.save(myfile.name, myfile)

        data = {}
        with open('uploadApp/data.json', 'r') as file:
            data = json.loads(file.read())
            data[filename] = text  # Hinweis: 'text' muss hier definiert werden

        with open('uploadApp/data.json', 'w') as file:
            json.dump(data, file, indent=2)

        bilderliste = []
        textliste = []

        for eintrag in data:
            bild = eintrag
            bilderliste.append(bild)
 
            text = data[eintrag]
            textliste.append(text)

        return render(request, r"\Users\sinan\Desktop\Server\uploadApp\templates\uploadApp\test.html",
                      {
                          "antwort": "Datei wurde hochgeladen",
                          "bilderliste": bilderliste,
                          "textliste": textliste
                      })
    else:
        return render(request, r"\Users\sinan\Desktop\Server\uploadApp\templates\uploadApp\test.html", 
                      {})