# REMS Event Handler

A simple HTTP server listening REMS event notifications.
On notification, it attempts to handle the event.

## Specific Event Handlers
### Auto Entitlement Revoker

On `application.event/revoked` notification, it tries to revoke any applications associated with the new blacklist entry.

## Installation

See [config.ini](config.ini) for an example of a configuration file that must be supplied. 

Add this in your REMS `config.edn`:
```
:event-notification-targets [{:url "http://127.0.0.1:3009/event"
                              :event-types [:application.event/revoked]}]
```

## Running locally
You can test your installation locally. Pick some `<BUILD_NAME>` and `<CONTAINER_NAME>` and run:
```
cd rems/resources/addons/rems_event_handler
docker build -t <BUILD_NAME> .
docker run --rm --network="host" --name <CONTAINER_NAME> <BUILD_NAME>
```
Invoke the `application.event/revoked` event in REMS and check that the auto_entitlement_revoker log looks ok. The actual request to 
REMS might fail from your local environment depending your configuration. 
