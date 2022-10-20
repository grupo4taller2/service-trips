from src.entrypoints.http.main import app
from behave import fixture, use_fixture
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.conf import config

Session = sessionmaker(bind=create_engine(config.Settings().DATABASE_URI))
session = Session()


@fixture
def app_client(context, *args, **kwargs):
    context.client = TestClient(app)
    yield context.client


def before_feature(context, feature):
    use_fixture(app_client, context)
    context.vars = {}


def after_scenario(context, scenario):
    pass


def after_all(context):
    session.commit()
    session.close()
