import datetime
from sqlalchemy import create_engine, ForeignKey, Table, MetaData, Column, Integer, String, DateTime, Sequence, \
    PrimaryKeyConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

metadata = MetaData()
location = Table('location', metadata,
                 Column('id', Integer, primary_key=True, autoincrement=True),
                 Column('address', String(100)),
                 relationship('service')
                 )

institution = Table('institution', metadata,
                    # Columns
                    Column('id', Integer, primary_key=True, autoincrement=True),
                    Column('tid', String(100)),
                    relationship('department')
                    )

department = Table('department', metadata,
                   Column('id', String(100), primary_key=True),
                   Column('institution_id', ForeignKey('institution.id')),
                   relationship('institution'),
                   relationship('service'),
                   relationship('provider'),
                   )

service = Table('service', metadata,
                Column('id', String(100), primary_key=True),
                Column('location_id', ForeignKey('location.lid')),
                Column('department_id', ForeignKey('department.id')),
                relationship('data')
                )

provider = Table('provider', metadata,
                 Column('npi', String(100), primary_key=True),
                 Column('department_id', ForeignKey('department.id')),
                 relationship('patient')
                 )

patient = Table('patient', metadata,
                Column('pid', String(100), primary_key=True),
                Column('ssn', String(100)),
                Column('address', String(100)),
                Column('provider_id', ForeignKey('provider.npi')),
                relationship('data')
                )

data = Table('data', metadata,
             Column('id', String(100), primary_key=True),
             Column('ts', DateTime, onupdate=datetime.datetime.utcnow),
             Column('patient_id', ForeignKey('patient.pid')),
             Column('service_id', ForeignKey('service.id')),
             Column('some_data', String(200))
             )
