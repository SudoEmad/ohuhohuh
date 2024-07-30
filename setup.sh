#!/bin/bash

# تثبيت مكتبة paramiko
pip3 install paramiko

# تشغيل سكربت مولد عناوين IP
python3 ip_generator.py

# تشغيل سكربت SSH Brute Force
python3 SSH_Brute_Force.py
