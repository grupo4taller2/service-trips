from src.webapi.main import app
from behave import fixture, use_fixture
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.conf import config
from sqlalchemy import text

Session = sessionmaker(bind=create_engine(config.Settings().DATABASE_URI))
session = Session()


@fixture
def app_client(context, *args, **kwargs) -> TestClient:
    context.client: TestClient = TestClient(app)
    yield context.client


def before_feature(context, feature):
    use_fixture(app_client, context)
    q = 'TRUNCATE TABLE taken_trips, requested_trips CASCADE'
    session.execute(text(q))
    session.flush()
    session.commit()
    context.vars = {}


def after_scenario(context, scenario):
    pass


def after_all(context):
    session.commit()
    session.close()
