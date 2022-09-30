import time
import json
import paho.mqtt.client as mqtt 


class MQTTPublish:
    topic_preset = "homeassistant/sensor/teapi_energy/"

    def __init__(self, ip, username, password, datafile):
        self.ip = ip
        self.username = username
        self.password = password
        self.datafile = datafile

        self.client = mqtt.Client("teapi_energy_consumption")
        self.client.username_pw_set(username, password)
        self.client.connect(ip, 1883, 60)

        # Publish initial config
        self._publish_config()

    def read_values(self):
        with open(self.datafile, "r") as file:
            values = file.readline()
            values = values.split("|")
            
            self.state_payload = {
                "date": values[0],
                "kwh": values[1],
                "temperature": values[2]
            }

    def _publish_config(self):
        payload = {
            "name": "teapi_energy_consumption",
            "device_class": "temperature",
            "state_topic": "homeassistant/sensor/teapi_energy/state",
            "unique_id": "teapi-daily-kwh-consumption",
            "value_template": "{{ value_json.kwh }}"
        }
        self.client.publish(
            "{}config".format(self.topic_preset),
            json.dumps(payload),
            retain=True
        )

    def publish_state(self):
        self.client.publish(
            "{}state".format(self.topic_preset),
            json.dumps(self.state_payload)
        )
