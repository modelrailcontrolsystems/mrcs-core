# mrcs-core
Core functionality and common data structures for the Model Rail Control Systems (MRCS) environment

## RabbitMQ

[The Homebrew RabbitMQ Formula](https://www.rabbitmq.com/docs/install-homebrew)

### Operations
`
brew services restart rabbitmq
`
`
/usr/local/opt/rabbitmq/sbin/rabbitmqctl enable_feature_flag all
`

[Deleting queues in RabbitMQ](https://stackoverflow.com/questions/6742938/deleting-queues-in-rabbitmq)

`
channel.queue_delete(queue='queue-name')
`

[How can I list or discover queues on a RabbitMQ exchange using python?](https://stackoverflow.com/questions/4287941/how-can-i-list-or-discover-queues-on-a-rabbitmq-exchange-using-python)

`
def rest_queue_list ...
`


### Monitoring
`
rabbitmqctl list_queues name messages_ready messages_unacknowledged
`
