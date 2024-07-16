from django.shortcuts import render
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
import os, json
# Create your views here.

def home(request):
    print(os.getcwd())


    if request.method == "POST" and request.FILES["file"]:

        text = request.POST.get("text")
        print(text)

        myfile = request.FILES["file"]
        fs = FileSystemStorage(os.path.join(os.getcwd(), "uploadApp/data"))
        dataPath = os.path.join(os.getcwd(), "uploadApp/data")
        Bilder = os.listdir(dataPath)
        name = ""

        for pic in Bilder:
            numb = os.path.splitext(pic)[0] # [0] Index 0 von [Dateiname, Endung] = [Bild, .png]
        if numb > name:
            name = numb

            myfile.name = str(int(name) + 1) + "." + myfile.name.split(".")[-1]
            filename = fs.save(myfile.name, myfile)

        data = {}
        with open('uploadApp/data.json', 'r') as file:
            data = json.loads(file.read())
            data[filename] = text
        with open('uploadApp/data.json', 'w') as file:
            json.dump(data, file, indent = 2) #damit eingrückt wird und untereinander nach jedem dict-eintrag

        return HttpResponse("Datei hochgeladen")
        
    else:

        return render(request, r"C:\Users\Andre\OneDrive\Wichtig\Andre Schambach\Studium\Ubuntu Server\djangoproject\uploadApp\templates\uploadApp\test.html", {


        })
"""
Wenn eine Datei hochgeladen wird: 
1. überprüft welche Dateinamen schon vergeben sind 
2. Die Datei mit einer ID versehen die noch nicht vergeben ist 
3. Die Datei mit der entsprechenden ID als Name gespeichert
os.path.splittext (name)[1] #Sucht den LETZTEN "." im Dateiname (Bild.png)
"""

 
 #inhalt Ordner os.listdir()
 #Überprüfen  was die größte Zahl ist (os.path.splitext)
 #Größte Zahl +1 als neue id
 #Die Dateiendung hunzufügen (mit string)
 #Name ersetzen oder direkt (myfile.name) #name = name wird beibehalten
 #myfile.name = "4.png"