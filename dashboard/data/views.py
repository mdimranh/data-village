import time

from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render

from apps.data.models import File, Folder


def DataView(request, *args, **kwargs):
    colors = [
        "#4B5563",
        "#E02424",
        "#9F580A",
        "#057A55",
        "#1C64F2",
        "#5850EC",
        "#7E3AF2",
        "#D61F69",
    ]
    if request.method == "GET":
        folders = Folder.objects.filter(parent__isnull=True)
        return render(
            request,
            "dashboard/data/datas.html",
            {"folders": folders, "colors": colors, "parent": True},
        )

    if request.method == "POST":
        if request.htmx:
            data = {
                "name": request.POST.get("name"),
                "premium": request.POST.get("premium") == "yes",
                "color": request.POST.get("color"),
            }
            folder = Folder(**data)
            folder.save()
            folders = Folder.objects.filter(parent__isnull=True)

            return render(
                request,
                "dashboard/data/folders.html",
                {"folders": folders, "colors": colors, "parent": True},
            )


def SubFolder(request, fid, **kwargs):
    colors = [
        "#4B5563",
        "#E02424",
        "#9F580A",
        "#057A55",
        "#1C64F2",
        "#5850EC",
        "#7E3AF2",
        "#D61F69",
    ]
    if request.method == "GET":
        folder = Folder.objects.filter(id=fid).first()
        return render(
            request,
            "dashboard/data/datas.html",
            {
                "folders": Folder.objects.filter(parent__id=fid),
                "files": File.objects.filter(folder__id=fid),
                "colors": colors,
                "sequence": folder.sequence,
                "parent_id": fid,
            },
        )

    if request.method == "POST":
        if request.htmx:
            data = {
                "name": request.POST.get("name"),
                "premium": request.POST.get("premium") == "yes",
                "color": request.POST.get("color"),
                "parent": Folder.objects.get(id=fid),
            }
            folder = Folder(**data)
            folder.save()

            return render(
                request,
                "dashboard/data/folders.html",
                {
                    "folders": Folder.objects.filter(parent__id=fid),
                    "files": File.objects.filter(folder__id=fid),
                    "colors": colors,
                    "parent_id": fid,
                },
            )


def DeleteFolder(request, **kwargs):
    colors = [
        "#4B5563",
        "#E02424",
        "#9F580A",
        "#057A55",
        "#1C64F2",
        "#5850EC",
        "#7E3AF2",
        "#D61F69",
    ]
    if request.method == "DELETE":
        # time.sleep(5)
        id = request.GET.get("id")
        folder = Folder.objects.filter(
            id=id
        ).first()  # Use first() to get the first object in the queryset
        if folder is None:
            return HttpResponseNotFound(
                "Folder not found"
            )  # Return 404 response if folder is not found
        else:
            folder.delete()
            if folder.parent is not None:
                return render(
                    request,
                    "dashboard/data/folders.html",
                    {
                        "folders": Folder.objects.filter(parent__id=folder.parent.id),
                        "colors": colors,
                        "parent_id": fid,
                    },
                )
            else:
                folders = Folder.objects.filter(parent__isnull=True)
                return render(
                    request,
                    "dashboard/data/folders.html",
                    {"folders": folders, "colors": colors, "parent": True},
                )
            return HttpResponse("Folder deleted successfully")


def AddFile(request, id):
    colors = [
        "#4B5563",
        "#E02424",
        "#9F580A",
        "#057A55",
        "#1C64F2",
        "#5850EC",
        "#7E3AF2",
        "#D61F69",
    ]
    if request.method == "POST":
        data = request.POST
        file = request.FILES["file"]
        folder = Folder.objects.filter(id=id).first()
        newfile = File(
            name=file.name, file=file, permium=False, folder=folder, size=10.5
        )
        newfile.save()
        files = File.objects.filter(folder__id=id)
        return render(
            request,
            "dashboard/data/folders.html",
            {"files": files, "colors": colors, "parent_id": id},
        )
