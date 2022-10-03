import logging
import sys
import datetime
from get_data import Authenticator
from datahandler import DataHandler
from mqtt import MQTTPublish

settings = dict()
settings["MQTT_IP"] = sys.argv[1]
settings["MQTT_USERNAME"] = sys.argv[2]
settings["MQTT_PASSWORD"] = sys.argv[3]
settings["TEAPI_USERNAME"] = sys.argv[4]
settings["TEAPI_PASSWORD"] = sys.argv[5]

for key, value in settings.items():
    if not value:
        print("{} not defined.".format(key))

# MQTT Publish
mqtt = MQTTPublish(
    ip=settings["MQTT_IP"],
    username=settings["MQTT_USERNAME"],
    password=settings["MQTT_PASSWORD"],
    datafile="values.txt",
)

today = datetime.datetime.today()

auth = Authenticator(
    settings["TEAPI_USERNAME"], settings["TEAPI_PASSWORD"], "excel.xlsx"
)
if auth.authenticate():
    print("Authentication successful on {}".format(today))
    if auth.save_excel_to_file():
        print("Excel file fetched on {}".format(today))
        handler = DataHandler("excel.xlsx")
        handler.read_excel_file()
        valuesfile = handler.write_results_to_file("values.txt")

        mqtt.read_values()
        mqtt.publish_state()
        print("New values published on {}".format(today))

    auth.logout()
