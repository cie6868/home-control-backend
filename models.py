from database import db
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

class Room(db.Model):
    __tablename__ = 'rooms'

    id = Column(Integer, primary_key = True)
    name = Column(String, nullable = False)

    controls = relationship('Control', back_populates = 'room')

    def json(self):
        return {
            'id': self.id,
            'name': self.name
        }

class Control(db.Model):
    __tablename__ = 'controls'

    id = Column(Integer, primary_key = True)
    room_id = Column(Integer, db.ForeignKey('rooms.id'))
    control_type = Column(Integer)
    name = Column(String, nullable = False)

    room = relationship('Room', back_populates = 'controls')
    devices = relationship('ControlDevice', back_populates = 'control')

    def json(self):
        return {
            'id': self.id,
            'room_id': self.room_id,
            'control_type': self.control_type,
            'name': self.name,
            'room': self.room.json()
        }

class ControlMulti(db.Model):
    __tablename__ = 'control_multi_mapping'

    control_one_id = Column(Integer, primary_key = True)
    control_two_id = Column(Integer, primary_key = True)

class ControlDevice(db.Model):
    __tablename__ = 'control_device_mapping'

    id = Column(Integer, primary_key = True, autoincrement = True)
    control_id = Column(Integer, db.ForeignKey('controls.id'), unique = True)
    device_id = Column(String, nullable = False)
    switch_id = Column(Integer)

    control = relationship('Control', back_populates = 'devices')

    def json(self):
        return {
            'id': self.id,
            'control_id': self.control_id,
            'device_id': self.device_id,
            'switch_id': self.switch_id,
            'control': self.control.json()
        }
