import json
from pyproj import Transformer
from statistics import mean, median
from math import sqrt

#def najmensia_vzdialenost():
#    if pomocna_vzdialenost > vzdialenost:
#        vzdialenost == pomocna_vzdialenost

wgs2jtsk = Transformer.from_crs(4326,5514,always_xy=True)           ### Transformacia na S-JTSK
vzdialenost = None                                                  
pomocna_vzdialenost = None                                          ### Premenne, s ktorymi sa vypocita najmensia vzdialenost ku kontajneru

with open ("adresy.geojson", encoding="utf-8") as adresy, open("kontejnery.geojson", encoding="utf-8") as kontajnery:
    
    data_adresy = json.load(adresy)                 ### Nacitanie dat zo suborov
    data_kontajnery = json.load(kontajnery)
    
    for adresa in range(len(data_adresy["features"])):                                  ### Pre kazdu adresu sa na zaciatok nacitaju jej suradnice zo suboru a transformuju sa do S-JTSK
        krovak_x = data_adresy["features"][adresa]["geometry"]["coordinates"][0]
        krovak_y = data_adresy["features"][adresa]["geometry"]["coordinates"][1]       
        krovak = wgs2jtsk.transform(krovak_x,krovak_y)
        
        for kontajner in range(len(data_kontajnery["features"])):                               ### Cyklus pre prechadzanie kazdym kontajnerom
            if data_kontajnery["features"][kontajner]["properties"]["PRISTUP"] == "volně":
                dlz_x = data_kontajnery["features"][kontajner]["geometry"]["coordinates"][0]
                dlz_y = data_kontajnery["features"][kontajner]["geometry"]["coordinates"][1]
                vzdialenost = int(sqrt((krovak[0]-dlz_x)**2+(krovak[1]-dlz_y)**2))              ### Vypocet vzdialenosti cez Pytagorovu vetu

                if pomocna_vzdialenost == None or pomocna_vzdialenost > vzdialenost:
                    pomocna_vzdialenost = vzdialenost                                           ### Zachovanie najmensej vzdialenosti

        
        data_adresy["features"][adresa]["k_najblizsiemu_kontajneru"] = pomocna_vzdialenost      ### Do slovnika sa k danej adrese pripise novy kluc s najmensou vzdialenostou
        pomocna_vzdialenost = None                                                              ### Pomocna vzdialenost sa vynuluje pre pracu s dalsou adresou
    
    vzdialenosti = [adresa["k_najblizsiemu_kontajneru"] for adresa in data_adresy["features"]]  ### Premenna, do ktorej sa nacita zoznam vypocitanych najmensich vzdialenosti
    
    najdi_index = (vzdialenosti.index(max(vzdialenosti)))

    print(f"Priemerna vzdialenost ku kontajnerom je: {round(mean(vzdialenosti),2)}.")            
    print(f"Median vzdialenosti ku kontajnerom je: {int(median(vzdialenosti))}.")                ### Pouzitie kniznice statistics pre jednoduchy priemer a median
    print("Najdalej od kontajneru vo vzdialenosti {max_vzdialenost} je vchod na adrese {adresa} {cd}".format(max_vzdialenost = max(vzdialenosti),adresa = data_adresy["features"][najdi_index]["properties"]["addr:street"],cd = data_adresy["features"][najdi_index]["properties"]["addr:housenumber"]))
