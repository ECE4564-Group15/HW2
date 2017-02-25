## Author:  Steven Frederiksen
## File:    RabbitMQClient.py 
## Date:    02/22/2017
## Purpose: Class that handles connections to a rabbit MQ server with a direct exchange.
## Last modified: 02/22/2017  8:15:29 PM (EST)

import pika
import pika.exceptions as PE
from enum import Enum, unique

""" 
    Enumerated type to choose which connection will be used in the 
    MQClient Class
"""
@unique
class Connection(Enum):
    def to_string(self):
        return 'Connection'

@unique
class Consumer(Connection):
    Normal = 0
    Debug  = 1
    def to_string(self):
        return '%s.%s'%(Connection.to_string(),'Consumer',)

@unique
class Publisher(Connection):
    Normal = 0
    Debug  = 1
    def to_string(self):
        return '%s.%s'%(Connection.to_string(),'Publisher',)
"""
    
"""
class MQClient:

    def _on_exchange_declare(self):
        print('Exchange Declaration OK.')

    def _on_queue_declare(self):
        print('Queue Declaration OK.')

    def _on_queue_bind(self):
        print('Queue Bind OK.')

    def __init__(
            self,
            hostname: object,
            queue_name: object,
            user: object,
            password: object,
            vhost: object,
            connection_type: object = Publisher.Normal) -> object:
        self.hostname = hostname
        self.queue_name = queue_name
        self.user = user
        self.password = password
        self.vhost = vhost
        self.connection_type = connection_type
        self.connection = None
        #create the rest of the needed parameters
        try:
            self.credentials = pika.PlainCredentials(self.user,self.password)
            self.connection_params = pika.ConnectionParameters(
                    host=self.hostname,
                    virtual_host=self.vhost,
                    credentials=self.credentials)
            self.connection = pika.BlockingConnection(self.connection_params)
            self.channel = self.connection.channel()
        except PE.ConnectionClosed:
            print('Error!: Invalid host address: %s' % (str(self.hostname),))
            raise ValueError
        except PE.ProbableAuthenticationError:
            print('Error!: Invalid username and password.')
            raise ValueError
        except PE.ProbableAccessDeniedError:
            print('Error!: Invalid username and password.')
            raise ValueError
        except ConnectionResetError:
            print('Connection Reset By Peer')
            raise ValueError

        if isinstance(self.connection_type,Connection):
            if (self.connection_type is Publisher.Normal or
                     self.connection_type is Consumer.Normal):
                #here we connect to the 'normal' exchange
                self.exchange = 'usage'
            elif (self.connection_type is Publisher.Debug or
                     self.connection_type is Consumer.Debug):
                #use the debuging exchange
                self.exchange = 'debug'
            else:
                print("Error! Invalid Connection Type %s"%(str(self.connection_type),))
                raise ValueError
        else:
            print("Error! Invalid Connection Type %s"%(str(self.connection_type),))
            raise ValueError
        #connect
        self.queue_id = None
        try:
            self.channel.exchange_declare(
                    exchange=self.exchange,
                    exchange_type='direct',
                    durable=True)

            #now we setup the rest of the functionality
            if isinstance(self.connection_type,Consumer): #Consumer
                result = self.channel.queue_declare(
                        queue=self.queue_name,
                        durable=True)
                self.queue_id = result.method.queue
                #now to bind to routing keys
                self.channel.queue_bind(
                        exchange=self.exchange,
                        queue=self.queue_id,
                        routing_key=self.queue_name)
        except PE.ChannelClosed as e:
            print('Error connecting to exchange: %s'%(e[1]))
        #else
        #do nothing, we are done setting up

    def __del__(self):
        if (self.connection is not None and
                self.connection.is_open):
            self.connection.close()

    def send_message(self,body):
        try:
            self.channel.basic_publish(
                    exchange=self.exchange,
                    routing_key=self.queue_name,
                    body=body)
            print("Sent: '%s'" % (body,))
        except PE.ChannelClosed:
            print('Connection Closed. Try to reconnect by recreating this object.')
    
    def _on_message_factory(self,callback):
        def ret(c,m,p,body):
            callback(body)
        return ret
    
    def subscribe(self,callback):
        if isinstance(self.connection_type,Consumer): 
            try:
                self.channel.basic_consume(
                        consumer_callback=self._on_message_factory(callback),
                        queue=self.queue_id,
                        no_ack=True)
                print('Starting to Consume.')
                self.channel.start_consuming()
            except PE.DuplicateConsumerTag:
                print("Internal Rabbit Error. Could not consume.")
            except PE.ChannelClosed as e:
                print(str(e))
        else:
            print("Cannot start consuming. This is not a consumer client.")
