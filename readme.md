## TODO:
- Find out where GraphQL client lives
  In FastAPI, graphQL lives in the `.py` file. Schema is the brain, FastAPI is the door and middleware is the bridge.
  
- Validation and Error Handling
  
- Authorization 
  Login -> Get JWT Token
  Login with Google
  
- Database Migrations
  
- Payment


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