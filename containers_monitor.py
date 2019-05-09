#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
import logging
import docker

# time in seconds
SLEEP_TIME = 3600 # 1 hs sleep
WAIT_RESTART_TIME = 10

logger = logging.getLogger('monitoring')
hdlr = logging.FileHandler(os.getcwd() + '/containers.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr) 
logger.setLevel(logging.DEBUG)

restart_list_names = [] # names of the containers you want to restart if they are down
proyect_containers_name = ""  # name of the proyect, name with which the containers start

def check_container_status():
    for container in client.containers.list(filters={"status": "exited"}):
        if (proyect_containers_name != "" and proyect_containers_name in container.name) or (container.name in restart_list_names):
            container.restart()
            logger.error(u"- RESTARTING - " + container.name)
            time.sleep(WAIT_RESTART_TIME)
            # wait x seconds before checking if the restart was successful.
            cont_restart = client.containers.get(container.name)
            if cont_restart.status == 'running':
                logger.info(u"- RESTART SUCCESS - " + container.name)
            else:
                logger.error(u'- RESTART FAIL - ' + container.name)
    for container in client.containers.list():
        if container.status == 'running':
            logger.info(u"- OK - " + container.name)
        else:
            logger.warning(u"- WARNING - " + container.name)

client = docker.from_env()

while True:
    check_container_status()
    time.sleep(SLEEP_TIME)