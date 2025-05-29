from django.shortcuts import render, redirect 
from django.http import HttpResponse
from django import forms


from .models import *

class MenuForm(forms.Form):
    lliga = forms.ModelChoiceField(queryset=Lliga.objects.all())

def classificacio_menu(request):
    queryset = Lliga.objects.all()
    #form = MenuForm()
    #return render(request, "classificacio_menu.html", {"lligues":queryset, "form": form})
    if request.method == "POST":
        form = MenuForm(request.POST)
        if form.is_valid():
            lliga = form.cleaned_data.get("lliga")
            # cridem a /classificacio/<lliga_id>
            return redirect('classificacio',lliga.id)

    form = MenuForm()
    return render(request, "classificacio_menu.html",{
                    "lligues": queryset,
                    "form": form,
            })

def classificacio(request, lliga_id):
    #lliga = Lliga.objects.first()
    #lliga = Lliga.objects.last()
    lliga = Lliga.objects.get(pk=lliga_id)
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
                    "lliga":lliga.nom,
                    "classificacio":classi,
                })



class EquipForm(forms.ModelForm):
    class Meta:
        model = Equip
        exclude = ()

def crea_equip(request):
    form = EquipForm()
    if request.method == "POST":
        form = EquipForm(request.POST)
        if form.is_valid():
            # TODO: verificar que el nom de l'equip no existeixi
            equips = Equip.objects.filter(nom=form.cleaned_data.get("nom"))
            if (equips.count() > 0):
                return HttpResponse("ERROR: nom repetit");
            form.save()

    return render(request,"crea_equip.html",
                {
                    "form":form
                })