# Hilla rentingCar v1.1: List Cars

## Intro & Links

Commits:

- [rentingCar at 286d930](https://github.com/AlbertProfe/rentingCar/tree/286d930bbb8e92a3f6c4565a3cd4a913c818dc04)
- [rentingCar at 0edf8b5 preliminar version](https://github.com/AlbertProfe/rentingCar/tree/0edf8b549b9891be14be66d56ba28485fdd84223)

> The Hilla `rentingCar`<mark> application (v1.0)</mark> full-stack framework combining a React frontend and a Spring Boot backend uses <mark>AWS DynamoDB</mark> for data storage. 

This v1.1 focuses on the <mark>"List Cars"</mark> feature, specifically the `listAllCars()` method, which retrieves **all available cars from the database** for display in the frontend.

**Links**:

- [Hilla Documentation](https://hilla.dev/docs/)
- [AWS DynamoDB SDK for Java](https://docs.aws.amazon.com/sdk-for-java/v2/developer-guide/examples-dynamodb-enhanced.html)
- [Vaadin Components](https://vaadin.com/docs/latest/components)

## Feature

> The "List Cars" feature allows users to view all available cars in the rental system. Each car is displayed with details such as make, model, year, color, price, and availability status. 

Users can book available cars directly from the interface. The feature relies on the `listAllCars()` method in the backend to fetch car data from a DynamoDB table named "Delegations," filtering for items with a sort key beginning with "car".

Key aspects:

- **Data Source**: AWS DynamoDB table "`Delegations`" storing `Car` and `Delegation` beans.
- **Filtering**: Retrieves only `Car` items where the sort key (`operation`) starts with "car" (e.g., "`car#2024#001`").
- **Frontend Display**: Cards with car images, details, and a "`BOOK`" button.
- **Interactivity**: Users can book cars, with a simple alert confirming the action (extendable for full booking logic).

## Backend Endpoint & Repo

The backend is implemented using Spring Boot and the AWS SDK for DynamoDB Enhanced Client. The `DelegationEndpoint` exposes the `getAllCars()` method, which calls `listAllCars()` from the `DelegationRepository`. The repository interacts with the DynamoDB table to retrieve `Car` objects.

- **Endpoint**: `DelegationEndpoint.getAllCars()` (Hilla endpoint, accessible from the frontend).
- **Repository**: `DelegationRepositoryImpl.listAllCars()` handles the DynamoDB scan operation.
- **Security**: The endpoint is annotated with `@AnonymousAllowed`, allowing unauthenticated access for browsing cars.

The `listAllCars()` method uses a filter expression (`begins_with(operation, :val)`) to ensure only `Car` items are returned, making the query efficient and targeted.

## Frontend Component

The frontend component, `ListCars`, is a React component built with Hilla and Vaadin components. It:

- Fetches the car list using `DelegationEndpoint.getAllCars()`.
- Displays cars in a responsive grid of cards, each showing an image (sourced from imagin.studio), details, and a "BOOK" button.
- Handles loading states and empty results gracefully.
- Filters out invalid cars (missing `delegationId` or `operation`) and ensures `make` and `model` are valid for display.
- Provides a simple booking interaction via an alert (extendable for full booking functionality).

The component is configured with a `ViewConfig` for menu integration, appearing as "Book a car" with a car icon.

## Code

### Backend: DelegationRepositoryImpl.java (`listAllCars()`)

This method retrieves all `Car` items from the DynamoDB "Delegations" table, filtering for sort keys starting with "car".

```java
@Override
public List<Car> listAllCars() {
    // Create a DynamoDB table object for the Car class, mapping to the "Delegations" table
    DynamoDbTable<Car> table = enhancedClient.table(tableName, TableSchema.fromBean(Car.class));
    // Initialize an empty ArrayList to store the retrieved Car objects
    List<Car> cars = new ArrayList<>();
    // Create a HashMap to store expression values for the filter expression
    Map<String, AttributeValue> expressionValues = new HashMap<>();
    // Add a key-value pair to the map, where ":val" is the placeholder for the string "car"
    expressionValues.put(":val", AttributeValue.builder().s("car").build());
    // Build a filter expression to match items where the "operation" sort key begins with "car"
    Expression filterExpression = Expression.builder()
            .expression("begins_with(operation, :val)") // Define the expression using the begins_with function
            .expressionValues(expressionValues) // Associate the expression values map
            .build(); // Construct the Expression object
    // Build a ScanEnhancedRequest with the filter expression to limit results to Car items
    ScanEnhancedRequest scanRequest = ScanEnhancedRequest.builder()
            .filterExpression(filterExpression) // Apply the filter expression to the scan
            .build(); // Construct the ScanEnhancedRequest object
    // Execute the scan operation and iterate over the results, adding each Car item to the cars list
    table.scan(scanRequest).items().forEach(cars::add);
    // Return the list of Car objects
    return cars;
}
```

****DynamoDB Query and Scan operations using the AWS Java SDK v2****

| Feature             | Query                                            | Scan                                                       |
| ------------------- | ------------------------------------------------ | ---------------------------------------------------------- |
| Purpose             | Retrieves items by partition key (direct lookup) | Retrieves all items in the table (full table scan)         |
| Performance         | Fast, efficient (accesses only relevant items)   | Slow, especially on large tables (reads every item)        |
| Cost                | Lower (reads only matching items)                | Higher (reads the entire table, even with filters)         |
| Required Parameters | Partition key (and optional sort key conditions) | None (filters are optional, applied after reading)         |
| Use Case            | When you know the partition key                  | When you need all items or don’t know the key              |
| Filtering           | KeyConditionExpression (before read), filters    | FilterExpression (after read, doesn’t save cost)           |
| Best Practice       | Prefer Query for most access patterns            | Avoid Scan unless necessary (e.g., analytics, full export) |

Use the <mark>Query</mark> operation when you know the partition key, as it provides fast and cost-effective access by retrieving only the relevant items directly from the table or index. Query operations are highly efficient and scale well, making them ideal for most access patterns in DynamoDB. 

In contrast, use the <mark>Scan</mark> operation only when you need to retrieve all items or when the partition key is unknown. Scan reads every item in the table, which can lead to high latency and increased costs, especially as the table grows. Scans can also consume your provisioned throughput quickly and may result in slower performance due to the need to examine every item, even those filtered out after reading. 

> For best performance and lower costs, design your data model to use Query whenever possible and reserve Scan for rare analytics or full data export scenarios

### Backend: DelegationEndpoint.java (`getAllCars()`)

This Hilla endpoint exposes the `listAllCars()` method to the frontend.

```java
@Endpoint
@AnonymousAllowed
public class DelegationEndpoint {
    private final DelegationRepository delegationRepository;

    @Autowired
    public DelegationEndpoint(DelegationRepository delegationRepository) {
        this.delegationRepository = delegationRepository;
    }

    // List all cars for all delegations
    public List<Car> getAllCars() {
        return delegationRepository.listAllCars();
    }
}
```

### Frontend: ListCars.tsx

This React component fetches and displays the car list, integrating with the backend endpoint.

```typescript
import { ViewConfig } from '@vaadin/hilla-file-router/types.js';
import { useEffect, useState } from 'react';
import { DelegationEndpoint } from 'Frontend/generated/endpoints';
import Car from 'Frontend/generated/dev/renting/delegations/Car';
import { Button } from '@vaadin/react-components/Button';

export const config: ViewConfig = {
  menu: { order: 6, icon: 'line-awesome/svg/car-side-solid.svg' },
  title: 'Book a car',
};

export default function ListCars() {
  const [cars, setCars] = useState<Car[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    DelegationEndpoint.getAllCars()
      .then((result) => {
        // Filter out cars missing delegationId or operation
        const safeCars = (result ?? []).filter(
          (car): car is Car =>
            !!car &&
            typeof car.delegationId === 'string' &&
            typeof car.operation === 'string'
        );
        setCars(safeCars);
      })
      .catch((error) => {
        console.error('Failed to fetch cars:', error);
        setCars([]);
      })
      .finally(() => setLoading(false));
  }, []);

  const handleBook = (car: Car) => {
    alert(`You booked ${car.make} ${car.model}!`);
    // Add booking logic here if needed
  };

  function isCarWithMakeAndModel(car: Car): car is Car & { make: string; model: string } {
    return typeof car.make === 'string' && typeof car.model === 'string';
  }

  if (loading) {
    return <div>Loading cars...</div>;
  }

  if (cars.length === 0) {
    return <div>No cars available.</div>;
  }

  return (
    <div
      style={{
        display: 'flex',
        flexWrap: 'wrap',
        gap: '2rem',
        justifyContent: 'center',
        padding: '2rem'
      }}
    >
      {cars
        .filter(isCarWithMakeAndModel)
        .map(car => (
          <div
            key={`${car.delegationId}-${car.operation}`}
            style={{
              border: '1px solid #ddd',
              borderRadius: '12px',
              width: '320px',
              boxShadow: '0 2px 8px rgba(0,0,0,0.08)',
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              padding: '1.5rem',
              background: '#fff'
            }}
          >
            <img
              src={`https://cdn.imagin.studio/getimage?customer=img&make=${encodeURIComponent(car.make)}&modelFamily=${encodeURIComponent(car.model.split(' ')[0])}&zoomType=fullscreen`}
              alt={`${car.make} ${car.model}`}
              style={{
                width: '100%',
                height: '180px',
                objectFit: 'cover',
                borderRadius: '8px',
                marginBottom: '1rem'
              }}
              onError={(e) => {
                (e.target as HTMLImageElement).src = 'https://placehold.co/300x180?text=Car+Not+Found';
              }}
            />
            <h3>
              {car.make} {car.model}
            </h3>
            <div style={{ marginBottom: '0.5rem', color: '#555' }}>
              Year: <strong>{car.year}</strong>
            </div>
            <div style={{ marginBottom: '0.5rem', color: '#555' }}>
              Color: <strong>{car.color}</strong>
            </div>
            <div style={{ marginBottom: '0.5rem', color: '#555' }}>
              Price: <strong>{car.price} €</strong>
            </div>
            <div style={{ marginBottom: '1rem', color: car.rented ? '#d33' : '#090' }}>
              {car.rented ? 'Rented' : 'Available'}
            </div>
            <Button
              theme="primary"
              disabled={car.rented}
              onClick={() => handleBook(car)}
              style={{ width: '100%' }}
            >
              BOOK
            </Button>
          </div>
        ))
      }
    </div>
  );
}
```
