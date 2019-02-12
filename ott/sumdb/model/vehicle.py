import datetime
from sqlalchemy import Column, Index, Integer, Numeric, String, DateTime
from sqlalchemy.sql import func, and_
from sqlalchemy.orm import deferred, object_session, relationship

from .base import Base
from .vehicle_position import VehiclePosition

import logging
log = logging.getLogger(__file__)


class Vehicle(Base):
    __tablename__ = 'vehicles'

    vehicle_id = Column(String, nullable=False)
    license_plate = Column(String)
    fuel_type = Column(String)

    positions = relationship(
        'VehiclePosition',
        primaryjoin='Vehicle.vehicle_id == VehiclePosition.vehicle_id',
        foreign_keys='(Vehicle.vehicle_id)',
        uselist=True, viewonly=True,
        backref="vehicle"
    )

    def __init__(self, agency, vehicle_id, license_plate=None):
        self.agency = agency
        self.vehicle_id = vehicle_id
        self.license_plate = license_plate

    @classmethod
    def clear_tables(cls, session, agency):
        """
        clear out the positions and vehicles tables
        """
        VehiclePosition.clear_tables(session, agency)
        session.query(Vehicle).filter(Vehicle.agency == agency).delete()
        session.commit()

    def update_position(self, session, agency, data, time_span=144):
        """ query the db for a position for this vehicle ... if the vehicle appears to be parked in the
            same place as an earlier update, update the 
            NOTE: the position add/update needs to be committed to the db by the caller of this method 
        """

        # step 0: cast some variables
        lat = round(data.position.latitude,  6)
        lon = round(data.position.longitude, 6)

        # step 1: get position object from db ...criteria is to find last position 
        #          update within an hour, and the car hasn't moved lat,lon
        hours_ago = datetime.datetime.now() - datetime.timedelta(hours=time_span)
        p = None
        try:
            q = session.query(VehiclePosition).filter(
                and_(
                    VehiclePosition.vehicle_fk == self.id,
                    VehiclePosition.updated >= hours_ago,
                    VehiclePosition.lat == lat,
                    VehiclePosition.lon == lon,
                )
            )
            p = q.first()
        except Exception as err:
            log.exception(err)

        # step 2: we didn't find an existing position in the Position history table, so add a new one
        try:
            if p is None:
                p = VehiclePosition()
                p.vehicle_fk = self.id
                p.agency = agency
                p.set_attributes(data)
                p.set_position(lat, lon)
                session.add(p)
            else:
                p.set_updated()

        except Exception as err:
            log.exception(err)
            session.rollback()
        finally:
            try:
                session.commit()
                session.flush()
            except Exception as err:
                log.exception(err)
                session.rollback()
        return p
