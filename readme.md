## TODO:
- Find out where GraphQL client lives
  In FastAPI, graphQL lives in the `.py` file. Schema is the brain, FastAPI is the door and middleware is the bridge.
  
- Validation and Error Handling
  
- Authorization 
  Login -> Get JWT Token
  Login with Google
  
- Database Migrations
  
- Payment

## Alembic
Initiate Alembic
```
alembic init alembic
```

Create Migration Script
```
alembic revision -m "initial migration"
```

Run Migration
```
alembic upgrade head
```

Rollback Migration
```
alembic downgrade -1
```

Migration History
```
alembic history --verbose
```



```python
# GraphQL Query
# =============

# Get All Items
# {
#   allItems {
#     id
#     name
#   }
# }

# Create Item
# mutation {
#  createItem(name: "RAM Hynix", description: "UltraFast RAM") {
#   name
#   description
# 	} 
# }

# Update Item
# mutation {
#   updateItem(id: 1, name: "CPU Intel", description: "Tralalelo Tralala") {
#     name
#     description
#   }
# }


# Delete Item
# mutation {
#  deleteItem(id: 2)
# }
```