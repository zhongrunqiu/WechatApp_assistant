#!/usr/bin/python
# -*-encoding=utf8 -*-

import os
import django
import logging

import sys
sys.path.append('/home/pi/github/WechatApp_assistant/')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

def logdemo():
    logger = logging.getLogger('django')
    logger.info('Hello logging')
    logger.debug('hello debug')
    logger.info('info---')


if __name__ == "__main__":
    logdemo()