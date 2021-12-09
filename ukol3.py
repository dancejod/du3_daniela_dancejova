import json
from pyproj import Transformer
import requests
from math import sqrt

#def najmensia_vzdialenost():
    #if 

wgs2jtsk = Transformer.from_crs(4326,5514,always_xy=True)
vzdialenost = None

with open ("adresy.geojson", encoding="utf-8") as adresy, open("kontejnery.geojson", encoding="utf-8") as kontajnery:
    
    data_adresy = json.load(adresy)
    data_kontajnery = json.load(kontajnery)
    
    for adresa in range(len(data_adresy["features"])):
        #print(data_adresy["features"][adresa]["properties"]["addr:street"], end=" "), print(data_adresy["features"][adresa]["properties"]["addr:housenumber"])
        krovak = wgs2jtsk.transform((data_adresy["features"][adresa]["geometry"]["coordinates"][1]),(data_adresy["features"][adresa]["geometry"]["coordinates"][0]))
        
        for kontajner in range(len(data_kontajnery["features"])):
            if data_kontajnery["features"][kontajner]["properties"]["PRISTUP"] == "volně":
                dlz_x = data_kontajnery["features"][kontajner]["geometry"]["coordinates"][0]
                dlz_y = data_kontajnery["features"][kontajner]["geometry"]["coordinates"][1]

                if vzdialenost == None:
                    vzdialenost = sqrt((krovak[0]-dlz_x)**2+(krovak[0]-dlz_y)**2) 
                    print(vzdialenost)