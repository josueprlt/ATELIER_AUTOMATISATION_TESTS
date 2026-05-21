def test_get_all_fruits(client):
    """Test 1: GET /api/fruit/all - Vérifie la liste globale des fruits (contrat, types, présence)"""
    name = "GET /api/fruit/all (Contrat global)"
    endpoint = "GET /api/fruit/all"
    
    res = client.request("/api/fruit/all")
    if not res["success"]:
        return {
            "name": name,
            "endpoint": endpoint,
            "status": "FAIL",
            "latency_ms": res["latency_ms"],
            "details": res["error"] or f"Status code: {res['status_code']}"
        }
        
    data = res["data"]
    if not isinstance(data, list):
        return {
            "name": name,
            "endpoint": endpoint,
            "status": "FAIL",
            "latency_ms": res["latency_ms"],
            "details": f"Format invalide: attendu une liste, obtenu {type(data).__name__}"
        }
        
    if len(data) == 0:
        return {
            "name": name,
            "endpoint": endpoint,
            "status": "FAIL",
            "latency_ms": res["latency_ms"],
            "details": "La liste des fruits est vide"
        }
        
    # Vérification du schéma du premier élément
    first = data[0]
    required_keys = ["name", "id", "family", "genus", "order", "nutritions"]
    for key in required_keys:
        if key not in first:
            return {
                "name": name,
                "endpoint": endpoint,
                "status": "FAIL",
                "latency_ms": res["latency_ms"],
                "details": f"Clé manquante dans le contrat: '{key}'"
            }
            
    # Vérification des types
    if not isinstance(first["name"], str) or not isinstance(first["id"], int) or not isinstance(first["nutritions"], dict):
        return {
            "name": name,
            "endpoint": endpoint,
            "status": "FAIL",
            "latency_ms": res["latency_ms"],
            "details": "Types invalides pour les champs de base (name, id, ou nutritions)"
        }
        
    return {
        "name": name,
        "endpoint": endpoint,
        "status": "PASS",
        "latency_ms": res["latency_ms"],
        "details": f"Succès: {len(data)} fruits validés."
    }

def test_get_single_fruit_banana(client):
    """Test 2: GET /api/fruit/banana - Vérifie les détails d'un fruit spécifique (Banana)"""
    name = "GET /api/fruit/banana (Spécifique)"
    endpoint = "GET /api/fruit/banana"
    
    res = client.request("/api/fruit/banana")
    if not res["success"]:
        return {
            "name": name,
            "endpoint": endpoint,
            "status": "FAIL",
            "latency_ms": res["latency_ms"],
            "details": res["error"] or f"Status code: {res['status_code']}"
        }
        
    data = res["data"]
    if not isinstance(data, dict):
        return {
            "name": name,
            "endpoint": endpoint,
            "status": "FAIL",
            "latency_ms": res["latency_ms"],
            "details": f"Format invalide: attendu un dictionnaire, obtenu {type(data).__name__}"
        }
        
    # Vérification des valeurs de Banana
    expectations = {
        "name": "Banana",
        "genus": "Musa",
        "family": "Musaceae",
        "order": "Zingiberales"
    }
    
    for key, expected_val in expectations.items():
        if data.get(key) != expected_val:
            return {
                "name": name,
                "endpoint": endpoint,
                "status": "FAIL",
                "latency_ms": res["latency_ms"],
                "details": f"Valeur incorrecte pour '{key}': attendu '{expected_val}', obtenu '{data.get(key)}'"
            }
            
    # Vérification des nutritions
    nutritions = data.get("nutritions", {})
    required_nutritions = ["carbohydrates", "protein", "fat", "calories", "sugar"]
    for nut in required_nutritions:
        if nut not in nutritions:
            return {
                "name": name,
                "endpoint": endpoint,
                "status": "FAIL",
                "latency_ms": res["latency_ms"],
                "details": f"Clé nutritionnelle manquante: '{nut}'"
            }
            
    return {
        "name": name,
        "endpoint": endpoint,
        "status": "PASS",
        "latency_ms": res["latency_ms"],
        "details": "Succès: Contrat Banana 100% validé (Musa, Musaceae, Zingiberales)."
    }

def test_get_fruit_invalid(client):
    """Test 3: GET /api/fruit/invalid_fruit - Vérifie le cas d'erreur 404 (cas d'entrée invalide)"""
    name = "GET /api/fruit/invalid (Robustesse 404)"
    endpoint = "GET /api/fruit/invalid_fruit_name_xyz"
    
    res = client.request("/api/fruit/invalid_fruit_name_xyz")
    status_code = res["status_code"]
    
    if status_code == 404:
        return {
            "name": name,
            "endpoint": endpoint,
            "status": "PASS",
            "latency_ms": res["latency_ms"],
            "details": "Succès: Le serveur renvoie bien une erreur 404 attendue pour une entrée inconnue."
        }
    else:
        return {
            "name": name,
            "endpoint": endpoint,
            "status": "FAIL",
            "latency_ms": res["latency_ms"],
            "details": f"Comportement inattendu: attendu code 404, obtenu {status_code}"
        }

def test_get_family_rosaceae(client):
    """Test 4: GET /api/fruit/family/Rosaceae - Filtre par famille Rosaceae"""
    name = "GET /api/fruit/family/Rosaceae (Filtre)"
    endpoint = "GET /api/fruit/family/Rosaceae"
    
    res = client.request("/api/fruit/family/Rosaceae")
    if not res["success"]:
        return {
            "name": name,
            "endpoint": endpoint,
            "status": "FAIL",
            "latency_ms": res["latency_ms"],
            "details": res["error"] or f"Status code: {res['status_code']}"
        }
        
    data = res["data"]
    if not isinstance(data, list) or len(data) == 0:
        return {
            "name": name,
            "endpoint": endpoint,
            "status": "FAIL",
            "latency_ms": res["latency_ms"],
            "details": "Format invalide ou liste vide renvoyée pour la famille Rosaceae"
        }
        
    # Vérifier que tous les fruits ont la famille Rosaceae
    for fruit in data:
        if fruit.get("family") != "Rosaceae":
            return {
                "name": name,
                "endpoint": endpoint,
                "status": "FAIL",
                "latency_ms": res["latency_ms"],
                "details": f"Fruit '{fruit.get('name')}' appartient à la famille '{fruit.get('family')}' au lieu de Rosaceae"
            }
            
    return {
        "name": name,
        "endpoint": endpoint,
        "status": "PASS",
        "latency_ms": res["latency_ms"],
        "details": f"Succès: {len(data)} fruits validés dans la famille Rosaceae."
    }

def test_get_genus_fragaria(client):
    """Test 5: GET /api/fruit/genus/Fragaria - Filtre par genre Fragaria"""
    name = "GET /api/fruit/genus/Fragaria (Filtre)"
    endpoint = "GET /api/fruit/genus/Fragaria"
    
    res = client.request("/api/fruit/genus/Fragaria")
    if not res["success"]:
        return {
            "name": name,
            "endpoint": endpoint,
            "status": "FAIL",
            "latency_ms": res["latency_ms"],
            "details": res["error"] or f"Status code: {res['status_code']}"
        }
        
    data = res["data"]
    if not isinstance(data, list) or len(data) == 0:
        return {
            "name": name,
            "endpoint": endpoint,
            "status": "FAIL",
            "latency_ms": res["latency_ms"],
            "details": "Format invalide ou liste vide renvoyée pour le genre Fragaria"
        }
        
    # Vérifier que tous les fruits ont le genre Fragaria
    for fruit in data:
        if fruit.get("genus") != "Fragaria":
            return {
                "name": name,
                "endpoint": endpoint,
                "status": "FAIL",
                "latency_ms": res["latency_ms"],
                "details": f"Fruit '{fruit.get('name')}' appartient au genre '{fruit.get('genus')}' au lieu de Fragaria"
            }
            
    return {
        "name": name,
        "endpoint": endpoint,
        "status": "PASS",
        "latency_ms": res["latency_ms"],
        "details": f"Succès: {len(data)} fruits validés dans le genre Fragaria."
    }

def test_get_order_rosales(client):
    """Test 6: GET /api/fruit/order/Rosales - Filtre par ordre Rosales"""
    name = "GET /api/fruit/order/Rosales (Filtre)"
    endpoint = "GET /api/fruit/order/Rosales"
    
    res = client.request("/api/fruit/order/Rosales")
    if not res["success"]:
        return {
            "name": name,
            "endpoint": endpoint,
            "status": "FAIL",
            "latency_ms": res["latency_ms"],
            "details": res["error"] or f"Status code: {res['status_code']}"
        }
        
    data = res["data"]
    if not isinstance(data, list) or len(data) == 0:
        return {
            "name": name,
            "endpoint": endpoint,
            "status": "FAIL",
            "latency_ms": res["latency_ms"],
            "details": "Format invalide ou liste vide renvoyée pour l'ordre Rosales"
        }
        
    # Vérifier que tous les fruits ont l'ordre Rosales
    for fruit in data:
        if fruit.get("order") != "Rosales":
            return {
                "name": name,
                "endpoint": endpoint,
                "status": "FAIL",
                "latency_ms": res["latency_ms"],
                "details": f"Fruit '{fruit.get('name')}' appartient à l'ordre '{fruit.get('order')}' au lieu de Rosales"
            }
            
    return {
        "name": name,
        "endpoint": endpoint,
        "status": "PASS",
        "latency_ms": res["latency_ms"],
        "details": f"Succès: {len(data)} fruits validés dans l'ordre Rosales."
    }

def test_get_nutrition_calories(client):
    """Test 7: GET /api/fruit/calories?min=0&max=100 - Filtre par valeur nutritionnelle (calories)"""
    name = "GET /api/fruit/calories (QoS & Filtre)"
    endpoint = "GET /api/fruit/calories?min=0&max=100"
    
    res = client.request("/api/fruit/calories?min=0&max=100")
    if not res["success"]:
        return {
            "name": name,
            "endpoint": endpoint,
            "status": "FAIL",
            "latency_ms": res["latency_ms"],
            "details": res["error"] or f"Status code: {res['status_code']}"
        }
        
    data = res["data"]
    if not isinstance(data, list):
        return {
            "name": name,
            "endpoint": endpoint,
            "status": "FAIL",
            "latency_ms": res["latency_ms"],
            "details": "Format invalide renvoyé pour le filtre de calories (attendu une liste)"
        }
        
    # Vérifier que tous les fruits ont des calories entre 0 et 100
    for fruit in data:
        cals = fruit.get("nutritions", {}).get("calories")
        if cals is None or not (0 <= cals <= 100):
            return {
                "name": name,
                "endpoint": endpoint,
                "status": "FAIL",
                "latency_ms": res["latency_ms"],
                "details": f"Fruit '{fruit.get('name')}' a {cals} calories, hors intervalle [0, 100]"
            }
            
    return {
        "name": name,
        "endpoint": endpoint,
        "status": "PASS",
        "latency_ms": res["latency_ms"],
        "details": f"Succès: {len(data)} fruits dans la plage de calories [0-100]."
    }

def get_all_tests():
    """Retourne la liste des fonctions de test à exécuter."""
    return [
        test_get_all_fruits,
        test_get_single_fruit_banana,
        test_get_fruit_invalid,
        test_get_family_rosaceae,
        test_get_genus_fragaria,
        test_get_order_rosales,
        test_get_nutrition_calories
    ]
