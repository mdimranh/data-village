from django.http import FileResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from apps.data.models import File, FilePackage, Folder


def datas(request, id=None):
    context = {}
    if id:
        folder = Folder.objects.filter(id=id).first()
        folders = Folder.objects.filter(parent__id=id)
        context["folders"] = folders
        files = FilePackage.objects.filter(folder__id=id)
        context["files"] = files
        context["sequence"] = folder.sequence if folder else None
    else:
        folders = Folder.objects.filter(parent__isnull=True)
        context["folders"] = folders
        context["parent"] = True
    if request.htmx:
        return render(
            request,
            "data/folders.html",
            context,
        )
    return render(
        request,
        "data/datas.html",
        context,
    )
    # return render(request, "data/datas.html")


def data(request, type):
    if type == "xlsx":
        context = {"xlsx": True}
    else:
        context = {"xlsx": False}
    return render(request, "files/viewer1.html", context)


def fileView(request, id):
    package = FilePackage.objects.filter(id=id).first()
    file = File.objects.filter(package__id=id, type=".pdf").first()
    files = File.objects.filter(package__id=id).values("file", "type")
    package.view += 1
    package.save()
    return render(request, "files/file_view.html", {"file": file, "files": files})


def fileDownload(request, id):
    file = File.objects.filter(id=id, type=".pdf").first()
    response = FileResponse(open(file.file, "rb"))
