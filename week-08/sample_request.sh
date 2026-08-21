curl -X POST http://127.0.0.1:8000/prioritize \
     -H "Content-Type: application/json" \
     -d '{
            "items": [
                "the food was great",
                "the service was terrible but we went there anyway",
                "never again"
            ],
            "top_n": 3
        }'


curl -X POST http://127.0.0.1:8000/prioritize \
     -H "Content-Type: application/json" \
     -d '{
            "items": [
                "it was the worst place I ever worked, do not recommend",
                "a bunch of backstabbing fools, stay far away!",
                "meh, it was a job",
                "loved it"
            ],
            "top_n": 3
        }'