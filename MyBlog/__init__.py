
from pyramid.config import Configurator
from sqlalchemy import engine_from_config
from models import DBSession, Base
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from views import login
def main(global_config, **settings):
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    authentication_policy = AuthTktAuthenticationPolicy('somesecret')
    authorization_policy = ACLAuthorizationPolicy()
    config = Configurator(settings=settings,
                          authentication_policy=authentication_policy,
                          authorization_policy=authorization_policy)
    config.include('pyramid_mako')
    config.include('.models')
    config.add_route('index', '/')
    config.add_route('admin','/admin')
    config.add_route('blog_action', '/blog/{action}',
                     factory='.models.Root')
    config.add_route('blog_view','/blogview')
    config.scan()
    return config.make_wsgi_app()