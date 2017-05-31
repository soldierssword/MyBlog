#coding:utf-8
from pyramid.security import Allow, Everyone, Authenticated
import zope.sqlalchemy
import rediscon
import cPickle
from sqlalchemy.sql import func
from sqlalchemy import (
    Column,
    Integer,
    UnicodeText,
    DateTime,
    String,
    engine_from_config
)

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    configure_mappers
)

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(
    sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


class Article(Base):
    __tablename__ = 'article'
    uid = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(UnicodeText)
    body = Column(UnicodeText)
    date = Column(DateTime,default=func.now())
    @classmethod
    def add_all(cls,request):
        all = request.dbsession.query(Article).order_by(Article.date).all()
        p = rediscon.r.pipeline()
        p.set('article', cPickle.dumps(all))
        p.execute()
        return all


    @classmethod
    def get_all(cls,request):
        if rediscon.r.keys()==[] :
            return cls.add_all(request)
        else:
            return cPickle.loads(rediscon.r.get('article'))


    @classmethod
    def update_cache(cls,request):
        rediscon.r.flushdb()
        cls.add_all(request)




class Admin(Base):
    __tablename__ = 'admin'
    uid = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(32),unique=True)
    pw = Column(String(32))



class Root(object):
    __acl__ = [(Allow, Everyone, 'view'),
               (Allow, Authenticated, 'edit')]

    def __init__(self, request):
        pass


configure_mappers()

#配置引擎
def get_engine(settings, prefix='sqlalchemy.'):
    return engine_from_config(settings, prefix)
#创建事务工厂
def get_session_factory(engine):
    factory = sessionmaker()
    factory.configure(bind=engine)
    return factory
#配置transaction.manager
def get_tm_session(session_factory, transaction_manager):
    """
    Get a ``sqlalchemy.orm.Session`` instance backed by a transaction.
    This function will hook the session to the transaction manager which
    will take care of committing any changes.
    - When using pyramid_tm it will automatically be committed or aborted
      depending on whether an exception is raised.
    - When using scripts you should wrap the session in a manager yourself.
      For example::
          import transaction
          engine = get_engine(settings)
          session_factory = get_session_factory(engine)
          with transaction.manager:
              dbsession = get_tm_session(session_factory, transaction.manager)
    """
    dbsession = session_factory()
    zope.sqlalchemy.register(
        dbsession, transaction_manager=transaction_manager)
    return dbsession

#加入事务到request
def includeme(config):
    """
    Initialize the model for a Pyramid app.
    Activate this setup using ``config.include('pyramid_blogr.models')``.
    """
    settings = config.get_settings()

    # use pyramid_tm to hook the transaction lifecycle to the request
    config.include('pyramid_tm')

    session_factory = get_session_factory(get_engine(settings))
    config.registry['dbsession_factory'] = session_factory

    # make request.dbsession available for use in Pyramid
    config.add_request_method(
        # r.tm is the transaction manager used by pyramid_tm
        lambda r: get_tm_session(session_factory, r.tm),
        'dbsession',
        reify=True
    )