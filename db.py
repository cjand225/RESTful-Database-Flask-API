import datetime
from sqlalchemy import create_engine, ForeignKey, Table, MetaData, Column, Integer, String, DateTime, Sequence, \
    PrimaryKeyConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

Base = declarative_base()


class Location(Base):
    __tablename__ = 'location'
    # Columns
    lid = Column('lid', Integer, primary_key=True, autoincrement=True)
    address = Column('address', String(100))
    # Relationship
    services = relationship('Service', cascade="save-update, merge, delete")

    def __repr__(self):
        return "<Location(lid='%s', address='%s')>" % (
            self.lid, self.address)


class Institution(Base):
    __tablename__ = 'institution'
    # Columns
    id = Column(Integer, primary_key=True, autoincrement=True)
    tid = Column('tid', String(100))
    # Relationship
    departments = relationship('Department')

    def __repr__(self):
        return "<Institution(id='%s', tid='%s')>" % (
            self.id, self.tid)


class Department(Base):
    __tablename__ = 'department'

    # Columns
    id = Column('id', String(100), primary_key=True)
    institution_id = Column('institution_id', ForeignKey('institution.id'))
    # Relationship
    institution = relationship('Institution')
    services = relationship('Service')
    providers = relationship('Provider')

    def __repr__(self):
        return "<Department(id='%s', institution_id='%s')>" % (
            self.id, self.institution_id)


class Service(Base):
    __tablename__ = 'service'

    # Columns
    id = Column('id', String(100), primary_key=True)
    location_id = Column('location_id', ForeignKey('location.lid'))
    department_id = Column('department_id', ForeignKey('department.id'))

    # Relationship
    patientData = relationship('Data', cascade="save-update, merge, delete")

    def __repr__(self):
        return "<Service(id='%s', location_id='%s', department_id='%s')>" % (
            self.id, self.location_id, self.department_id)


class Provider(Base):
    __tablename__ = 'provider'
    # Columns
    npi = Column('npi', String(100), primary_key=True)
    department_id = Column('department_id', ForeignKey('department.id'))
    # Relationship
    patients = relationship('Patient')

    def __repr__(self):
        return "<Provider(npi='%s', department_id='%s')>" % (
            self.npi, self.department_id)


class Patient(Base):
    __tablename__ = 'patient'
    # Columns
    pid = Column('pid', String(100), primary_key=True)
    ssn = Column('ssn', String(100))
    address = Column('address', String(100))
    provider_id = Column('provider_id', ForeignKey('provider.npi'))

    # Relationship
    patientData = relationship('Data')

    def __repr__(self):
        return "<Patient(pid='%s', ssn='%s', address='%s', provider_id='%s')>" % (
            self.pid, self.ssn, self.address, self.provider_id)


class Data(Base):
    __tablename__ = 'data'
    # Columns
    id = Column('id', String(100), primary_key=True)
    ts = Column('ts', DateTime, onupdate=datetime.datetime.utcnow)
    patient_id = Column('patient_id', ForeignKey('patient.pid'))
    service_id = Column('service_id', ForeignKey('service.id'))
    some_data = Column('some_data', String(200))

    def __repr__(self):
        return "<Data(id='%s', ts='%s', patient_id='%s', service_id='%s', some_data='%s')>" % (
            self.id, self.ts, self.patient_id, self.service_id, self.some_data)
