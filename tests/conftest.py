from fastapi.testclient import TestClient
from app import models
from app.main import app
import pytest
from app.database import Base,get_db
from sqlalchemy import create_engine
from app.config import setting
from sqlalchemy.orm import sessionmaker
from app.oauth import create_access_token
import sqlalchemy


SQL_ALCHEMY_DATABSE_URL=f'postgresql://{setting.database_username}:{setting.database_password}@{setting.database_hostname}:{setting.database_port}/{setting.database_name}_test'


print(SQL_ALCHEMY_DATABSE_URL)
engine=create_engine(SQL_ALCHEMY_DATABSE_URL)

TestingSessionLocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)

@pytest.fixture()
def session():
    # if not engine.dialect.has_schema(engine,f'{setting.database_name}_test'):
    #     engine.execute(sqlalchemy.schema.CreateSchema(f'{setting.database_name}_test'))
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db= TestingSessionLocal()
    try :
        yield db
    finally :
         db.close()


@pytest.fixture()
def client(session):
    def override_get_db() :
        try :
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db]=override_get_db
    yield TestClient(app)

@pytest.fixture
def test_user2(client):
    user_data={
        'email':'user2@example.com',
        'password':'password123'
    }
    res=client.post('/users/',json=user_data)
    assert res.status_code==201
    new_user=res.json()
    new_user['password']=user_data['password']
    return new_user

@pytest.fixture
def test_user(client):
    user_data={
        'email':'user@example.com',
        'password':'password123'
    }
    res=client.post('/users/',json=user_data)
    assert res.status_code==201
    new_user=res.json()
    new_user['password']=user_data['password']
    return new_user

@pytest.fixture()
def token(test_user):
    return create_access_token({'user_id':test_user['email']})

@pytest.fixture()
def authorized_client(client,token):
    client.headers={
        **client.headers,
        "Authorization":f"Bearer {token}"
    }

    return client

@pytest.fixture()
def test_posts(test_user,session,test_user2):
    posts_data=[{
        "title": "first title",
        "content": "first content",
        "owner_id": test_user['id']
    }, {
        "title": "2nd title",
        "content": "2nd content",
        "owner_id": test_user['id']
    },
        {
        "title": "3rd title",
        "content": "3rd content",
        "owner_id": test_user['id']
    }, {
        "title": "3rd title",
        "content": "3rd content",
        "owner_id": test_user2['id']
    }]

    def create_post_model(post):
        return models.Posts(**post)

    posts_map=map(create_post_model,posts_data)
    posts=list(posts_map)
    session.add_all(posts)
    session.commit()

    posts==session.query(models.Posts).all()
    return posts