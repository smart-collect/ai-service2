import math

def calculer_distance_haversine(lat1, lng1, lat2, lng2):
    R = 6371.0  # Rayon de la Terre en kilomètres
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lng2 - lng1)
    
    a = math.sin(delta_phi / 2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def optimiser_plus_proche_voisin(bacs, depart_lat, depart_lng):
    bacs_a_collecter = [b for b in bacs if b.get("remplissage", 0) >= 70]
    tournee = []
    position_actuelle = (depart_lat, depart_lng)
    
    while bacs_a_collecter:
        prochain_bac = None
        distance_minimale = float('inf')
        for bac in bacs_a_collecter:
            dist = calculer_distance_haversine(position_actuelle[0], position_actuelle[1], bac["lat"], bac["lng"])
            if dist < distance_minimale:
                distance_minimale = dist
                prochain_bac = bac
        if prochain_bac:
            tournee.append(prochain_bac)
            position_actuelle = (prochain_bac["lat"], prochain_bac["lng"])
            bacs_a_collecter.remove(prochain_bac)
    return tournee

def calculer_distance_totale_tournee(tournee, start_lat, start_lng):
    if not tournee: return 0
    distance = calculer_distance_haversine(start_lat, start_lng, tournee[0]["lat"], tournee[0]["lng"])
    for i in range(len(tournee) - 1):
        distance += calculer_distance_haversine(tournee[i]["lat"], tournee[i]["lng"], tournee[i+1]["lat"], tournee[i+1]["lng"])
    return distance

def optimiser_2opt(tournee, start_lat, start_lng):
    meilleure_tournee = tournee[:]
    meilleure_distance = calculer_distance_totale_tournee(meilleure_tournee, start_lat, start_lng)
    ameliore = True
    while ameliore:
        ameliore = False
        for i in range(1, len(tournee) - 1):
            for j in range(i + 1, len(tournee)):
                nouvelle_tournee = meilleure_tournee[:]
                nouvelle_tournee[i:j] = reversed(meilleure_tournee[i:j])
                nouvelle_dist = calculer_distance_totale_tournee(nouvelle_tournee, start_lat, start_lng)
                if nouvelle_dist < meilleure_distance:
                    meilleure_tournee = nouvelle_tournee
                    meilleure_distance = nouvelle_dist
                    ameliore = True
        if not ameliore: break
    return meilleure_tournee
