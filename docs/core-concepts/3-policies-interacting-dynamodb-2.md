# DynamoDB Integration Approaches in Spring Boot

This document summarizes and compares three different approaches used in the project for integrating with DynamoDB, each demonstrated with a distinct domain model.

## Table of Contents

- [Approach 1: Car (Manual Mapping)](#approach-1-car-manual-mapping)
- [Approach 2: Delegation (Hybrid Mapping)](#approach-2-delegation-hybrid-mapping)
- [Approach 3: User (Repository + Enhanced Client)](#approach-3-user-repository--enhanced-client)
- [Comparison Table](#comparison-table)



## Approach 1: Car (Manual Mapping)

**Domain:** Car

- Uses low-level DynamoDB client (`DynamoDbClient`)
- Manually maps a `Map&lt;String, Object&gt;` to DynamoDB attributes
- No compile-time type safety

```java
public void saveCar(Map<String, Object> carJson) {
    Map<String, AttributeValue> itemValues = new HashMap<>();
    // Manual mapping logic...
    dynamoDbClient.putItem(PutItemRequest.builder()
        .tableName("Cars")
        .item(itemValues)
        .build());
}
```

## Approach 2: Delegation (Hybrid Mapping)

**Domain:** Delegation

- Uses POJO with DynamoDB annotations (`@DynamoDbBean`, `@DynamoDbAttribute`)
- Still manually creates an attribute map in the endpoint
- Partial type safety, but manual mapping can cause schema drift

```java
@DynamoDbBean
public class Delegation {
    // fields, getters, setters with @DynamoDbAttribute
}
public void saveDelegation(Delegation delegation) {
    Map<String, AttributeValue> delegationMap = new HashMap<>();
    // Manual mapping logic...
    dynamoDbClient.putItem(PutItemRequest.builder()
        .tableName("Delegations")
        .item(delegationMap)
        .build());
}
```

## Approach 3: User (Repository + Enhanced Client)

**Domain:** User

- Uses DynamoDB Enhanced Client and repository pattern
- Pure POJO with annotations; no manual mapping in endpoint
- Full type safety and maintainability

```java
@DynamoDbBean
public class User { /* ... */ }

@Repository
public class UserRepositoryImpl implements UserRepository {
    private final DynamoDbTable<User> userTable;
    public void saveUser(User user) {
        userTable.putItem(user);
    }
}
```

## Comparison Table

| Feature / Approach | Car (Manual Mapping)               | Delegation (Hybrid)          | User (Repository + Enhanced)       |
|:------------------ |:---------------------------------- |:---------------------------- |:---------------------------------- |
| **Domain**         | Car                                | Delegation                   | User                               |
| **Client Type**    | Low-level DynamoDB client          | Low-level + POJO/Annotations | Enhanced Client + Repository       |
| **Mapping**        | Manual `Map&lt;String, Object&gt;` | POJO + manual map            | POJO, automatic                    |
| **Type Safety**    | ❌ None                             | ⚠️ Partial                   | ✅ Full                             |
| **Boilerplate**    | High                               | Moderate                     | Low                                |
| **Best For**       | Dynamic/unstructured data          | Transitional codebases       | Structured, maintainable codebases |
| **Error Prone?**   | High                               | Moderate                     | Low                                |

---

## Summary & Recommendations

- **Approach 1 (Car):**
  Use only for rapid prototyping or when schema is highly dynamic. Not recommended for production due to lack of type safety and high maintenance cost.
- **Approach 2 (Delegation):**
  Useful as a transitional pattern, but mixing POJO annotations with manual mapping can lead to schema mismatches and bugs. Prefer moving to full Enhanced Client usage.
- **Approach 3 (User):**
  Recommended for most use cases. The repository pattern with DynamoDB Enhanced Client provides type safety, maintainability, and cleaner code.


