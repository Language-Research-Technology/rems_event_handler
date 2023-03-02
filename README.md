# REMS Event Handler

A simple HTTP server listening REMS event notifications.
On notification, it attempts to handle the event.

## Pre-requirements for REMS
You will need to create the `event-handler-user` user (create using API/swagger). This must match the user you configure
in the `rems_admin_userid` value in the `config.ini` file. This is important to prevent unwanted recursion in the 
`application.event/revoked` event when the script revokes approved applications.

## Specific Event Handlers
- On `application.event/created` notification, it tries to delete the current draft application if an open application 
already exists with the same user_id and resource_id.
- On `application.event/submitted` notification, it tries to reject or revoke the current submitted application if an open 
application already exists with the same user_id and resource_id.
- On `application.event/revoked` notification, it tries to revoke any approved applications with the same user_id and 
resource_id.

## Installation

See [config.ini](config.ini) for an example of a configuration file that must be supplied. 

Add this in your REMS `config.edn`:
```
:event-notification-targets [
    {:url "http://127.0.0.1:3009/event"
     :event-types [:application.event/created]}
    {:url "http://127.0.0.1:3009/event"
     :event-types [:application.event/submitted]}
    {:url "http://127.0.0.1:3009/event"
     :event-types [:application.event/revoked]}
    ]
```
Note that the application.event/created event handler deletes draft events, so it may cause undesirable UI effects while
the user is looking at the application page for a deleted draft application.

## Running locally
You can test your installation locally. Pick some `<BUILD_NAME>` and `<CONTAINER_NAME>` and run:
```
docker build -t <BUILD_NAME> .
docker run --rm --network="host" --name <CONTAINER_NAME> <BUILD_NAME>
```
Invoke the desired event in REMS and check that the rems_event_handler log looks ok. The actual request to 
REMS might fail from your local environment depending your configuration. 
