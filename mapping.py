from database import db
from flask import Blueprint
from models import Control, ControlDevice, ControlMulti, Room
import json
from sqlalchemy import func

mapping = Blueprint('api_v1_mapping', __name__)

@mapping.route('/map/<control_id>/<device_id>/<switch_id>', methods = ['PUT'])
def map(control_id, device_id, switch_id):
    control_device = db.session.scalars(
        db.select(ControlDevice).filter(ControlDevice.control_id == control_id)
    ).one_or_none()

    if control_device is None:
        control_device = ControlDevice(
            control_id = control_id,
            device_id = device_id,
            switch_id = switch_id
        )
        db.session.add(control_device)
    else:
        control_device.device_id = device_id
        control_device.switch_id = switch_id

    db.session.commit()

    return {
        'control_device': control_device.json()
    }

@mapping.route('/control/<control_id>/device', methods = ['GET'])
def device(control_id):
    control_device = db.session.scalars(
        db.select(ControlDevice).filter(ControlDevice.control_id == control_id)
    ).one_or_none()

    return {
        'control_device': control_device.json() if control_device is not None else None
    }

@mapping.route('/repopulate', methods = ['PUT'])
def repopulate():
    for obj in db.session.scalars(db.select(ControlDevice)).all():
        db.session.delete(obj)
    for obj in db.session.scalars(db.select(ControlMulti)).all():
        db.session.delete(obj)
    for obj in db.session.scalars(db.select(Control)).all():
        db.session.delete(obj)
    for obj in db.session.scalars(db.select(Room)).all():
        db.session.delete(obj)

    with mapping.open_resource('seed_data/rooms.json') as f:
        for room in json.load(f):
            obj = Room(
                id = room['id'],
                name = room['name']
            )
            db.session.add(obj)

    with mapping.open_resource('seed_data/controls.json') as f:
        for control in json.load(f):
            obj = Control(
                id = control['id'],
                room_id = control['room_id'],
                control_type = control['type'],
                name = control['name']
            )
            db.session.add(obj)

    with mapping.open_resource('seed_data/controls.json') as f:
        for control in json.load(f):
            print(control['combined_with'])
            for related_control_id in control['combined_with']:
                print(f'relating {control["id"]} and {related_control_id}')
                obj = ControlMulti(
                    control_one_id = control['id'],
                    control_two_id = related_control_id
                )
                db.session.add(obj)

    db.session.commit()

    return {
        'rooms': db.session.execute(db.select(func.count(Room.id))).scalar_one(),
        'controls': db.session.execute(db.select(func.count(Control.id))).scalar_one(),
        'control_multis': db.session.execute(db.select(func.count(ControlMulti.control_one_id))).scalar_one(),
        'control_devices': db.session.execute(db.select(func.count(ControlDevice.id))).scalar_one()
    }
