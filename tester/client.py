import urllib.request
import urllib.error
import time
import json

class APIClient:
    def __init__(self, base_url="https://api.frankfurter.app", timeout=3.0, max_retries=1):
        self.base_url = base_url
        self.timeout = timeout
        self.max_retries = max_retries
        self.headers = {
            "User-Agent": "Atelier-QoS-Tester/1.0",
            "Accept": "application/json"
        }

    def request(self, endpoint, method="GET", data=None):
        """
        Effectue une requête HTTP avec timeout, retries, et calcule de la latence.
        Retourne un dictionnaire standardisé :
        {
            "success": bool,
            "status_code": int,
            "data": dict/list ou None,
            "latency_ms": float,
            "error": str ou None
        }
        """
        url = f"{self.base_url.rstrip('/')}/{endpoint.lstrip('/')}"
        
        # Préparation des données si c'est un POST/PUT
        req_data = None
        if data is not None:
            req_data = json.dumps(data).encode("utf-8")
            self.headers["Content-Type"] = "application/json"
            
        retries = 0
        backoff = 1.0 # temps de pause en secondes avant retry

        while True:
            start_time = time.perf_counter()
            error_msg = None
            status_code = 0
            response_data = None
            success = False
            
            req = urllib.request.Request(url, data=req_data, headers=self.headers, method=method)
            
            try:
                # Execution de la requete
                with urllib.request.urlopen(req, timeout=self.timeout) as response:
                    status_code = response.status
                    body = response.read().decode("utf-8")
                    latency_ms = (time.perf_counter() - start_time) * 1000
                    
                    try:
                        response_data = json.loads(body)
                    except json.JSONDecodeError:
                        response_data = body # retourne la chaine brute si pas du JSON
                    
                    success = (200 <= status_code < 300)
                    
                    return {
                        "success": success,
                        "status_code": status_code,
                        "data": response_data,
                        "latency_ms": latency_ms,
                        "error": None
                    }
                    
            except urllib.error.HTTPError as e:
                # Erreurs HTTP (ex. 404, 429, 500)
                status_code = e.code
                latency_ms = (time.perf_counter() - start_time) * 1000
                error_msg = f"HTTP Error {status_code}: {e.reason}"
                
                # Lire le corps de l'erreur JSON s'il existe
                try:
                    error_body = e.read().decode("utf-8")
                    response_data = json.loads(error_body)
                except Exception:
                    response_data = None
                    
            except urllib.error.URLError as e:
                # Erreurs de connexion / DNS / timeout
                latency_ms = (time.perf_counter() - start_time) * 1000
                status_code = 0
                error_msg = f"Network/URL Error: {e.reason}"
                
            except Exception as e:
                # Autres erreurs inattendues
                latency_ms = (time.perf_counter() - start_time) * 1000
                status_code = 0
                error_msg = f"Unexpected Error: {str(e)}"

            # Gestion de la robustesse / Retry
            # Si code 429 (Rate Limit) ou 5xx (Server Error) ou timeout/connexion (status_code == 0)
            is_recoverable = (status_code == 0 or status_code == 429 or 500 <= status_code < 600)
            
            if is_recoverable and retries < self.max_retries:
                retries += 1
                # Si c'est un rate limit (429), on attend un peu plus longtemps
                sleep_time = backoff * 2 if status_code == 429 else backoff
                time.sleep(sleep_time)
                continue # Recommence la boucle
                
            # Si on a épuisé les retries ou si l'erreur n'est pas récupérable (ex. 404, 400)
            return {
                "success": False,
                "status_code": status_code,
                "data": response_data,
                "latency_ms": latency_ms,
                "error": error_msg
            }
