# AWS DynamoDB Guide

## Introduction

> <mark>Amazon DynamoDB is a fully managed NoSQL database service</mark> provided by AWS, designed for high availability, scalability, and low latency.
> 
> It supports key-value and document data models, making it suitable for applications requiring consistent, **single-digit millisecond** performance at any scale.

**Useful Links:**

- [Official DynamoDB Documentation](https://docs.aws.amazon.com/dynamodb/)
- [AWS DynamoDB Console](https://aws.amazon.com/dynamodb/)
- [DynamoDB Pricing](https://aws.amazon.com/dynamodb/pricing/)

## What is NoSQL and DynamoDB?

NoSQL databases are non-relational databases designed to handle large-scale, unstructured, or semi-structured data. 

Unlike traditional SQL databases, NoSQL databases offer flexible schemas and horizontal scaling.

DynamoDB is AWS's NoSQL database service, optimized for:

- **Scalability**: Automatically scales to handle millions of requests per second.
- **Performance**: Delivers consistent low-latency responses.
- **Fully Managed**: Handles maintenance, backups, and scaling without manual intervention.
- **Use Cases**: Mobile apps, gaming, IoT, e-commerce, and real-time analytics.

## AWS Account

To use DynamoDB, you need an AWS account:

1. Sign up at [aws.amazon.com](https://aws.amazon.com/).
2. Set up billing and configure Multi-Factor Authentication (MFA).
3. Access DynamoDB via the AWS Management Console, CLI, or SDKs.
4. Use the AWS Free Tier, which includes **25 GB of storage and 25 write/read capacity units per month for DynamoDB**.

## DynamoDB Features

### Backup / Replicas

- **On-Demand Backup**: Create full backups of tables for long-term retention or disaster recovery.
- **Point-in-Time Recovery (PITR)**: Restore tables to any point in the last 35 days.
- **Global Tables**: Replicate data across multiple AWS regions for low-latency access and disaster recovery.
  - Ensures data consistency with multi-region replication.

### Streams

- **DynamoDB Streams**: Captures item-level changes (inserts, updates, deletes) in a table.
- **Use Cases**: Trigger AWS Lambda functions, replicate data, or build event-driven applications.
- **Configuration**: Enable streams on a table and specify the view type (e.g., new image, old image, or both).

### Keys (PK + SK, GSI)

- **Primary Key (PK)**: Uniquely identifies each item. Can be:
  - **Partition Key**: A single attribute for distributing data.
  - **Partition Key + Sort Key**: Combines a partition key with a sort key for range queries.
- **Global Secondary Index (GSI)**: Alternate query paths with different partition and sort keys.
  - Supports eventual or strong consistency.
  - Useful for flexible querying without duplicating tables.
- **Local Secondary Index (LSI)**: Alternate sort key for the same partition key (created at table creation).

### DAX (DynamoDB Accelerator)

- **DAX**: In-memory cache for DynamoDB, reducing read latency to microseconds.
- **Use Cases**: Applications needing ultra-low latency, like real-time bidding or gaming.
- **Features**:
  - Fully managed, compatible with existing DynamoDB APIs.
  - Write-through caching ensures data consistency.
- **Considerations**: Additional costs and best for read-heavy workloads.

### TTL (Time to Live)

- **TTL**: Automatically deletes items after a specified timestamp.
- **Configuration**: Enable TTL on a table and specify an attribute containing the expiration timestamp (Unix epoch).
- **Use Cases**: Remove stale data, like session logs or temporary records, to reduce costs.
- **Note**: Deletion is asynchronous and may take up to 48 hours.

### SDK Java v2

- **AWS SDK for Java v2**: A modern, modular SDK for interacting with DynamoDB.

- **Key Features**:
  
  - Supports synchronous and asynchronous clients.
  - Enhanced client for simplified data modeling.
  - Example operations: `PutItem`, `GetItem`, `Query`, `Scan`.

- **Setup**:
  
  1. Add dependency to `pom.xml`:
     
     ```xml
     <dependency>
         <groupId>software.amazon.awssdk</groupId>
         <artifactId>dynamodb</artifactId>
         <version>2.x.x</version>
     </dependency>
     ```
  
  2. Configure credentials (e.g., via AWS CLI or environment variables).
  
  3. Example code:
     
     ```java
     import software.amazon.awssdk.services.dynamodb.DynamoDbClient;
     import software.amazon.awssdk.services.dynamodb.model.AttributeValue;
     import software.amazon.awssdk.services.dynamodb.model.PutItemRequest;
     import java.util.HashMap;
     
     public class DynamoDBExample {
         public static void main(String[] args) {
             DynamoDbClient client = DynamoDbClient.create();
             HashMap<String, AttributeValue> item = new HashMap<>();
             item.put("ID", AttributeValue.builder().s("123").build());
             item.put("Name", AttributeValue.builder().s("John Doe").build());
             PutItemRequest request = PutItemRequest.builder()
                     .tableName("MyTable")
                     .item(item)
                     .build();
             client.putItem(request);
         }
     }
     ```

- **Resources**: [Java SDK v2 Documentation](https://docs.aws.amazon.com/sdk-for-java/v2/developer-guide/basics.html).

## AWS CLI

The AWS Command Line Interface (CLI) allows you to manage DynamoDB resources from the terminal.

- **Installation**:
  
  - Install AWS CLI: [AWS CLI Installation Guide](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html).
  - Configure credentials: `aws configure`.

- **Common Commands**:
  
  - Create a table:
    
    ```bash
    aws dynamodb create-table \
        --table-name MyTable \
        --attribute-definitions AttributeName=ID,AttributeType=S \
        --key-schema AttributeName=ID,KeyType=HASH \
        --provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5
    ```
  
  - Put an item:
    
    ```bash
    aws dynamodb put-item \
        --table-name MyTable \
        --item '{"ID": {"S": "123"}, "Name": {"S": "John Doe"}}'
    ```
  
  - Query a table:
    
    ```bash
    aws dynamodb query \
        --table-name MyTable \
        --key-condition-expression "ID = :id" \
        --expression-attribute-values '{":id": {"S": "123"}}'
    ```
  
  - Enable TTL:
    
    ```bash
    aws dynamodb update-time-to-live \
        --table-name MyTable \
        --time-to-live-specification "Enabled=true, AttributeName=ExpirationTime"
    ```

- **Resources**: [DynamoDB CLI Reference](https://docs.aws.amazon.com/cli/latest/reference/dynamodb/).