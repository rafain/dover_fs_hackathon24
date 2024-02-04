from azure.storage.blob import ContainerClient
import yaml
import os
import numpy as np
from datetime import datetime
import json

class Nishant():
    def __init__(self):
        self.config = self.load_config()
        self.hist = []
    
    def load_config(self):
        # dir_root = os.path.dirname(os.path.abspath(__file__))
        with open ("F:\Code\config.yaml", "r") as yamlfile:
            return yaml. load (yamlfile, Loader=yaml. FullLoader)
    
    def upload_blob(self, file_path, conatiner):
        container_client = ContainerClient.from_connection_string (self.config["azure_storage_connectionstring"], 
                                                                   self.config[conatiner])
        blob_client = container_client.get_blob_client(file_path)
        with open(file_path,"rb") as data:
            blob_client.upload_blob(data)
        
    def add_log(self, log):
        if len(self.hist)==25:
            self.hist.pop(0)
            self.hist.append(log)
        else:
            self.hist.append(log)

    def Faliure_P4(self, log):
        log_push = {}

        log_push["device_id"] = self.config["device_id"]
        log_push["datetime"] = str(datetime.now())
        log_push["error_type"] = "SPM 2 Memory reaching Capacity"
        log_push["Priority"] = 3
        log_push["Last_Log"] = log
        log_push["logs"] = self.hist.reverse()

        log_file_name = self.config["device_id"] + "_" + str(datetime.now()) + ".json"
        log_file_name = log_file_name.strip().replace(":","").replace(" ","").replace("-","_")
        print(f"Pushing file {log_file_name} to cloud...")
        with open(log_file_name, 'w') as fp:
            json.dump(log_push, fp)

        self.upload_blob(log_file_name, "error_container_name")
        os.remove(log_file_name)
        print("Completed...")

    def Faliure_P3(self, log):
        log_push = {}

        log_push["device_id"] = self.config["device_id"]
        log_push["datetime"] = str(datetime.now())
        log_push["error_type"] = "Time Reading Backwards"
        log_push["Priority"] = 3
        log_push["Last_Log"] = log
        log_push["logs"] = self.hist.reverse()

        log_file_name = self.config["device_id"] + "_" + str(datetime.now()) + ".json"
        log_file_name = log_file_name.strip().replace(":","").replace(" ","").replace("-","_")
        print(f"Pushing file {log_file_name} to cloud...")
        with open(log_file_name, 'w') as fp:
            json.dump(log_push, fp)

        self.upload_blob(log_file_name, "error_container_name")
        os.remove(log_file_name)
        print("Completed...")
    
    def Faliure_P2(self, log):
        log_push = {}

        log_push["device_id"] = self.config["device_id"]
        log_push["datetime"] = str(datetime.now())
        log_push["error_type"] = "Keypad Not Working"
        log_push["Priority"] = 0
        log_push["Last_Log"] = log
        log_push["logs"] = self.hist.reverse()

        log_file_name = self.config["device_id"] + "_" + str(datetime.now()) + ".json"
        log_file_name = log_file_name.strip().replace(":","").replace(" ","").replace("-","_")
        print(f"Pushing file {log_file_name} to cloud...")
        with open(log_file_name, 'w') as fp:
            json.dump(log_push, fp)

        self.upload_blob(log_file_name, "error_container_name")
        os.remove(log_file_name)
        print("Completed...")
    
    def Faliure_P1(self, log):
        log_push = {}

        log_push["device_id"] = self.config["device_id"]
        log_push["datetime"] = str(datetime.now())
        log_push["error_type"] = "Copius: Payment inside only"
        log_push["Priority"] = 1
        log_push["Last_Log"] = log
        log_push["logs"] = self.hist.reverse()

        log_file_name = self.config["device_id"] + "_" + str(datetime.now()) + ".json"
        log_file_name = log_file_name.strip().replace(":","").replace(" ","").replace("-","_")
        print(f"Pushing file {log_file_name} to cloud...")
        with open(log_file_name, 'w') as fp:
            json.dump(log_push, fp)

        self.upload_blob(log_file_name, "error_container_name")
        os.remove(log_file_name)
        print("Completed...")
    
    def CriticalFaliure_P0(self, log):
        log_push = {}
        log_push["device_id"] = self.config["device_id"]
        log_push["datetime"] = str(datetime.now())
        
        if log.find("OpenContactlessReaderResponse")!=-1:
            log_push["error_type"] = "Contactless Reader Critical Faliure"
        elif log.find("OpenChipCardReaderResponse")!=-1:
            log_push["error_type"] = "Open Chip Reader Critical Faliure"
        
        log_push["Priority"] = 0
        log_push["Last_Log"] = log
        log_push["logs"] = self.hist.reverse()

        log_file_name = self.config["device_id"] + "_" + str(datetime.now()) + ".json"
        log_file_name = log_file_name.strip().replace(":","").replace(" ","").replace("-","_")
        print(f"Pushing file {log_file_name} to cloud...")
        with open(log_file_name, 'w') as fp:
            json.dump(log_push, fp)

        self.upload_blob(log_file_name, "error_container_name")
        os.remove(log_file_name)
        print("Completed...")
