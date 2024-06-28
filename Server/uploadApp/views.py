from django.shortcuts import render
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
import os, json, uuid
from django.conf import settings
from datetime import datetime


def upload(request):
    if request.method == "POST":
        myfile = request.FILES.get("file")
        text = request.POST.get("text")
        titel = request.POST.get("titel")
        filter_value = request.POST.get("tag") 

        if text is None:
            text = ""
        if filter_value is None:
            filter_value = ""

        if myfile:
            unique_filename = str(uuid.uuid4())
            _, file_extension = os.path.splitext(myfile.name)
            filename = unique_filename + file_extension.lower()

            fs = FileSystemStorage(location=os.path.join(settings.BASE_DIR, "uploadApp", "static", "data"))
            filename = fs.save(filename, myfile)
        else:
            filename = ""

        post_data = {
            "id": str(uuid.uuid4()), 
            "bild": filename,
            "text": text,
            "titel": titel,
            "filter": filter_value,
            "timestamp": datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]  # Remove microseconds
        }

        data_file_path = os.path.join(settings.BASE_DIR, 'uploadApp', 'data.json')

        if os.path.exists(data_file_path):
            with open(data_file_path, 'r') as file:
                try:
                    data = json.load(file)
                except json.JSONDecodeError:
                    data = []
        else:
            data = []

        data.append(post_data)

        with open(data_file_path, 'w') as file:
            json.dump(data, file, indent=2)

        with open(data_file_path, 'r') as file:
            data = json.load(file)

        return render(request, "uploadApp/feed.html", {'beitraege': data})

    else:
        return render(request, "uploadApp/upload.html", {})

