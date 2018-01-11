## Broker settings. Local config
# broker_url = 'amqp://qlf:1234@localhost:5672/qlfbroker'

# Redis
broker_url = 'redis://redis:6379/0'
result_backend = 'redis://redis:6379/0'
broker_transport_options = {'fanout_prefix': True, 'fanout_patterns': True, 'visibility_timeout': 3600}

# List of modules to import when the Celery worker starts.
imports = ('tasks',)

## Using AMQP
# result_backend = 'amqp://'
