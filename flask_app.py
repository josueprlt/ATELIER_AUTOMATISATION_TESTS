from flask import Flask, render_template, jsonify, request, redirect, url_for, make_response
import sqlite3
import json
import os
import datetime

import storage
from tester.runner import run_all_tests
from tester.client import APIClient

app = Flask(__name__)

# Initialise la base de données SQLite au démarrage
storage.init_db()

@app.route("/")
@app.route("/dashboard")
def dashboard():
    """Affiche le dashboard principal."""
    # Récupérer l'historique complet pour les graphiques et le tableau
    runs = storage.get_all_runs(limit=100)
    latest_run = storage.get_latest_run()
    
    # Calculer des statistiques globales
    total_runs = len(runs)
    avg_latency_global = 0.0
    avg_success_rate_global = 0.0
    
    if total_runs > 0:
        avg_latency_global = sum(r["latency_avg"] for r in runs) / total_runs
        avg_success_rate_global = sum(r["success_rate"] for r in runs) / total_runs
        
    return render_template(
        "dashboard.html",
        latest_run=latest_run,
        runs=runs,
        total_runs=total_runs,
        avg_latency_global=round(avg_latency_global, 1),
        avg_success_rate_global=round(avg_success_rate_global, 1)
    )

@app.route("/run", methods=["POST", "GET"])
def trigger_run():
    """
    Déclenche une exécution de tests à la volée,
    enregistre le run dans SQLite et renvoie le rapport.
    """
    # Mesurer si c'est un call AJAX ou non
    is_ajax = request.headers.get("X-Requested-With") == "XMLHttpRequest" or request.args.get("ajax") == "1"
    
    # Exécuter les tests
    report = run_all_tests()
    
    # Enregistrer dans SQLite
    storage.save_run(
        timestamp=report["timestamp"],
        passed_count=report["passed_count"],
        failed_count=report["failed_count"],
        latency_avg=report["latency_avg"],
        latency_p95=report["latency_p95"],
        success_rate=report["success_rate"],
        details=report["tests"]
    )
    
    if is_ajax or request.method == "POST":
        return jsonify(report)
    
    # Sinon (GET classique sans AJAX), rediriger vers le dashboard
    return redirect(url_for("dashboard"))

@app.route("/api/history")
def api_history():
    """Renvoie l'historique complet des runs au format JSON."""
    runs = storage.get_all_runs(limit=100)
    return jsonify(runs)

@app.route("/api/export")
def api_export():
    """Permet de télécharger l'historique complet au format JSON."""
    runs = storage.get_all_runs(limit=1000)
    response_content = json.dumps(runs, indent=2, ensure_ascii=False)
    
    response = make_response(response_content)
    response.headers["Content-Disposition"] = "attachment; filename=fruityvice_test_history.json"
    response.headers["Content-Type"] = "application/json"
    return response

@app.route("/api/clear", methods=["POST"])
def api_clear():
    """Vide l'historique de la base de données."""
    storage.clear_db()
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return jsonify({"success": True, "message": "Database cleared successfully."})
    return redirect(url_for("dashboard"))

@app.route("/health")
def health():
    """
    Endpoint bonus de santé (/health) pour évaluer l'état
    de la base SQLite, de l'API externe et du dernier run.
    """
    health_status = {
        "status": "OK",
        "timestamp": datetime.datetime.now().isoformat(),
        "database": {
            "status": "OK",
            "total_runs": 0,
            "error": None
        },
        "fruityvice_api": {
            "status": "UNKNOWN",
            "latency_ms": 0.0,
            "error": None
        },
        "last_run": None
    }
    
    # 1. Vérification BDD
    try:
        runs = storage.get_all_runs(limit=1)
        health_status["database"]["total_runs"] = len(storage.get_all_runs(limit=1000))
        if runs:
            health_status["last_run"] = {
                "timestamp": runs[0]["timestamp"],
                "success_rate": runs[0]["success_rate"],
                "passed_count": runs[0]["passed_count"],
                "failed_count": runs[0]["failed_count"]
            }
    except Exception as e:
        health_status["status"] = "DEGRADED"
        health_status["database"]["status"] = "ERROR"
        health_status["database"]["error"] = str(e)
        
    # 2. Vérification API externe (Fruityvice)
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
    app.run(host="0.0.0.0", port=5000, debug=True)
