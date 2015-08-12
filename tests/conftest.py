from app import create_app
import pytest


@pytest.fixture(scope='session')
def app():
	"""Creates an app with test settings"""
	app = create_app()
	return app


test = app()