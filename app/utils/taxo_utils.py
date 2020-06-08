def count_genera(species):
    genera = []
    for single_species in species:
        genera.append(single_species.split(" ")[0])
    genera = list(set(genera))
    return len(genera)