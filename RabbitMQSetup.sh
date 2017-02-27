#!/usr/bin/env bash
sudo rabbitmqctl add_user Usage team15
sudo rabbitmqctl add_vhost usage_vhost
sudo rabbitmqctl set_permissions -p usage_vhost "Usage" ".*" ".*" ".*"
sudo rabbitmqctl set_permissions -p usage_vhost "guest" ".*" ".*" ".*"
sudo rabbitmqctl set_permissions -p / "Usage" ".*" ".*" ".*"
sudo rabbitmqctl set_permissions -p / "guest" ".*" ".*" ".*"
