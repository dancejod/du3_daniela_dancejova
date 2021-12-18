import json
from pyproj import Transformer
from statistics import mean, median
from math import sqrt
import sys
from json.decoder import JSONDecodeError

wgs2jtsk = Transformer.from_crs(4326,5514,always_xy=True)           ### Transformacia na S-JTSK
vzdialenost = None                                                  
pomocna_vzdialenost = None
najblizsi_kontajner = None                                          ### Premenne, s ktorymi sa vypocita najmensia vzdialenost ku kontajneru
do_geojsonu = []                                                    ### Zoznam, ktory posluzi na ulozenie adries do noveho suboru GEOJSON

try:
    with open ("adresy.geojson", encoding="utf-8") as adresy:
        data_adresy  =json.load(adresy)                             ### Nacitanie adries zo suboru  

except FileNotFoundError:
    sys.exit("Vstupny subor adries neexistuje. Skontroluj, ci sa subor nachadza v rovnakom adresari ako tento skript a je pomenovany spravne.")

except IOError:
    sys.exit("Subor adries sa neda precitat. Prosim opravte ho a spustite skript znova.")
    
except PermissionError:
    sys.exit("Skript nema opravnenie otvorit subor s adresami.")

except JSONDecodeError:
    sys.exit("Vstupny subor s adresami nie je validny. Prosim skontrolujte ho a opravte ho.")

except:
    sys.exit("Nieco sa nepodarilo, program sa teraz ukonci.")

try:
    with open("kontejnery.geojson", encoding="utf-8") as kontajnery:  
        data_kontajnery = json.load(kontajnery)                             ### Nacitanie kontajnerov zo suboru

except FileNotFoundError:
    sys.exit("Vstupny subor s kontajnermi neexistuje. Skontrolujte, ci sa subor nachadza v rovnakom adresari ako tento skript a je pomenovany spravne.")

except IOError:
    sys.exit("Subor s kontajnermi sa neda precitat. Prosim opravte ho a spustite skript znova.")
    
except PermissionError:
    sys.exit("Skript nema opravnenie otvorit subor s kontajnermi.")

except JSONDecodeError:
    sys.exit("Vstupny subor s kontajnermi nie je validny. Prosim skontrolujte ho a opravte ho.")

except:
    sys.exit("Nieco sa nepodarilo, program sa teraz ukonci.")

print("Nacitanych {pocet_adries} adresnych bodov.".format(pocet_adries = len(data_adresy["features"])))
print("Nacitanych {pocet_kontajnerov} kontajnerov na triedeny odpad.".format(pocet_kontajnerov = len(data_kontajnery["features"])))
print("Program teraz vypocitava vzdialenosti vchodov od kontajnerov . . .")

try:       
    for adresa in data_adresy["features"]:                                  ### Pre kazdu adresu sa na zaciatok nacitaju jej suradnice zo suboru a transformuju sa do S-JTSK
        krovak_x = adresa["geometry"]["coordinates"][0]
        krovak_y = adresa["geometry"]["coordinates"][1]       
        krovak = wgs2jtsk.transform(krovak_x,krovak_y)
        aktualna_adresa = "{ulica} {cislo}".format(ulica = adresa["properties"]["addr:street"], cislo = adresa["properties"]["addr:housenumber"])      ### Nacita sa sformatovana adresa
                
        for kontajner in data_kontajnery["features"]:                               ### Cyklus pre prechadzanie kazdym kontajnerom
            aktualny_kontajner = kontajner["properties"]["ID"]                      ### Nacita sa ID aktualne spracovaneho kontajneru
                    
            if kontajner["properties"]["PRISTUP"] == "volně":
                dlz_x = kontajner["geometry"]["coordinates"][0]
                dlz_y = kontajner["geometry"]["coordinates"][1]
                vzdialenost = float(sqrt((krovak[0]-dlz_x)**2+(krovak[1]-dlz_y)**2))              ### Vypocet vzdialenosti cez Pytagorovu vetu

                if pomocna_vzdialenost == None or pomocna_vzdialenost > vzdialenost:
                    pomocna_vzdialenost = vzdialenost                                           ### Zachovanie najmensej vzdialenosti
                    najblizsi_kontajner = aktualny_kontajner                                    ### Zachova sa ID kontajneru, kde bola najmensia vzdialenost od vchodu

            elif kontajner["properties"]["PRISTUP"] == "obyvatelům domu":
                if aktualna_adresa == kontajner['properties']['STATIONNAME']:                   ### Porovna sa sformatovana adresa s polohou kontajneru, ak je zhoda, vzdialenosti sa priradi 0
                    pomocna_vzdialenost = 0
                else:
                    pass
        
        if pomocna_vzdialenost > 10000:
            sys.exit("Najblizsi kontajner je dalej ako 10 km, program to nedava.")
        adresa["k_najblizsiemu_kontajneru"] = round(pomocna_vzdialenost)                               ### Do slovnika sa k danej adrese pripise novy kluc s najmensou vzdialenostou
        adresa["properties"]["kontejner"] = najblizsi_kontajner                                 ### Podobne sa k atributom adresy pripise novy kluc s ID najblizsieho kontajnera
        pomocna_vzdialenost = None                                                              ### Pomocna vzdialenost sa vynuluje pre pracu s dalsou adresou
        do_geojsonu.append(adresa)                                                              ### Do zoznamu sa zavola spracovana adresa

except KeyError:
    sys.exit("Subor nema vsetky pozadovane atributy, prosim opravte ho a nacitajte skript znova.")

with open("adresy_kontejnery.geojson","w", encoding="utf-8") as out:                        ### Zoznam s adresami sa hodi do novovytvoreneho suboru s jednoduchym formatovanim
    json.dump(do_geojsonu, out, ensure_ascii = False, indent = 2)
        
vzdialenosti = [adresa["k_najblizsiemu_kontajneru"] for adresa in data_adresy["features"]]  ### Premenna, do ktorej sa nacita zoznam vypocitanych najmensich vzdialenosti
najdi_index = (vzdialenosti.index(max(vzdialenosti)))                                       ### Najde sa index hodnoty s najvacsou vzdialenostou od kontajneru, aby sa tak nasla aj adresa miesta

print(f"Priemerna vzdialenost ku kontajnerom je: {round(mean(vzdialenosti),1)} m")            
print(f"Median vzdialenosti ku kontajnerom je: {round(median(vzdialenosti))}")                ### Pouzitie kniznice statistics pre jednoduchy priemer a median
print("Najdalej od kontajneru vo vzdialenosti {max_vzdialenost} m je vchod na adrese {adresa} {cd}".format(max_vzdialenost = max(vzdialenosti),adresa = data_adresy["features"][najdi_index]["properties"]["addr:street"],cd = data_adresy["features"][najdi_index]["properties"]["addr:housenumber"]))
