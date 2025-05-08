import json
import random

makes = ["Toyota", "Honda", "Ford", "Chevrolet", "Nissan"]
models = ["Camry", "Civic", "Mustang", "Impala", "Altima"]
cars = []

for i in range(50):
    car = {
        "delegationId": f"DELEG#001",
        "operation": f"car#{random.choice([2023,2024,2025])}#{i+1:03d}",
        "make": random.choice(makes),
        "model": random.choice(models),
        "year": random.randint(2023, 2025),
        "color": random.choice(["Blue", "Red", "Black", "White", "Green"]),
        "rented": random.choice([True, False]),
        "price": random.randint(10, 50)
    }
    cars.append(car)

with open('cars.json', 'w') as f:
    json.dump(cars, f, indent=2)

