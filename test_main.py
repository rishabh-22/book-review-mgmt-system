from fastapi.testclient import TestClient
from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import sessionmaker
from main import app, get_db

client = TestClient(app)


DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    DATABASE_URL,
    connect_args={
        "check_same_thread": False,
    },
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency to override the get_db dependency in the main app
def override_get_db():
    database = TestingSessionLocal()
    yield database
    database.close()


app.dependency_overrides[get_db] = override_get_db


def test_get_all_books():
    response = client.get("/books/all")
    assert response.status_code == 200
    assert response.json() == []


def test_add_new_book():
    response = client.post("/books/add", json={"title": "book1", "author": "rishabh", "author_email": "rb@test.com",
                                               "publication_year": 2024})
    assert response.status_code == 200
    assert response.json() == {"message": "success"}


def test_get_all_books2():
    response = client.get("/books/all")
    assert response.status_code == 200
    assert response.json() == {"book_id": 1, "title": "book1", "author": "rishabh",
                               "publication_year": 2024, "price": 0}


def test_add_new_review():
    response = client.post("/review/add", json={"book_id": 1, "text": "new review", "rating": 5})
    assert response.status_code == 200
    assert response.json() == {"message": "success"}

