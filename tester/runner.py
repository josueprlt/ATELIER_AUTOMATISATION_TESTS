import datetime
import math
from tester.client import APIClient
from tester.tests import get_all_tests

def calculate_p95(latencies):
    """Calcule le 95ème percentile d'une liste de latences."""
    if not latencies:
        return 0.0
    sorted_latencies = sorted(latencies)
    index = math.ceil(0.95 * len(sorted_latencies)) - 1
    # Assurer que l'index reste dans les bornes
    index = max(0, min(index, len(sorted_latencies) - 1))
    return sorted_latencies[index]

def run_all_tests():
    """
    Exécute tous les tests définis, compile les statistiques QoS,
    et renvoie le rapport complet du run.
    """
    client = APIClient(base_url="https://www.fruityvice.com", timeout=4.0, max_retries=1)
    tests = get_all_tests()
    
    timestamp = datetime.datetime.now().isoformat()
    test_results = []
    latencies = []
    
    passed_count = 0
    failed_count = 0
    
    for test_func in tests:
        try:
            # Exécution d'un test
            res = test_func(client)
            test_results.append(res)
            
            latencies.append(res["latency_ms"])
            if res["status"] == "PASS":
                passed_count += 1
            else:
                failed_count += 1
        except Exception as e:
            failed_count += 1
            test_results.append({
                "name": test_func.__doc__.split("-")[0].strip() if test_func.__doc__ else test_func.__name__,
                "endpoint": "N/A",
                "status": "FAIL",
                "latency_ms": 0.0,
                "details": f"Crash inattendu du test: {str(e)}"
            })
            
    total_tests = len(test_results)
    success_rate = (passed_count / total_tests) * 100 if total_tests > 0 else 0.0
    latency_avg = sum(latencies) / len(latencies) if latencies else 0.0
    latency_p95 = calculate_p95(latencies)
    
    return {
        "timestamp": timestamp,
        "passed_count": passed_count,
        "failed_count": failed_count,
        "success_rate": success_rate,
        "latency_avg": latency_avg,
        "latency_p95": latency_p95,
        "tests": test_results
    }
