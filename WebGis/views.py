from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, render_to_response
from django.http import HttpRequest, HttpResponse
from django.http import JsonResponse
from WebGis.models import *
from django.forms.models import model_to_dict


def home(request):
    assert(isinstance(request, HttpRequest))
    return render(request, 'Main_Win.html')


def search_cell(request):
    if request.method == 'POST':
        string = request.POST['phrase']
        rez = []
        try:
            int(string)
            bazne = Bazne.objects.filter(cell_id__startswith=string)  # cell_id is a string
            if len(bazne) > 0:
                rez = [model_to_dict(bazna, ['name', 'cell_id', 'lat', 'lon', 'pow', 'azimuth']) for bazna in bazne]
        except ValueError:
            bazne = Bazne.objects.filter(name__icontains=string)
            if len(bazne) > 0:
                rez = [model_to_dict(bazna, ['name', 'cell_id', 'lat', 'lon', 'pow', 'azimuth']) for bazna in bazne]
        return JsonResponse({"items": rez})
        # return JsonResponse({"items": ["red", "yellow", "brown"],})


def lock_mngr(request):
    if request.method == 'POST':
        cmd = request.POST['cmd']   # {cmd: add/remove/list, cell_id: cell_id}
        if cmd =='add':
            id = request.POST['cell_id']
            Bazne.objects.filter(cell_id=id).update(lock=True)
            return HttpResponse()

        elif cmd == 'remove':
            cell_id = request.POST['cell_id']
            if cell_id == 'all':
                Bazne.objects.filter(lock=True).update(lock=False)
            else:
                Bazne.objects.filter(cell_id=cell_id).update(lock=False)
            return HttpResponse()

        elif cmd == 'list':
            bazne = Bazne.objects.filter(lock=True)
            if len(bazne):
                bazna_js = {'cells': [model_to_dict(bazna, ['name', 'cell_id', 'lat', 'lon']) for bazna in bazne]}
                return JsonResponse(bazna_js)
            else:
                return HttpResponse()

        else:
            return HttpResponse('WTF!?')

