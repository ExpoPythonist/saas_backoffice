#!/usr/bin/env bash
sudo git pull
sudo docker-compose down -v --rmi all --remove-orphans
