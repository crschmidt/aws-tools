#!/usr/bin/python

import boto.ec2
import sys

def connect():
    r = boto.ec2.connect_to_region("us-east-1")
    return r

def autoscale_activities(group_name):
    """Reports the autoscaling activities, given a group."""
    scale = boto.connect_autoscale()
    act = scale.get_all_activities(group_name)
    for i in act:
        print i.cause
        print "    ", i.description
autoscale_activities.activity = True

def list():
    """List active instances"""
    r = connect()
    for reservation in r.get_all_instances():
        for instance in reservation.instances:
            print instance.id, instance.state, instance.ip_address, instance.key_name, instance.launch_time, "\n    ", instance.dns_name
            tags = []
            for k,v in instance.tags.items():
                tags.append(k+":"+v)
            if tags:
                print "    ", ", ".join(tags)
list.activity = True

def console(instance_id):
    r = connect()
    i = r.get_all_instances(instance_id)[0].instances[0]
    print i.get_console_output().output
console.activity = True

def terminate(instance_id):
    """Terminate an instance, given an instance id"""
    r = connect()
    i = r.get_all_instances(instance_id)[0]
    return i.instances[0].terminate()
terminate.activity = True

def help():
    for g in globals():
        if hasattr(globals()[g], 'activity'):
            print g, '-', globals()[g].__doc__
if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        args = ['list']
    ret = globals()[args[0]](*args[1:])
    if ret != None: 
        print ret
