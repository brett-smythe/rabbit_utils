import sys

import argparse

import pika

import interns_creds
import interns_settings

parser = argparse.ArgumentParser()
parser.add_argument(
    '--queue',
    dest='queue_name',
    help='Name of queue to purge'
)
args = parser.parse_args()

if args.queue_name is None:
    sys.exit('A queue must be supplied')

host_ip = interns_settings.rabbitmq_host
host_port = interns_settings.rabbitmq_port

uname = interns_creds.rabbit_uname
pwd = interns_creds.rabbit_pwd

channel = pika.BlockingConnection(
    pika.ConnectionParameters(
        host_ip,
        int(host_port),
        '/',
        credentials=pika.PlainCredentials(
            uname,
            pwd
        )
    )
).channel()


num_messages = 0

for method_frame, properties, body in channel.consume('celery'):
    channel.basic_ack(delivery_tag=method_frame.delivery_tag)
    num_messages += 1
    if (num_messages % 10) == 0:
        print '{0} messages cleared                               \r'.format(
            num_messages
        )

