#!/usr/bin/python

import boto.ec2
import sys

def connect():
    r = boto.ec2.connect_to_region("us-east-1")
    return r

def create(size, snapshot_id=None, zone="us-east-1b"):
    "Create a volume with a size (given in GB) and an optional snapshot_id"
    r = connect()
    return r.create_volume(int(size), zone, snapshot_id)
create.activity = True    

def snapshots():
    "List self-owned snapshots"
    r = connect()
    for snap in r.get_all_snapshots(owner='self'):
        display = [snap.id]
        if snap.description:
            display.append(snap.description)
        if snap.tags:
            for k, v  in snap.tags.items():
                display.append("%s: %s" % (k, v))
        display.append("%s (%s)" % (snap.status, snap.progress))
        print " ".join(display)
snapshots.activity = True    

def snapshot(volume_id, description):
    "Snapshot a given volume ID, with a description"
    r = connect()
    return r.create_snapshot(volume_id, description)
snapshot.activity = True

def delete_unused():
    """Delete any currently unattached volumes not coming from a snapshot"""
    r = connect()
    for volume in r.get_all_volumes():
        if volume.attachment_state() == None:
            if not volume.snapshot_id:
                print "Deleting %s" % volume.id
                delete(volume.id)
            else:
                print "Cowardly refusing to delete volume with snapshot (%s, %s)" % (volume.id, volume.snapshot_id)
delete_unused.activity = True

def delete(volume_id):
    """Delete a volume, given an instance id"""
    r = connect()
    return r.delete_volume(volume_id)
delete.activity = True

def list():
    """List active volumes"""
    r = connect()
    for volume in r.get_all_volumes():
        print volume.id, volume.attachment_state(), volume.snapshot_id
list.activity = True

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
