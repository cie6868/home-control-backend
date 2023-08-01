from flask import Blueprint
import json
import tinytuya

device = Blueprint('api_v1_device', __name__)

def init_device(device_id):
    return tinytuya.OutletDevice(
        dev_id = device_id,
        address = 'Auto',
        version = '3.3'
    )

@device.route('/list', methods = ['GET'])
def list():
    with device.open_resource('devices.json') as f:
        data = json.load(f)

        return {
            'response': data
        }

@device.route('/scan', methods = ['POST'])
def scan():
    devices = tinytuya.deviceScan()

    return {
        'response': devices
    }

@device.route('/<device_id>/<switch_id>/status', methods = ['GET'])
def status(device_id, switch_id):
    device = init_device(device_id)

    response = device.status()

    switch_status = response['dps'][switch_id]

    return {
        'value': switch_status,
        'response': response
    }

@device.route('/<device_id>/<switch_id>/on', methods = ['PUT'])
def on(device_id, switch_id):
    device = init_device(device_id)

    response = device.set_status(True, switch = switch_id)

    switch_status = response['dps'][switch_id]

    return {
        'value': switch_status,
        'response': response
    }

@device.route('/<device_id>/<switch_id>/off', methods = ['PUT'])
def off(device_id, switch_id):
    device = init_device(device_id)

    response = device.set_status(False, switch = switch_id)

    switch_status = response['dps'][switch_id]

    return  {
        'value': switch_status,
        'response': response
    }

@device.route('/<device_id>/dim/<pct>', methods = ['PUT'])
def dim(device_id, pct):
    device = init_device(device_id)

    value = int(int(pct) * 255 / 100)

    response = device.set_value(2, value)

    return  {
        'dim': pct,
        'response': response
    }
