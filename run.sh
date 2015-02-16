#!/bin/bash
screen -s py python server.py
sleep 1
cd websockify
screen -s web ./run 8081 localhost:8888
