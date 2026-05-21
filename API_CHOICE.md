# API Choice

- Étudiant : Josué Perrault
- API choisie : Fruityvice
- URL base : https://www.fruityvice.com
- Documentation officielle / README : https://www.fruityvice.com
- Auth : None
  - Endpoints testés :
      - GET https://www.fruityvice.com/api/fruit/all
      - GET https://www.fruityvice.com/api/fruit/:fruit
      - GET https://www.fruityvice.com/api/fruit/family/:family
      - GET https://www.fruityvice.com/api/fruit/genus/:genus
      - GET https://www.fruityvice.com/api/fruit/order/:order
      - GET https://www.fruityvice.com/api/fruit/:nutrition?min=0&max=1000
      - PUT https://www.fruityvice.com/api/fruit
        - ```json
          {
          "genus": "Fragaria",
          "name": "Strawberry",
          "family": "Rosaceae",
          "order": "Rosales",
          "nutritions": {
          "carbohydrates": 5.5,
          "protein": 0,
          "fat": 0.4,
          "calories": 29,
          "sugar": 5.4
          }
          }
          ```
- Hypothèses de contrat (champs attendus, types, codes) :

```json
{
  "genus": "Musa",            // String
  "name": "Banana",           // String
  "id": 2,                    // Interger
  "family": "Musaceae",       // String
  "order": "Zingiberales",    // String
  "nutritions": {             // Object
    "carbohydrates": 22,      // Integer
    "protein": 0,             // Integer
    "fat": 0.2,               // Decimal
    "calories": 96,           // Integer
    "sugar": 17.2             // Decimal
  }
}
```

Codes :
```baash
Code : 200 OK
```
```baash
Code : 404 Not Found
```
```baash
Code : 500 Internal server error
```
- Limites / rate limiting connu : Pas d'info à se sujet
- Risques (instabilité, downtime, CORS, etc.) : Pas d'info à se sujet