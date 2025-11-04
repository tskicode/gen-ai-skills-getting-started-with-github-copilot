import pytest
from fastapi.testclient import TestClient
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from src.app import app

@pytest.fixture
def client():
    """
    Test client fixture that can be used across tests
    """
    return TestClient(app)

@pytest.fixture
def test_activity():
    """
    Sample activity data for testing
    """
    return {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu"]
        }
    }