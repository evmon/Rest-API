from raven import Client
from django.conf import settings

# If SENTRY_DSN is empty, the client will not send messages, but
# there will be no failures too - this case is handled by raven
# client code.
sentry = Client(settings.SENTRY_DSN)
