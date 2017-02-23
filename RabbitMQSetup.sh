#!/usr/bin/env bash
rabbitmqctl add_user Usage team15
rabbitmqctl add_vhost usage_vhost
rabbutmqctl set_permissions -p usage_vhost "Usage" ".*" ".*" ".*"
