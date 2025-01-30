import sys
import os
from fastapi.testclient import TestClient

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')

from app.main import app
from app.auth.auth_service import create_access_token, decode_access_token

client = TestClient(app)

token = create_access_token(user_id=1)
print(token)

response = client.post("/notes", json={"title": "Test", "content": "Test content", "token": token})
print(response.json())

payload = decode_access_token(token)
print(payload)
