import sqlalchemy as db
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Boolean, Enum, Table
from sqlalchemy.sql import func
from sqlalchemy.orm import declarative_base, relationship
import enum

engine = db.create_engine('postgresql+psycopg2://postgres:thedogsofwar@localhost:5432/postgres')

Base = declarative_base()

conn = engine.connect() 


# Association Tables
user_roles = Table(
    'user_roles',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('role_id', Integer, ForeignKey('roles.id'), primary_key=True)
)


user_regions = Table(
    'user_regions',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('region_id', Integer, ForeignKey('regions.id'), primary_key=True)
)


# Main Tables
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String)
    email = Column(String, nullable=False, unique=True)
    age = Column(Integer)
    is_active = Column(Boolean, default=True, nullable=False)

    roles = relationship('Role', back_populates='users', secondary='user_roles')
    regions = relationship('Region', back_populates='users', secondary='user_regions')
    logs = relationship('AuditLog', back_populates='user')


class Role(Base):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(Text)

    users = relationship('User', back_populates='roles', secondary='user_roles')


class Region(Base):
    __tablename__ = 'regions'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

    users = relationship('User', back_populates='regions', secondary='user_regions')


class AuditAction(enum.Enum):
    LOGIN = 'LOGIN'
    LOGOUT = 'LOGOUT'
    QUERY = 'QUERY'
    ACCESS_DENIED = 'ACCESS_DENIED'
    SYSTEM_ERROR = 'SYSTEM_ERROR'
    UNAUTHORIZED = 'UNAUTHORIZED'
    VIEW_LOGS = 'VIEW_LOGS'
    DOWNLOAD = 'DOWNLOAD'
    

class AuditLog(Base):
    __tablename__ = 'audit_logs'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    action = Column(Enum(AuditAction), nullable=False)
    query_type = Column(String, nullable=False)
    success = Column(Boolean, default=True, nullable=False)
    details = Column(Text)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship('User', back_populates='logs')


Base.metadata.create_all(engine)
