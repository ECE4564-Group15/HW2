# How to setup RabbitMQ
The RabbitMQ configuration used in this project is simple. We have a shell script that can be run that adds the new user: `Usage` with password `team15`. It also sets up a new vhost `usage_vhost` that can be specified. Finally, it adds the proper permissions for the new user and vhost as well as the guest and default vhost.

**IMPORTANT**
One final note is that this setup requires that the consumers as defined in the `RabbitMWClient` package be connected prior to the publisher's first use. This allows the proper queues to be setup in order to allow persistant messages. This can be acheived by modifying and running the [TestConsumer.py](TestConsumer.py) script.

# How to use the RabbitMQClient package

First of all, the package includes:
  1. `MQClient` Class
  2. `Connection` Type
    - Connection SubTypes: `Consumer` and `Publisher`
    - Each SubType can hold value `Normal` or value `Debug`
  
Just use a simple import statement like so:
  ```python
  from RabbitMQClient import MQClient, Connection, Consumer, Publisher
  ```
## MQClient Class
The constructor of the MQClient class is as such:
  ```python
  MQClient(
      hostname,
      queue_name,
	  user='Usage',
      password='team15',
      vhost='/',
      connection_type=Publisher.Normal)
  ``` 
Where `hostname` is the IP address or hostname of the RabbitMQ server, `queue_name` is the name of the queue you want to interact with, `user` is the RabbitMQ username, `password` is the User's password, `vhost` is the virtual host to use, and `connection_type` is the type of client you want.
For `connection_type` you must choose one of the `Connection` SubTypes and then choose whether to use the `Normal` or `Debug` version. In general, `Normal` will suffice.

### Exceptions
The  `MQClient` constructor will raise `ValueError` exception is you pass in an invalid argument or something else happens. Be sure to handle this in your code.

### Consumer Usage
The `Consumer` connection type of MQClient can be used to listen to the specified message queue and do something on each message received.

This is done by calling the *blocking* method `MQClient#subscribe` like so:
  ```python
  test = MQClient('localhost','example','Usage','team15','usage_vhost',Consumer.Normal)
  test.subscribe(callback)
  ```
The important part to note is the use of a callback function to handle the messages. As such, you must create or have access to a method to handle the messages you receive with the signature: `func(message)` where `message` is a raw string. A simple example is:
  ```python
  def example_handler(msg):
    print("GOT: %s"%(str(msg))
  ```
Additionally, note that the `subscribe` method is *blocking* so your program cannot execute while this is running. As such, all functionality must be called from your callback function.
  
### Publisher Usage
The `Publisher` connection type is even easier to use. Once you have you MQClient object, you simple have to call the `MQClient#send_message` method like so:
  ```python
  test = MQClient('localhost','example','Usage','team15','usage_vhost',Publisher.Normal)
  test.send_message(callback)
  ```
It is important to note that this method is *non-blocking*, so once the message is sent you should see a message on the console saying your message is sent. After that, you may call `send_message` as many times as you need.

## Examples
Fully functioning examples are included in the Test\*.py files.

# Host & Monitor

For bost host and monitor, we have the similar usage as following. When we use it, we have to make sure they are same.

Usage:
    ```python
    pistatd.py [-h] -b MSGBROKER [-p P] [-c C] -k ROUTKEY
    ```
    
Example:
    ```
    pistatd.py -b 127.0.0.1 [-p usage_vhost] [-c Usage:team15] -k host_1
    ```

optional arguments:
  ```
  -h, --help    show this help message and exit
  -b MSGBROKER  This is the IP address or named address of the message broker
                to connect to
   -p P         This is the virtual host to connect to on the message broker.
                If not specified, should default to the root virtual host
                (i.e. ‘/’)
   -c C         Use the given credentials when connecting to the message
                broker. If not specified,should default to a guest login
   -k ROUTKEY   The routing key to use for filtering when subscribing to the
                pi_utilization exchange on the message broker
   
    

