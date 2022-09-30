import logging
import sys
import datetime
from get_data import Authenticator
from datahandler import DataHandler
from mqtt import MQTTPublish

MQTT_IP = sys.argv[1]
MQTT_USERNAME = sys.argv[2]
MQTT_PASSWORD = sys.argv[3]
TEAPI_USERNAME = sys.argv[4]
TEAPI_PASSWORD = sys.argv[5]

# MQTT Publish
mqtt = MQTTPublish(
    ip=MQTT_IP,
    username=MQTT_USERNAME,
    password=MQTT_PASSWORD,
    datafile="values.txt"
)

today = datetime.datetime.today()

auth = Authenticator(TEAPI_USERNAME, TEAPI_PASSWORD, "excel.xlsx")
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
