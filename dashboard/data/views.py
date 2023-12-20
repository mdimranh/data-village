from django.shortcuts import render

from apps.data.models import Folder


def DataView(request, *args, **kwargs):
    colors = ["#4B5563", "#E02424", "#9F580A", "#057A55", "#1C64F2", "#5850EC", "#7E3AF2", "#D61F69"]
    if request.method == "GET":
        folders = Folder.objects.all()
        return render(request, 'dashboard/data/datas.html', {'folders': folders, "colors": colors})

    if request.method == 'POST':
        if request.htmx:
            data = {
                "name": request.POST.get("name"),
                "premium": request.POST.get("premium") == "yes",
                "color": request.POST.get("color")
            }
            folder = Folder(**data)
            folder.save()
            folders = Folder.objects.all()
            
            return render(request, 'dashboard/data/folders.html', {'folders': folders, "colors": colors})