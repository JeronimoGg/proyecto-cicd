import pytest
from app.app import app  # Ajusta el import si tu archivo principal está en otro módulo

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client
