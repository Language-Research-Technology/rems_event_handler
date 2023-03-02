# REMS Event Handler

A simple HTTP server listening for REMS event notifications. On notification, it attempts to handle the event.

Events which could be handled are as follows:

- `application.event/applicant-changed`
- `application.event/approved`
- `application.event/closed`
- `application.event/copied-from`
- `application.event/copied-to`
- `application.event/created`
- `application.event/decided`
- `application.event/decider-invited`
- `application.event/decider-joined`
- `application.event/decision-requested`
- `application.event/deleted`
- `application.event/draft-saved`
- `application.event/expiration-notifications-sent`
- `application.event/external-id-assigned`
- `application.event/licenses-accepted`
- `application.event/licenses-added`
- `application.event/member-added`
- `application.event/member-invited`
- `application.event/member-joined`
- `application.event/member-removed`
- `application.event/member-uninvited`
- `application.event/rejected`
- `application.event/remarked`
- `application.event/resources-changed`
- `application.event/returned`
- `application.event/review-requested`
- `application.event/reviewed`
- `application.event/reviewer-invited`
- `application.event/reviewer-joined`
- `application.event/revoked`
- `application.event/submitted`

## Pre-requirements for REMS

You will need to create the `event-handler-user` user (create using API/swagger). **Note that this must match the user
you configure in the `rems_admin_userid` value in the `config.ini` file.** This is important to prevent unwanted
recursion in the `application.event/revoked` event when the script revokes approved applications.

## Specific Event Handlers

- `application.event/created` - deletes the current draft application if an open application already exists with the
  same user_id and resource_id.
- `application.event/submitted` - rejects or revokes the current submitted application if an open application already
  exists with the same user_id and resource_id.
- `application.event/revoked` - rejects or revokes any approved applications with the same user_id and resource_id.
  There is a pre-check to ensure that the event was not triggered by the `event-handler-user` user in order to prevent
  unwanted recursion which would always revoke everything.

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

Note that the `application.event/created` event handler will delete the current draft application when existing open
applications are found, so it may cause undesirable UI effects while the user is looking at the application page for a
deleted draft application.

## Running locally

You can test your installation locally. Pick some `<BUILD_NAME>` and `<CONTAINER_NAME>` and run:

```
docker build -t <BUILD_NAME> .
docker run --rm --network="host" --name <CONTAINER_NAME> <BUILD_NAME>
```

Trigger the desired event in REMS and check that the rems_event_handler log looks ok. Note that the actual request to
REMS might fail from your local environment depending your configuration. 
