#!/usr/bin/python
import boto
import boto.ec2
import boto.ec2.elb
import sys

def connect():
    elb = boto.ec2.elb.connect_to_region("us-east-1")
    return elb

def add_instance(lbname, instance_id):
    elb = connect()
    return elb.register_instances(lbname, [instance_id])

def remove_instance(lbname, instance_id):
    elb = connect()
    return elb.deregister_instances(lbname, [instance_id])
    

def delete(lbname):
    elb = connect()
    lb = elb.get_all_load_balancers(load_balancer_names=[lbname])[0]
    return lb.delete()

def list():
    elb = connect()
    lbs = elb.get_all_load_balancers()
    for lb in lbs:
        print lb.name, lb.dns_name
        print "  ", ", ".join([str(x) for x in lb.instances])
list.activity = True

def help():
    for g in globals():
        if hasattr(globals()[g], 'activity'):
            print g, '-', globals()[g].__doc__

if __name__ == "__main__":
    if __name__ == "__main__":
        args = sys.argv[1:]
        if not args:
            args = ['list']
        ret = globals()[args[0]](*args[1:])
        if ret != None: 
            print ret

