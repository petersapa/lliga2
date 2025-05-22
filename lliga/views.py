from django.shortcuts import render 
from django.http import HttpResponse

from .models import *

def classificacio(request):
    lliga = Lliga.objects.first()
    equips = lliga.equips.all()
    classi = []
 
    # calculem punts en llista de tuples (equip,punts)
    for equip in equips:
        punts = 0
        for partit in lliga.partits.filter(local=equip):
            if partit.gols_local() > partit.gols_visitant():
                punts += 3
            elif partit.gols_local() == partit.gols_visitant():
                punts += 1
        for partit in lliga.partits.filter(visitant=equip):
            if partit.gols_local() < partit.gols_visitant():
                punts += 3
            elif partit.gols_local() == partit.gols_visitant():
                punts += 1
        # si es posa tupla, ordenarà pel primer criteri
        classi.append( (punts,equip.nom) )
    # ordenem llista
    classi.sort(reverse=True)
    return render(request,"classificacio.html",
                {
                    "classificacio":classi,
                })