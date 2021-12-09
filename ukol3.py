import json
from pyproj import Transformer

with open ("adresy.geojson", encoding="utf-8") as adresy, open("kontejnery.geojson", encoding="utf-8") as kontajnery:
    for line in adresy:
        print(line)
