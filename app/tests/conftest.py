# from main import app
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from core.settings import Settings
# from fastapi.testclient import TestClient
# from core.dependencies import get_db
# import models.department
# import models.seller
# import models.user


# SQLALCHEMY_DATABASE_URL: str = "postgresql+psycopg2://postgres:12345@localhost:5430/test-db"

# engine = create_engine(SQLALCHEMY_DATABASE_URL)
# TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Settings.DBBaseModel.metadata.drop_all
# Settings.DBBaseModel.metadata.create_all

# def override_get_db():
#     try:
#         db = TestingSessionLocal()
#         yield db
#     finally:
#         db.close()


# app.dependency_overrides[get_db] = override_get_db

# client = TestClient(app)
