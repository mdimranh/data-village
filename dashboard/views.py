from django.shortcuts import render

from .models import Privacy


def Dashboard(request):
    return render(request, 'dashboard/base.html')

def PrivacyView(request):
    if request.method == 'GET':
        privacy = Privacy.objects.first()
        if privacy is None:
            privacy = Privacy.objects.create(body="")
        context = {'privacy': privacy}
        return render(request, 'dashboard/meta/privacy.html', context=context)
    if request.method == 'POST':
        body = request.POST.get('body')
        editor_content = request.POST.get('editor_content')
        privacy = Privacy.objects.first()
        if privacy is None:
            privacy = Privacy.objects.create(body=editor_content)
        else:
            privacy.body = editor_content
            privacy.save()
        context = {'privacy': privacy}
        return render(request, 'dashboard/meta/privacy.html', context=context)
        