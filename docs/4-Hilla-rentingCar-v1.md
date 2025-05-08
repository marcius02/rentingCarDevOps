# Hilla rentingCar: 2 single-tables

## Intro & Links

Having both `Delegation` and `Car`:

```java
@DynamoDbBean
public class Car {
    private String delegationId;     // Partition Key
    private String operation;        // Sort Key
    private String make;
    private String model;
    private int year;
    private String color;
    private boolean rented;
    private int price;

    // Partition key
    @DynamoDbPartitionKey
    public String getDelegationId() {
        return delegationId;
    }

    public void setDelegationId(String delegationId) {
        this.delegationId = delegationId;
    }

    @DynamoDbSortKey
    public String getOperation() {
        return operation;
    }

    public void setOperation(String operation) {
        this.operation = operation;
    }
    // ... other getters and setters
}


@DynamoDbBean
public class Delegation {
    private String delegationId;    // Partition Key
    private String operation;       // Sort Key
    private String name;
    private String address;
    private String city;
    private int availableCarQty;
    private String phone;
    private String email;

    @DynamoDbPartitionKey
    public String getDelegationId() {
        return delegationId;
    }

    public void setDelegationId(String delegationId) {
        this.delegationId = delegationId;
    }

    @DynamoDbSortKey
    public String getOperation() {
        return operation;
    }

    public void setOperation(String operation) {
        this.operation = operation;
    }
     // ... other getters and setters
}
```



- Both `Delegation` and `Car` are stored in the same DynamoDB table `"Delegations"`.
- They share the same partition key attribute name (`delegationId` for Delegation, `id` for Car) and sort key attribute `operation`.
- We want to use the same <mark>DynamoDbEnhancedClient table instance</mark> to *save/get/query* both types.
- We want a **single repository interface** and implementation to <mark>handle</mark> both types.
- We want a **single endpoint** <mark>exposing</mark> operations for both types.



## Step-by-step

How to design a unified repository and endpoint for two beans

### 1. Create a generic repository interface

```java
package dev.renting.delegations;

import java.util.List;

public interface DelegationCarRepository {
    <T> void save(T item);

    <T> T get(String partitionKey, String sortKey, Class<T> clazz);

    <T> List<T> listByPartitionKey(String partitionKey, Class<T> clazz);
}
```

- This interface uses generics to support any bean type (`Delegation` or `Car`).
- The `partitionKey` and `sortKey` are strings.
- The `clazz` parameter tells the repository which bean type to use for marshalling/unmarshalling.

### 2. Implement the generic repository

```java
package dev.renting.delegations;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Repository;
import software.amazon.awssdk.enhanced.dynamodb.DynamoDbEnhancedClient;
import software.amazon.awssdk.enhanced.dynamodb.DynamoDbTable;
import software.amazon.awssdk.enhanced.dynamodb.Key;
import software.amazon.awssdk.enhanced.dynamodb.TableSchema;
import software.amazon.awssdk.enhanced.dynamodb.model.QueryConditional;

import java.util.ArrayList;
import java.util.List;

@Repository
public class DelegationCarRepositoryImpl implements DelegationCarRepository {

    private final DynamoDbEnhancedClient enhancedClient;
    private final String tableName = "Delegations";

    @Autowired
    public DelegationCarRepositoryImpl(DynamoDbEnhancedClient enhancedClient) {
        this.enhancedClient = enhancedClient;
    }

    @Override
    public <T> void save(T item) {
        DynamoDbTable<T> table = enhancedClient.table(tableName, TableSchema.fromBean((Class<T>) item.getClass()));
        table.putItem(item);
    }

    @Override
    public <T> T get(String partitionKey, String sortKey, Class<T> clazz) {
        DynamoDbTable<T> table = enhancedClient.table(tableName, TableSchema.fromBean(clazz));
        Key key = Key.builder()
                .partitionValue(partitionKey)
                .sortValue(sortKey)
                .build();
        return table.getItem(key);
    }

    @Override
    public <T> List<T> listByPartitionKey(String partitionKey, Class<T> clazz) {
        DynamoDbTable<T> table = enhancedClient.table(tableName, TableSchema.fromBean(clazz));
        QueryConditional queryConditional = QueryConditional.keyEqualTo(k -> k.partitionValue(partitionKey));
        List<T> items = new ArrayList<>();
        table.query(queryConditional).items().forEach(items::add);
        return items;
    }
}
```

### 3. Create a unified endpoint

```java
package dev.renting.delegations;

import com.vaadin.flow.server.auth.AnonymousAllowed;
import com.vaadin.hilla.Endpoint;
import org.springframework.beans.factory.annotation.Autowired;

import java.util.List;

@Endpoint
@AnonymousAllowed
public class DelegationCarEndpoint {

    private final DelegationCarRepository delegationCarRepository;

    @Autowired
    public DelegationCarEndpoint(DelegationCarRepository delegationCarRepository) {
        this.delegationCarRepository = delegationCarRepository;
    }

    // Save Delegation
    public void saveDelegation(Delegation delegation) {
        delegationCarRepository.save(delegation);
    }

    // Save Car
    public void saveCar(Car car) {
        delegationCarRepository.save(car);
    }

    // Get Delegation by keys
    public Delegation getDelegation(String delegationId, String operation) {
        return delegationCarRepository.get(delegationId, operation, Delegation.class);
    }

    // Get Car by keys
    public Car getCar(String id, String operation) {
        return delegationCarRepository.get(id, operation, Car.class);
    }

    // List Delegations by delegationId
    public List<Delegation> listDelegationsById(String delegationId) {
        return delegationCarRepository.listByPartitionKey(delegationId, Delegation.class);
    }

    // List Cars by id (partition key)
    public List<Car> listCarsById(String id) {
        return delegationCarRepository.listByPartitionKey(id, Car.class);
    }
}
```

## Generics

Here’s a very basic explanation:

- **`<T>`** is Java’s way of saying “*this method or interface works with any type*.” 
  - The `T` is just a placeholder for a real type (like `Car`, `Delegation`, `String`, etc.). [^1](https://stackoverflow.com/questions/60200188/java-generics-t-meaning) [^4](https://www.digitalocean.com/community/tutorials/java-generics-example-method-class-interface).
- **`T`** is the name commonly used for this placeholder type. It stands for “Type,” but you could use any letter or word (like ` `<E>`, `<Type>, etc.)[^4](https://www.tutorialspoint.com/is-it-mandatory-to-use-t-for-type-parameter-while-defining-generics-classes-methods-in-java).
- **`clazz`** (short for “class”) is a parameter of type `Class<T>`. This tells Java what the real type is at runtime, so it knows how to create or read objects of that type[^6](https://stackoverflow.com/questions/15888551/how-to-interpret-public-t-t-readobjectdata-classt-type-in-java).

**Example:**

```java
<T> T get(String partitionKey, String sortKey, Class<T> clazz)
```

- The `<T>` before the method means this method is generic-it works with any type.
- The `T` after it means the method will return an object of whatever type you specify.
- The `Class<T> clazz` parameter tells Java what type you want (e.g., `Car.class` or `Delegation.class`).

**In practice:**

- If you call `get("123", "profile", Delegation.class)`, `T` becomes `Delegation`.
- If you call `get("abc", "car#2024#001", Car.class)`, `T` becomes `Car`.

**Why use this?**

- It lets you write one method that works for many types, instead of repeating code for each type.



## Summary

| Layer          | Implementation detail                                             |
| -------------- | ----------------------------------------------------------------- |
| **Repository** | Generic with `<T>` and `Class<T>` to support multiple beans       |
| **Table**      | Single DynamoDB table `"Delegations"` with different beans        |
| **Endpoint**   | Unified endpoint exposing methods for both `Delegation` and `Car` |

## Next

- Make sure your `Delegation` and `Car` beans have distinct partition key and sort key attribute names mapped correctly.
- The generic repository relies on the bean class to marshal/unmarshal correctly.
- You can extend the generic interface with more specific queries if needed.
- For complex queries involving both types together, consider using a discriminator attribute or a GSI.
