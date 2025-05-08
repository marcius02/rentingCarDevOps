## Summary of DynamoDB Integration Approaches

> The project implements three distinct approaches for interacting with DynamoDB across different domains (`Car`, `Delegation`, and `User`). 

| **Feature**              | **Approach 1: Car**                                                     | **Approach 2: Delegation**                                                     | **Approach 3: User**                                                  |
| ------------------------ | ----------------------------------------------------------------------- | ------------------------------------------------------------------------------ | --------------------------------------------------------------------- |
| **Client Type**          | Low-level DynamoDB client                                               | Mixed: Enhanced Client for mapping + Low-level client for writes               | Enhanced Client exclusively                                           |
| **Data Handling**        | Manual conversion of `Map<String, Object>` to DynamoDB `AttributeValue` | Partially automated via `@DynamoDbBean`, but manual `Map` creation in endpoint | Fully automated via `DynamoDbTable.putItem()` with repository pattern |
| **Type Safety**          | ❌ Loose typing (relies on runtime checks)                               | ✅ Partial (annotations enforce schema but manual `Map` reduces safety)         | ✅ Full (compile-time validation via POJOs)                            |
| **Boilerplate**          | High (manual field mapping)                                             | Moderate (annotations reduce boilerplate but manual `Map` remains)             | Low (repository abstraction hides DynamoDB specifics)                 |
| **Use Case**             | Dynamic schemas or unstructured data                                    | Transitional phase between low-level and enhanced client                       | Structured domain models with strict schemas                          |
| **DynamoDB Annotations** | None                                                                    | `@DynamoDbBean` + `@DynamoDbAttribute`                                         | `@DynamoDbBean` + `@DynamoDbPartitionKey` + `@DynamoDbAttribute`      |
| **Error-Prone?**         | High (manual type conversions)                                          | Moderate (annotation mismatches can cause issues)                              | Low (type-safe operations)                                            |
| **Maintenance**          | Difficult (changes require updating manual mappings)                    | Moderate (annotations simplify schema updates)                                 | Easy (changes propagate automatically)                                |

## Key Takeaways

1. **Approach 1 (Car)**
   
   - **Best for**: Rapid prototyping or dynamic data structures.
   
   - **Drawback**: No type safety; manual mapping is error-prone.

2. **Approach 2 (Delegation)**
   
   - **Hybrid Approach**: Combines annotation-based mapping with low-level client operations.
   
   - **Issue**: Manual `Map` creation in the endpoint overrides the benefits of `@DynamoDbBean`, leading to schema mismatches (e.g., `carAvailableQty` vs. `availableCarQty`).

3. **Approach 3 (User)**
   
   - **Best Practice**: Uses repository pattern with Enhanced Client for full type safety and minimal boilerplate.
   
   - **Recommendation**: Adopt this approach for most structured data models.
