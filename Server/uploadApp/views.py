from django.shortcuts import render
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
import os, json

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
            try:
                if len(werte) == 3:
                    titelliste.append(werte[0])  
                    dateiliste.append(datei)     
                    filterliste.append(werte[2]) 
                    textliste.append(werte[1])
            except:
                continue

        return render(request, r"uploadApp/test.html",
                      {}
                      )
    else:
        return render(request, r"uploadApp/upload.html", 
                      {}
                      )




def load(request): #Wenn der titel der key sein soll
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
                data = json.load(file)

        # Sicherstellen, dass text, titel und filter nicht None sind
        if text is None:
            text = ""
        if titel is None:
            titel = ""
        if not filter_values:
            filter_values = []

        # Daten hinzufügen
        data[titel] = [filename, text, filter_values]

        # Daten in JSON-Datei speichern
        with open(data_file_path, 'w') as file:
            json.dump(data, file, indent=2)

        titelliste = []
        dateiliste = []
        filterliste = []
        textliste = []

        # Daten für die Vorlage vorbereiten
        for titel, values in data.items():
            try:
                if titel in data:  # Sicherstellen, dass der Schlüssel vorhanden ist
                    titelliste.append(titel)
                    dateiliste.append(values[0])  # filename
                    filterliste.append(values[2])  # filter_values
                    textliste.append(values[1])    # text
            except:
                continue

        return render(request, r"uploadApp/test.html",
                        {})

    else:
        return render(request, r"uploadApp/upload.html", {})





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

        return render(request, r"uploadApp\test.html",
                      {
                          "antwort": "Datei wurde hochgeladen",
                          "bilderliste": bilderliste,
                          "textliste": textliste
                      })
    else:
        return render(request, r"uploadApp\test.html", 
                      {})
