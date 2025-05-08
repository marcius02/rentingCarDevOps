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

