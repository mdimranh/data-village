import os
import time

from django.core.files.storage import default_storage
from django.db.models import FileField
from django.db.models.signals import post_delete
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render

from apps.data.models import File, FilePackage, Folder


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
                # "color": request.POST.get("color"),
            }
            folder = Folder(**data)
            folder.save()
            folders = Folder.objects.filter(parent__isnull=True)

            return render(
                request,
                "dashboard/data/folders.html",
                {"folders": folders, "parent": True},
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
                "files": FilePackage.objects.filter(folder__id=fid),
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
                "parent": Folder.objects.get(id=fid),
            }
            folder = Folder(**data)
            folder.save()

            return render(
                request,
                "dashboard/data/folders.html",
                {
                    "folders": Folder.objects.filter(parent__id=fid),
                    "files": FilePackage.objects.filter(folder__id=fid),
                    "parent_id": fid,
                },
            )


def DeleteFolder(request, **kwargs):
    if request.method == "DELETE" and request.htmx:
        id = request.GET.get("id")
        folder = Folder.objects.filter(id=id).first()
        if folder is None:
            return HttpResponseNotFound("Folder not found")
        else:
            folder.delete()
            if folder.parent is not None:
                folders = Folder.objects.filter(parent__id=folder.parent.id)
                return render(
                    request,
                    "dashboard/data/folders.html",
                    {
                        "folders": folders,
                        "parent_id": folder.parent.id,
                    },
                )
            else:
                folders = Folder.objects.filter(parent__isnull=True)
                return render(
                    request,
                    "dashboard/data/folders.html",
                    {"folders": folders, "parent": True},
                )
            return HttpResponse("Folder deleted successfully")


def AddFile(request, id):
    if request.method == "POST" and request.htmx:
        data = request.POST
        errors = {}
        files = request.FILES.getlist("file")
        name = data.get("name")
        if name == "":
            errors["name"] = "This field is required"
        if errors:
            response = render(
                request,
                "dashboard/data/forms/inputs.html",
                {"parent_id": id, "errors": errors},
            )
            response["HX-Retarget"] = "#addfile-inputs"
            response["HX-Reswap"] = "innerHTML"
            return response
        folder = Folder.objects.filter(id=id).first()
        free = data.get("free") == "yes"
        newPackage = FilePackage(name=name, premium=not free, folder=folder)
        newPackage.save()
        for file in files:
            name, extension = os.path.splitext(file.name)
            newfile = File(
                file=file, size=file.size, type=extension, package=newPackage, name=name
            )
            newfile.save()
        files = FilePackage.objects.filter(folder__id=id)
        folders = Folder.objects.filter(parent__isnull=True)
        return render(
            request,
            "dashboard/data/folders.html",
            {"files": files, "parent_id": id},
        )


def FileDetails(request, id):
    if request.method == "GET":
        file = FilePackage.objects.filter(id=id).first()
        return render(
            request,
            "dashboard/data/forms/edit-file-inputs.html",
            {
                "file": file
            }
        )
    if request.method == 'DELETE':
        file = File.objects.filter(id=id).first()
        if file:
            file.delete()
            return HttpResponse("")
    if request.method == 'POST':
        data = request.POST
        print(data)
        package = FilePackage.objects.filter(id=id).first()
        files = request.FILES.getlist("file")
        name = data.get("name")
        if name:
            package.name = name
        free = data.get("free") == "yes"
        package.premium = not free
        package.save()
        for file in files:
            name, extension = os.path.splitext(file.name)
            newfile = File(
                file=file, size=file.size, type=extension, package=package, name=name
            )
            newfile.save()
        return render(
            request,
            "dashboard/data/folders.html",
            {"files": FilePackage.objects.filter(folder=package.folder), "parent_id": package.folder.id},
        )

def FolderDetails(request, id):
    if request.method == "GET":
        folder = Folder.objects.filter(id=id).first()
        return render(
            request,
            "dashboard/data/forms/edit-folder-inputs.html",
            {
                "folder": folder
            }
        )
    if request.method == 'POST':
        data = request.POST
        folder = Folder.objects.filter(id=id).first()
        name = data.get("name")
        if name:
            folder.name = name
        free = data.get("free") == "yes"
        folder.premium = not free
        folder.save()
        context = {}
        if folder.parent:
            context['folders'] = Folder.objects.filter(parent__id=folder.parent.id)
            context['parent_id'] = folder.parent.id
        else:
            context['folders'] = Folder.objects.filter(parent__isnull=True)
            context['files'] = []
            context['parent_id'] = None
        return render(
            request,
            "dashboard/data/folders.html",
            context
        )

def DeleteFile(request, **kwargs):
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
        file = FilePackage.objects.filter(
            id=id
        ).first()  # Use first() to get the first object in the queryset
        if file is None:
            return HttpResponseNotFound(
                "File not found"
            )  # Return 404 response if folder is not found
        else:
            folder = Folder.objects.filter(id=file.folder.id).first()
            file.delete()
            context = {
                "parent_id": folder.id,
            }
            files = FilePackage.objects.filter(folder__id=folder.id)
            if files:
                context["files"] = files
            context["folders"] = Folder.objects.filter(parent__id=folder.id)
            return render(request, "dashboard/data/folders.html", context)
            return HttpResponse("File deleted successfully")


# def file_cleanup(sender, **kwargs):
#     for fieldname in sender._meta.get_all_field_names():
#         try:
#             field = sender._meta.get_field(fieldname)
#         except:
#             field = None

#         if field and isinstance(field, FileField):
#             inst = kwargs["instance"]
#             f = getattr(inst, fieldname)
#             m = inst.__class__._default_manager
#             if (
#                 hasattr(f, "path")
#                 and os.path.exists(f.path)
#                 and not m.filter(
#                     **{"%s__exact" % fieldname: getattr(inst, fieldname)}
#                 ).exclude(pk=inst._get_pk_val())
#             ):
#                 try:
#                     default_storage.delete(f.path)
#                 except:
#                     pass


# post_delete.connect(file_cleanup, sender=File)