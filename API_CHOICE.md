# API Choice

- Étudiant : Josué Perrault
- API choisie : Frankfurter
- URL base : https://api.frankfurter.app
- Documentation officielle / README : https://www.frankfurter.app/docs/
- Auth : None
  - Endpoints testés :
      - GET https://api.frankfurter.app/currencies
      - GET https://api.frankfurter.app/latest
      - GET https://api.frankfurter.app/latest?from=USD
      - GET https://api.frankfurter.app/latest?amount=100&from=EUR&to=USD
      - GET https://api.frankfurter.app/2020-01-01
      - GET https://api.frankfurter.app/invalid_route_xyz
      - GET https://api.frankfurter.app/latest?from=INVALID
- Hypothèses de contrat (champs attendus, types, codes) :

```json
{
  "amount": 1.0,
  "base": "EUR",
  "date": "2026-05-20",
  "rates": {
    "USD": 1.0854,
    "GBP": 0.8542
  }
}
```

Codes :
- Code : 200 OK (requête valide)
- Code : 404 Not Found (route invalide)
- Code : 400 Bad Request (devise invalide ou mal formatée)
- Limites / rate limiting connu : Pas de limites strictes pour un usage raisonnable.
- Risques (instabilité, downtime, CORS, etc.) : Très stable, hébergé de façon résiliente, sur la liste blanche officielle de PythonAnywhere.