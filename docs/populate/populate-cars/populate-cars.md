# Populate Cars

The item car is like this:

```tsx
const sampleCar: Car = {
delegationId: "DELEG#001",
operation: "car#2025#002",
make: "Toyota",
model: "Camry",
year: 2025,
color: "Blue",
rented: false,
price: 14
};
```

**1. Generate Cars Data (Python):**

```python
import json
import random

makes = ["Toyota", "Honda", "Ford", "Chevrolet", "Nissan"]
models = ["Camry", "Civic", "Mustang", "Impala", "Altima"]
cars = []

for i in range(50):
    car = {
        "delegationId": f"DELEG#{i+1:03d}",
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
```

**2. Bash Import Script:**

```bash
#!/bin/bash
TABLE_NAME="Delegations"

for car in $(jq -c '.[]' cars.json); do
    aws dynamodb put-item \
        --table-name $TABLE_NAME \
        --item "$(echo "$car" | jq '{
            "delegationId": {"S": .delegationId},
            "operation": {"S": .operation},
            "make": {"S": .make},
            "model": {"S": .model},
            "year": {"N": (.year|tostring)},
            "color": {"S": .color},
            "rented": {"BOOL": .rented},
            "price": {"N": (.price|tostring)}
        }')"
done

echo "50 items inserted to $TABLE_NAME"
```

**To execute:**

1. Save Python code as `generate_cars.py`
2. Run `python3 generate_cars.py`
3. Save bash script as `import_cars.sh`
4. Make executable: `chmod +x import_cars.sh`
5. Run: `./import_cars.sh`

**Key components:**

- Uses `jq` for JSON processing
- Converts numeric fields to DynamoDB `N` type
- Preserves boolean values with `BOOL` type
- Processes all 50 items in sequence
- Requires AWS CLI configured with proper permissions

**Prerequisites:**

- Install `jq`: `sudo apt-get install jq`
- AWS CLI configured with access to DynamoDB
- Existing DynamoDB table named "Delegations"
