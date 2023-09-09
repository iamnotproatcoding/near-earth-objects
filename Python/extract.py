import csv
import json
from models import NearEarthObject, CloseApproach

def load_neos(neo_csv_path):
    with open(neo_csv_path, "r") as infile:
        reader = csv.DictReader(infile)
        neos = []
        for line in reader:
            line["name"] = line["name"] or None
            line["diameter"] = float(line["diameter"]) if line["diameter"] else None
            line["pha"] = False if line["pha"] in ["", "N"] else True
            try:
                neo = NearEarthObject(
                    designation = line["pdes"],
                    name = line["name"],
                    diameter = line["diameter"],
                    hazardous = line["pha"],
                )
            except Exception as e:
                print(e)
            else:
                neos.append(neo)
    return neos

def load_approaches(cad_json_path):
    with open(cad_json_path, "r") as infile:
        reader = json.load(infile)
        reader = [dict(zip(reader["fields"], data)) for data in reader["data"]]
        approaches = []
        for line in reader:
            try:
                approach = CloseApproach(
                    designation=line["des"],
                    time=line["cd"],
                    distance=float(line["dist"]),
                    velocity=float(line["v_rel"]),
                )
            except Exception as e:
                print(e)
            else:
                approaches.append(approach)
    return approaches