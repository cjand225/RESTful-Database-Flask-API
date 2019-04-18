import datetime
from sqlalchemy import create_engine, ForeignKey, Table, MetaData, Column, Integer, String, DateTime, Sequence, \
    PrimaryKeyConstraint
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import relationship, backref

Base = declarative_base()
#s


class Location(Base):
    __tablename__ = 'location'

    lid = Column('lid', Integer, primary_key=True, unique=True, nullable=False)
    address = Column('address', String(100))

    services = relationship('Service', backref='service')

    def __init__(self, lid, address):
        self.lid = lid
        self.address = address


class Institution(Base):
    __tablename__ = 'institution'
    id = Column('id', Integer, primary_key=True, unique=True, nullable=False)
    tid = Column('tid', Integer, unique=True, nullable=False)

    departments = relationship('Department', backref='department')

    def __init__(self, id, tid):
        self.id = id
        self.tid = tid


class Department(Base):
    __tablename__ = 'department'
    __table_args__ = (
        PrimaryKeyConstraint('id', 'institution_id'),
    )
    id = Column('id', Integer, unique=True, nullable=False)
    institution_id = Column('institution_id', Integer, ForeignKey('institution.id'))

    institution = relationship('Institution', backref='institution')
    services = relationship('Service', backref='service')
    providers = relationship('Provider', backref='provider')

    def __init__(self, id, institution_id):
        self.id = id
        self.institution_id = institution_id


class Service(Base):
    __tablename__ = 'service'
    id = Column('id', Integer, primary_key=True, unique=True, nullable=False)
    location_id = Column('location_id', Integer, ForeignKey('location.lid'))
    department_id = Column('department_id', Integer, ForeignKey('department.id'))

    patientData = relationship('Data', backref='data')

    def __init__(self, id, location_id, department_id):
        self.id = id
        self.location_id = location_id
        self.department_id = department_id


class Provider(Base):
    __tablename__ = 'provider'
    __table_args__ = (
        PrimaryKeyConstraint('npi'),
    )
    npi = Column('npi', Integer, unique=True, nullable=False)
    department_id = Column('department_id', Integer, ForeignKey('department.id'))

    patients = relationship('Patient', backref='patient')

    def __init__(self, npi, department_id):
        self.npi = npi
        self.department_id = department_id


class Patient(Base):
    __tablename__ = 'patient'
    __table_args__ = (
        PrimaryKeyConstraint('pid', 'ssn'),
    )

    pid = Column('pid', Integer, unique=True, nullable=False)
    ssn = Column('ssn', Integer)
    address = Column('address', String(100))
    provider_id = Column('provider_id', Integer, ForeignKey('provider.npi'))

    patientData = relationship('Data', backref='data')

    def __init__(self, pid, ssn, address, provider_id):
        self.pid = pid
        self.ssn = ssn
        self.address = address
        self.provider_id = provider_id


class Data(Base):
    __tablename__ = 'data'
    __table_args__ = (
        PrimaryKeyConstraint('id', 'patient_id'),
    )

    id = Column('id', Integer, unique=True, nullable=False)
    ts = Column('ts', DateTime, onupdate=datetime.datetime.utcnow)
    patient_id = Column('patient_id', Integer, ForeignKey('patient.pid'))
    service_id = Column('service_id', Integer, ForeignKey('service.id'))
    some_data = Column('some_data', String(200))

    def __init__(self, id, ts, patient_id, service_id, some_data):
        self.id = id
        self.ts = ts
        self.patient_id = patient_id
        self.service_id = service_id
        self.some_data = some_data
