# Hilla  rentingCar: minimum implementation

> Let's save the car JSON straightforwardly to DynamoDB by directly mapping the JSON to a `Map<String, AttributeValue>` <mark>item</mark> and using the AWS SDK Java v2 `PutItem` operation.

**Car JSON Example:**

```json
{
  "id": "123",
  "make": "Toyota",
  "model": "Camry",
  "year": 2023,
  "color": "Blue",  
  "isRented" : false
}
```

**Spring Boot Endpoint to Save Car JSON to DynamoDB:**

```java
import com.amazonaws.services.dynamodbv2.AmazonDynamoDB;
import com.amazonaws.services.dynamodbv2.model.AttributeValue;
import com.amazonaws.services.dynamodbv2.model.PutItemRequest;
import com.vaadin.hilla.Endpoint;
import com.vaadin.hilla.Nonnull;
import org.springframework.beans.factory.annotation.Autowired;

import java.util.HashMap;
import java.util.Map;

@Endpoint
public class CarEndpoint {

    @Autowired
    private AmazonDynamoDB dynamoDB;

    public void saveCar(@Nonnull Map<String, Object> carJson) {

        Map<String, AttributeValue> item = new HashMap<>();

        carJson.forEach((key, value) -> item.put(key, new AttributeValue().withS(value.toString())));

        PutItemRequest putItemRequest = new PutItemRequest()
                .withTableName("Cars")
                .withItem(item);

        dynamoDB.putItem(putItemRequest);
    }
}
```

**Usage in Hilla Frontend**:
Hilla will generate a TypeScript client for this endpoint. You can call it from the frontend like this (example in TypeScript):

```typescript
import { CarEndpoint } from 'Frontend/generated/endpoints';


export interface Car {
  id: string;
  make: string;
  model: string;
  year: number;
  color: string;
}


const car = {
  id: "123",
  make: "Toyota",
  model: "Camry",
  year: 2023,
  color: "Blue"
};

await CarEndpoint.saveCar(car);
```
