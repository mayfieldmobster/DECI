import os
import socket
import random
import time
import numpy as np
import copy
import requests
import json
import zipfile


def send(host, port, message):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((host, port))
        client.send(message.encode("utf-8"))
    except:
        return "node offline"


def upload(filename, depen_zip, AM_I: bool = False, port="1379"):  # am i a worker
    script_identity = str(random.random())
    with open(filename, "r") as file:
        script = file.read().replace(" ", "`")

    with open(depen_zip, "rb") as file:
        zip_file = file.read()

    for line in script:
        if "tensorflow" in line:
            framework = "tensorflow"
            break

        elif "torch" in line:
            framework = "pytorch"
            break

    nodes = ["127.0.0.1:1379"]  # requests.get() # get request from website
    my_ip = requests.get('https://api.ipify.org').text


    if AM_I:
        for node in nodes:
            node = node.split(":")
            send(node[0], int(node[1]), f"DIST {script_identity} {script}")

            send(node[0], int(node[1]), f"DEP {script_identity} {zip_file.hex()}")



    if not AM_I:
        for node in nodes:
            node = node.split(":")
            send(node[0], int(node[1]), f"DIST {script_identity} {script}")
            time.sleep(0.5)
            send(node[0], int(node[1]), f"DEP {script_identity} {zip_file.hex()}")


if __name__ == "__main__":
    file = "./model.py"
    dependencies = "./iCloudSetup.zip"
    upload(file, dependencies)
