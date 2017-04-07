#!/usr/bin/python
import boto3
import sys

def get_instance_ip(instance_id):
    client = boto3.client('ec2')
    response = client.describe_instances(InstanceIds = [instance_id])
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            for interface in instance['NetworkInterfaces']:
                if 'PrivateIpAddress' in interface:
                   yield interface['PrivateIpAddress']
                if 'Association' in interface:
                   yield interface['Association']['PublicIp']

def as_get_instances(client, asgroup):

    irsp = client.describe_auto_scaling_instances()

    for i in irsp['AutoScalingInstances']:
        if i['AutoScalingGroupName'] == asgroup:
            yield i['InstanceId']

if __name__ == '__main__':
    client = boto3.client('autoscaling', region_name='ca-central-1')
    id_list = list(as_get_instances(client, sys.argv[1]))
    print (id_list)
    for id in id_list:
        print(list(get_instance_ip(id)))
