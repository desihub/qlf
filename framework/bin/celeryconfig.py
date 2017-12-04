## Broker settings.
broker_url = 'amqp://qlf:1234@localhost:5672/qlfbroker'

# List of modules to import when the Celery worker starts.
imports = ('tasks',)

## Using AMQP
result_backend = 'amqp://'
