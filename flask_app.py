from flask import Flask, render_template, jsonify, request, redirect, url_for
import datetime
from tester.runner import run_all_tests
from tester.client import APIClient

app = Flask(__name__)

@app.route("/")
@app.route("/dashboard")
def dashboard():
    """Affiche le dashboard principal (le stockage et rendu se font côté client)."""
    return render_template("dashboard.html")

@app.route("/run", methods=["POST", "GET"])
def trigger_run():
    """
    Déclenche une exécution de tests à la volée,
    et renvoie le rapport complet au format JSON.
    """
    report = run_all_tests()
    return jsonify(report)

@app.route("/health")
def health():
    """
    Endpoint de santé (/health) pour évaluer l'état
    de l'application Flask et de l'API Fruityvice externe.
    """
    health_status = {
        "status": "OK",
        "timestamp": datetime.datetime.now().isoformat(),
        "fruityvice_api": {
            "status": "UNKNOWN",
            "latency_ms": 0.0,
            "error": None
        }
    }
    
    # Vérification de l'API Fruityvice externe
    client = APIClient(base_url="https://www.fruityvice.com", timeout=3.0, max_retries=0)
    res = client.request("/api/fruit/banana")
    
    if res["success"]:
        health_status["fruityvice_api"]["status"] = "OK"
        health_status["fruityvice_api"]["latency_ms"] = round(res["latency_ms"], 1)
    else:
        health_status["status"] = "DEGRADED"
        health_status["fruityvice_api"]["status"] = "DOWN/UNREACHABLE"
        health_status["fruityvice_api"]["error"] = res["error"]
        
    return jsonify(health_status)

if __name__ == "__main__":
    # utile en local uniquement
    app.run(host="0.0.0.0", port=5000, debug=True)
