#!/usr/bin/python

import boto.ec2

r = boto.ec2.connect_to_region("us-east-1")
for reservation in r.get_all_instances():
    for instance in reservation.instances:
        print instance.id, instance.state, instance.ip_address, instance.key_name, instance.launch_time
