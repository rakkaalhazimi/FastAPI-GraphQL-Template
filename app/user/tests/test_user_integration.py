def test_create_user_success(client):
    # This 'client' is automatically injected from conftest.py
    query = """
    mutation {
      createUser(usernameOrEmail: "test_dev", password: "Password123!") {
        id
        username
      }
    }
    """
    response = client.post("/graphql", json={"query": query})
    
    print(response.content)
    
    assert response.status_code == 200
    data = response.json()
    assert "errors" not in data
    assert data["data"]["createUser"]["username"] == "test_dev"


def test_create_user_invalid_password(client):
    # Testing the validation logic in auth.py through the GraphQL layer
    query = """
    mutation {
      createUser(usernameOrEmail: "test_dev", password: "123") {
        username
      }
    }
    """
    response = client.post("/graphql", json={"query": query})
    data = response.json()
    
    # We expect a GraphQL error because the password is too short
    assert "errors" in data
    assert "Password should be at least 8 characters" in data["errors"][0]["message"]