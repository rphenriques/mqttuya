# -*- coding: utf-8 -*-
"""
 MQTTuya - TinyTuya <-> MQTT Bridge

 Author: Rui Pedro Henriques
 For more information see https://github.com/rphenriques/mqttuya

"""

import json
import os
import random
from paho.mqtt import client as mqtt_client
import towel_heater
# import sched, time

# s = sched.scheduler(time.time, time.sleep)

device_list = {}


def create_device(device_data):
    """
    Create and initialize tuya device

    Args:
        device_data(json): device data
    """
    for device in device_data:
        # TODO: if IP is None, "Auto" or 0.0.0.0", init will find the device IP and VERSION. This should be used to set version
        # TODO: BUT if IP is SET, the version returned may be wrong because find() is not used
        aux_device = towel_heater.TowelHeaterDevice(
            device['id'], device['ip'], device['key'])
        if(device['ver'] == '3.3'):    # IMPORTANT to always set version
            aux_device.set_version(3.3)
        else:
            aux_device.set_version(3.1)
        # Keep socket connection open between commands
        # aux_device.set_socketPersistent(True)
        device_list[device['id']] = aux_device
        print(f"Created device {device['id']}")


def connect_mqtt(broker, port, username=None, password=None, client_id=None):
    """
    Connect to MQTT Broker
    """
    def on_connect(client, userdata, flags, rc):
        """
        hook for when the client connects to the broker
        """
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client_id = client_id if client_id else f'mqttuya-{random.randint(0, 1000)}'
    client = mqtt_client.Client(client_id)
    if username and password:
        client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def publish_status(client, device_id):
    """
    Publish status to MQTT Broker

    Args:
        client(mqtt_client): MQTT Client
        device_id(str): device ID
    """
    if device_id not in device_list:
        print("Not here")
        return False
    status_topic = f"mqttuya/status/{device_id}"
    data_topic = f"mqttuya/data/{device_id}"
    print("Publishing status")
    client.publish(
        status_topic, json.dumps(device_list[device_id].status()))
    client.publish(
        data_topic, json.dumps(device_list[device_id].get_data()))


def on_message(client, userdata, msg):
    """
    Hook to be called when a message is received. Calls the appropriate function
    depending on the cmd received.
    """

    data = json.loads(msg.payload)
    print(f"Received `{data}` from `{msg.topic}` topic")

    if 'cmd' not in data:
        aux_msg = {'status': 'error',
                   'msg': 'Invalid message', 'original_msg': data}
        client.publish("mqttuya/monitor", json.dumps(aux_msg))
        print(aux_msg)
        return False

    if data['cmd'] == 'config':
        if 'value' not in data:
            aux_msg = {'status': 'error',
                    'msg': 'Invalid message', 'original_msg': data}
            client.publish("mqttuya/monitor", json.dumps(aux_msg))
            print(aux_msg)
            return False
        create_device(device_data=data['value'])
        for device in data['value']:
            publish_status(client=client, device_id=device['id'])
        return True

    if 'value' not in data or 'id' not in data:
        aux_msg = {'status': 'error',
                   'msg': 'Invalid message', 'original_msg': data}
        client.publish("mqttuya/monitor", json.dumps(aux_msg))
        print(aux_msg)
        return False

    if data['id'] not in device_list and data['cmd'] != 'config':
        aux_msg = {'status': 'error',
                   'msg': 'Unknown device', 'original_msg': data}
        client.publish("mqttuya/monitor", json.dumps(aux_msg))
        print(aux_msg)
        return False

    if data['cmd'] == 'status':
        publish_status(client, data['id'])
    elif data['cmd'] == 'turn_on':
        device_list[data['id']].turn_on()
        publish_status(client, data['id'])
    elif data['cmd'] == 'turn_off':
        device_list[data['id']].turn_off()
        publish_status(client, data['id'])
    elif data['cmd'] == 'lock':
        device_list[data['id']].lock()
        publish_status(client, data['id'])
    elif data['cmd'] == 'unlock':
        device_list[data['id']].unlock()
        publish_status(client, data['id'])
    elif data['cmd'] == 'set_temp':
        device_list[data['id']].set_temp(data['value'])
        publish_status(client, data['id'])
    elif data['cmd'] == 'set_timer':
        device_list[data['id']].set_timer(data['value'])
        publish_status(client, data['id'])
    elif data['cmd'] == 'timer_off':
        device_list[data['id']].timer_off()
        publish_status(client, data['id'])
    elif data['cmd'] == 'open':
        device_list[data['id']].open()
        publish_status(client, data['id'])
    elif data['cmd'] == 'close':
        device_list[data['id']].close()
        publish_status(client, data['id'])
    else:
        aux_msg = {'status': 'error',
                   'msg': 'Unknown message', 'original_msg': data}
        client.publish("mqttuya/monitor", json.dumps(aux_msg))
        print(aux_msg)


def subscribe(client, topic_list):
    """
    Set target temp

    Args:
        client(Client): active mqtt client
        topic_list(list): list of topics to subscribe
    """
    for topic in topic_list:
        client.subscribe(topic)
        print(f"Subscribed to {topic}")
    client.on_message = on_message


def run():
    """
    default run function: connect to broker and subscribe to topics
    """

    BROKER = os.getenv("BROKER", 'test.mosquitto.org')
    PORT = int(os.getenv("PORT", '1883'))
    USERNAME = os.getenv("USERNAME", None)
    PASSWORD = os.getenv("PASSWORD", None)
    CLIENTID = os.getenv("CLIENTID", None)

    SUB_TOPICS_LIST = json.loads(os.getenv("SUB_TOPICS_LIST", "mqttuya/sub"))

    client = connect_mqtt(broker=BROKER, port=PORT,
                          username=USERNAME, password=PASSWORD, client_id=CLIENTID)
    subscribe(client=client, topic_list=SUB_TOPICS_LIST)
    client.loop_forever()


if __name__ == '__main__':
    run()
