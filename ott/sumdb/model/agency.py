import datetime
from sqlalchemy import Column, Index, Integer, Numeric, String, DateTime
from sqlalchemy.sql import func, and_
from sqlalchemy.orm import deferred, object_session, relationship

from .base import Base

import logging
log = logging.getLogger(__file__)


class Agency(Base):
    __tablename__ = 'agencies'

    agency_id = Column(String, nullable=False)
    agency_url = Column(String)

    def __init__(self, agency_id, agency_url=None):
        self.agency_id = agency_id
        self.agency_url = agency_url

    @classmethod
    def add_geometry_column(cls, srid=4326):
        cls.geom = Column(Geometry(geometry_type='POINT', srid=srid))

    @classmethod
    def set_boundary(cls, url):
        pass
