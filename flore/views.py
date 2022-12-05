from django.shortcuts import render
from http.client import HTTPResponse
from lodstorage.sparql import SPARQL
import ssl
import json
from urllib.error import HTTPError
from urllib.request import urlopen
import time
from .forms import ContactForm




def iiifmanifest(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            zoekterm = form.cleaned_data['zoekterm']
            ssl._create_default_https_context = ssl._create_unverified_context

            sparqlQuery = """
             PREFIX cidoc: <http://www.cidoc-crm.org/cidoc-crm/>
             SELECT DISTINCT ?o ?title FROM <http://stad.gent/ldes/dmg> WHERE {
             ?object cidoc:P129i_is_subject_of ?o .
             ?object cidoc:P102_has_title ?title.
             FILTER (regex(?title, "%s" , "i"))
             BIND(RAND() AS ?random) .
             } ORDER BY ?random
             LIMIT 20
             """ % (zoekterm,)
            sparql = SPARQL("https://stad.gent/sparql")
            qlod = sparql.queryAsListOfDicts(sparqlQuery)
            print(time.perf_counter())
            print(qlod)
            print(str(len(qlod)) + " gevonden objecten")
            if len(qlod) == 0:
                print("Te weinig objecten in de Collectie van de Gentenaar met dit woord in de titel :(. Probeer het opnieuw!")
                return render(request, "error.html")
            else:
                for i in range(len(qlod)):
                    try:
                        response = urlopen(qlod[i-1]['o'])
                    except ValueError:
                        pass
                    except HTTPError:
                        pass
                    else:
                        data_json = json.loads(response.read())
                        afbeelding = data_json["sequences"][0]['canvases'][0]["images"][0]["resource"]["@id"]
                        afbeelding1 = afbeelding.replace("full/full/0/default.jpg", "full/1000,/0/default.jpg")
                        manifestje = data_json["@id"]
                        objectnummer = manifestje.rpartition('/')[2]
                        webplatform = "https://data.collectie.gent/entity/" + objectnummer
                        titel = data_json["label"]['@value']
                        return render(request, 'flore.html', {'afbeelding1': afbeelding1, 'webplatform': webplatform, 'titel': titel, 'zoekterm': zoekterm})

    form = ContactForm()
    return render(request, 'form.html', {'form': form})



