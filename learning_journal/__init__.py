import os
from pyramid.config import Configurator
from sqlalchemy import engine_from_config

from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy

from .security import EntryFactory

from .models import (
    DBSession,
    Base,
    )


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    # update building the configurator to pass in our policies
    if 'DATABASE_URL' in os.environ:
        settings['sqlalchemy.url'] = os.environ['DATABASE_URL']
    secret = os.environ.get('AUTH_SECRET', 'somesecret')
    authentication_policy=AuthTktAuthenticationPolicy(secret)
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    config = Configurator(
        settings=settings,
        authentication_policy=AuthTktAuthenticationPolicy('somesecret'),
        authorization_policy=ACLAuthorizationPolicy(),
        default_permission='view'
    )
    config.include('pyramid_jinja2')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/', factory=EntryFactory)
    config.add_route('detail', '/journal/{id:\d+}', factory=EntryFactory)
    config.add_route('action', '/journal/{action}', factory=EntryFactory)
    config.add_route('auth', '/sign/{action}', factory=EntryFactory)
    config.scan()
    return config.make_wsgi_app()

def create_session(settings):
    from sqlalchemy.orm import sessionmaker
    engine = engine_from_config(settings, 'sqlalchemy.')
    Session = sessionmaker(bind=engine)
    return Session()
