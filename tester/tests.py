def test_get_currencies(client):
    """Test 1: GET /currencies - Liste des devises supportées (Contrat de base)"""
    name = "GET /currencies (Contrat global)"
    endpoint = "GET /currencies"
    
    res = client.request("/currencies")
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
            "details": f"Format de réponse invalide: attendu un dictionnaire, obtenu {type(data).__name__}"
        }
        
    # Vérification de clés importantes
    expected_currencies = ["USD", "EUR", "GBP", "JPY", "CAD"]
    for cur in expected_currencies:
        if cur not in data:
            return {
                "name": name,
                "endpoint": endpoint,
                "status": "FAIL",
                "latency_ms": res["latency_ms"],
                "details": f"Devise majeure manquante dans la liste: '{cur}'"
            }
            
    return {
        "name": name,
        "endpoint": endpoint,
        "status": "PASS",
        "latency_ms": res["latency_ms"],
        "details": f"Succès: {len(data)} devises supportées et validées."
    }

def test_get_latest_rates(client):
    """Test 2: GET /latest - Taux de change actuels depuis EUR (Contrat Taux)"""
    name = "GET /latest (Taux de base EUR)"
    endpoint = "GET /latest"
    
    res = client.request("/latest")
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
            "details": "Format invalide"
        }
        
    # Vérification du contrat de structure
    required_keys = ["amount", "base", "date", "rates"]
    for key in required_keys:
        if key not in data:
            return {
                "name": name,
                "endpoint": endpoint,
                "status": "FAIL",
                "latency_ms": res["latency_ms"],
                "details": f"Clé obligatoire manquante : '{key}'"
            }
            
    if data["base"] != "EUR":
        return {
            "name": name,
            "endpoint": endpoint,
            "status": "FAIL",
            "latency_ms": res["latency_ms"],
            "details": f"Base incorrecte: attendu 'EUR', obtenu '{data['base']}'"
        }
        
    rates = data.get("rates", {})
    if "USD" not in rates or not isinstance(rates["USD"], (int, float)):
        return {
            "name": name,
            "endpoint": endpoint,
            "status": "FAIL",
            "latency_ms": res["latency_ms"],
            "details": "Taux USD absent ou au format invalide"
        }
        
    return {
        "name": name,
        "endpoint": endpoint,
        "status": "PASS",
        "latency_ms": res["latency_ms"],
        "details": f"Succès: Base EUR validée. Taux USD actuel : {rates['USD']}"
    }

def test_get_latest_from_usd(client):
    """Test 3: GET /latest?from=USD - Taux de change depuis USD (Paramétrage)"""
    name = "GET /latest?from=USD (Taux de change USD)"
    endpoint = "GET /latest?from=USD"
    
    res = client.request("/latest?from=USD")
    if not res["success"]:
        return {
            "name": name,
            "endpoint": endpoint,
            "status": "FAIL",
            "latency_ms": res["latency_ms"],
            "details": res["error"] or f"Status code: {res['status_code']}"
        }
        
    data = res["data"]
    if data.get("base") != "USD":
        return {
            "name": name,
            "endpoint": endpoint,
            "status": "FAIL",
            "latency_ms": res["latency_ms"],
            "details": f"Base incorrecte: attendu 'USD', obtenu '{data.get('base')}'"
        }
        
    rates = data.get("rates", {})
    if "EUR" not in rates:
        return {
            "name": name,
            "endpoint": endpoint,
            "status": "FAIL",
            "latency_ms": res["latency_ms"],
            "details": "Taux de retour vers EUR absent de la réponse"
        }
        
    return {
        "name": name,
        "endpoint": endpoint,
        "status": "PASS",
        "latency_ms": res["latency_ms"],
        "details": f"Succès: Base USD validée. Taux EUR : {rates['EUR']}"
    }

def test_get_conversion_amount(client):
    """Test 4: GET /latest?amount=100&from=EUR&to=USD - Conversion d'un montant (Calcul)"""
    name = "GET /latest?amount=100 (Conversion)"
    endpoint = "GET /latest?amount=100&from=EUR&to=USD"
    
    res = client.request("/latest?amount=100&from=EUR&to=USD")
    if not res["success"]:
        return {
            "name": name,
            "endpoint": endpoint,
            "status": "FAIL",
            "latency_ms": res["latency_ms"],
            "details": res["error"] or f"Status code: {res['status_code']}"
        }
        
    data = res["data"]
    if data.get("amount") != 100:
        return {
            "name": name,
            "endpoint": endpoint,
            "status": "FAIL",
            "latency_ms": res["latency_ms"],
            "details": f"Montant incorrect: attendu 100, obtenu {data.get('amount')}"
        }
        
    rates = data.get("rates", {})
    if "USD" not in rates or rates["USD"] <= 0:
        return {
            "name": name,
            "endpoint": endpoint,
            "status": "FAIL",
            "latency_ms": res["latency_ms"],
            "details": "Conversion USD invalide ou négative"
        }
        
    return {
        "name": name,
        "endpoint": endpoint,
        "status": "PASS",
        "latency_ms": res["latency_ms"],
        "details": f"Succès: 100 EUR convertis en {rates['USD']} USD."
    }

def test_get_historical_rates(client):
    """Test 5: GET /2020-01-01 - Taux de change historique spécifique (Historique)"""
    name = "GET /2020-01-01 (Taux Historique)"
    endpoint = "GET /2020-01-01"
    
    res = client.request("/2020-01-01")
    if not res["success"]:
        return {
            "name": name,
            "endpoint": endpoint,
            "status": "FAIL",
            "latency_ms": res["latency_ms"],
            "details": res["error"] or f"Status code: {res['status_code']}"
        }
        
    data = res["data"]
    date_val = data.get("date", "")
    
    # Le 1er Janvier étant férié, l'API renvoie le jour ouvré de bourse le plus proche (ex: 2019-12-31 ou 2020-01-02)
    if not (date_val.startswith("2020-01") or date_val.startswith("2019-12")):
        return {
            "name": name,
            "endpoint": endpoint,
            "status": "FAIL",
            "latency_ms": res["latency_ms"],
            "details": f"Date historique incohérente : attendu début '2020-01', obtenu '{date_val}'"
        }
        
    rates = data.get("rates", {})
    if "USD" not in rates:
        return {
            "name": name,
            "endpoint": endpoint,
            "status": "FAIL",
            "latency_ms": res["latency_ms"],
            "details": "Taux historique USD manquant"
        }
        
    return {
        "name": name,
        "endpoint": endpoint,
        "status": "PASS",
        "latency_ms": res["latency_ms"],
        "details": f"Succès: Historique validé (Date bourse : {date_val}, USD: {rates['USD']})."
    }

def test_get_invalid_route(client):
    """Test 6: GET /invalid_route_xyz - Vérification du comportement 404 (Entrée invalide)"""
    name = "GET /invalid_route (Robustesse 404)"
    endpoint = "GET /invalid_route_xyz"
    
    res = client.request("/invalid_route_xyz")
    status_code = res["status_code"]
    
    if status_code == 404:
        return {
            "name": name,
            "endpoint": endpoint,
            "status": "PASS",
            "latency_ms": res["latency_ms"],
            "details": "Succès: L'API renvoie correctement un code 404 attendu pour une route inconnue."
        }
    else:
        return {
            "name": name,
            "endpoint": endpoint,
            "status": "FAIL",
            "latency_ms": res["latency_ms"],
            "details": f"Comportement inattendu: attendu statut 404, obtenu {status_code}"
        }

def test_get_invalid_currency_code(client):
    """Test 7: GET /latest?from=INVALID - Code d'erreur 400 attendu pour paramètre invalide (Robustesse 400)"""
    name = "GET /latest?from=INVALID (Robustesse 400)"
    endpoint = "GET /latest?from=INVALID"
    
    res = client.request("/latest?from=INVALID")
    status_code = res["status_code"]
    
    if status_code in [400, 404]:
        return {
            "name": name,
            "endpoint": endpoint,
            "status": "PASS",
            "latency_ms": res["latency_ms"],
            "details": f"Succès: L'API rejette correctement le code devise invalide (statut HTTP {status_code} obtenu)."
        }
    else:
        return {
            "name": name,
            "endpoint": endpoint,
            "status": "FAIL",
            "latency_ms": res["latency_ms"],
            "details": f"Comportement inattendu: attendu statut 400 ou 404, obtenu {status_code}"
        }

def get_all_tests():
    """Retourne la liste des fonctions de test à exécuter."""
    return [
        test_get_currencies,
        test_get_latest_rates,
        test_get_latest_from_usd,
        test_get_conversion_amount,
        test_get_historical_rates,
        test_get_invalid_route,
        test_get_invalid_currency_code
    ]
