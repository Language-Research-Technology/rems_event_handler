#!/usr/bin/env python3

# A simple HTTP server listening for REMS event notifications.
# On 'application.event/revoked' notification it tries to revoke any existing entitlements for that user & resource.

# A configuration file 'config.ini' must be supplied.

# Usage: ./auto_entitlement_revoker.py
#        Stop with Ctrl-C

import configparser
import http.server
import json
import logging

import requests

logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.DEBUG)
log = logging.getLogger(__name__)

parser = configparser.ConfigParser()
try:
    parser.read('config.ini')
    config = parser['default']
    url = config.get('url')
    port = config.getint('port')
    rems_url = config.get('rems_url')
    rems_admin_userid = config.get('rems_admin_userid')
    rems_admin_api_key = config.get('rems_admin_api_key')
except KeyError as e:
    log.error(f'Configuration error: missing key {e}')
    exit(1)


def get_entitlement_application_ids(user_id, resource_id, event_id):
    """Return list of application IDs for entitlements associated with user_id and resource_id"""
    entitlements_url = f'{rems_url}/api/entitlements'
    params = {
        'user': user_id,
        'resource': resource_id,
        'expired': 'false'
    }
    headers = {
        'accept': 'application/json',
        'x-rems-api-key': rems_admin_api_key,
        'x-rems-user-id': rems_admin_userid,
    }
    log.info(f'{event_id} Retrieving entitlements for user ID {user_id} and resource ID {resource_id}')
    log.debug(f'{event_id} entitlements_url: {entitlements_url}, params: {params}, headers={headers}')
    response = requests.get(
        url=entitlements_url,
        params=params,
        headers=headers,
    )
    log.info(f'{event_id} Response: {response.status_code} {response.reason}')
    log.debug(f'{event_id} response.text: {response.text}')
    if response.status_code != 200:
        raise Exception(f'Response code {response.status_code} received when retrieving entitlements')

    applications = [entitlement['application-id'] for entitlement in response.json()]
    log.debug(f'{event_id} applications: {applications}')
    return applications


def revoke_entitlements(user_id, resource_id, event_id):
    """
    Revoke applications for active entitlements for specified user_id and resource_id
    Will report errors and continue processing
    """
    application_ids = get_entitlement_application_ids(user_id, resource_id, event_id)
    revoked_count = 0
    for application_id in application_ids:
        try:
            log.info(f'{event_id} Revoking application {application_id}')
            process_application('revoke',
                                application_id,
                                "Application revoked by auto-revoker after identical application revoked",
                                event_id
                                )
            log.info(f'{event_id} Revoked application {application_id}')
            revoked_count += 1
        except Exception as e:
            log.warning(f'{event_id} Failure revoking application_id {application_id}: {e}')
    return revoked_count


def application_revoked_event_handler(data, event_id):
    """Handle application.event/revoked event - added to REMSEventHandler.EVENT_HANDLERS"""

    # Prevent unwanted recursion
    if data["event/actor"] == rems_admin_userid:
        log.info(
            f'{event_id} Not handling application.event/revoked event triggered by user {rems_admin_userid}')
        return

    # Pull required information from data structure in request body
    user_id = data['event/application']['application/applicant']['userid']
    resource_id = data['event/application']['application/resources'][0]['resource/ext-id']
    log.info(f'{event_id} Revoking entitlements for user id: {user_id}, resource_id: {resource_id}')

    revoked_count = revoke_entitlements(user_id, resource_id, event_id)
    log.info(
        f'{event_id} Revoked {revoked_count} entitlements for user id: {user_id}, resource_id: {resource_id}')


def get_open_applications(user_id, resource_id, application_id, event_id):
    """
    Return list of application IDs for open applications associated with user_id and resource_id
    "Open" is defined as state:approved OR state:applied OR state:returned OR state:draft
    We need to filter out the current application by ID, so we do that in the query
    """
    applications_url = f'{rems_url}/api/applications'
    params = {
        'query': f'resource:"{resource_id}" AND applicant:"{user_id}" '
                 'AND (state:approved OR state:applied OR state:returned OR state:draft) '
                 f'AND NOT id:{application_id}'
    }
    headers = {
        'accept': 'application/json',
        'x-rems-api-key': rems_admin_api_key,
        'x-rems-user-id': rems_admin_userid,
    }
    log.info(f'{event_id} Retrieving open applications for user ID {user_id} and resource ID {resource_id}')
    log.debug(f'{event_id} applications_url: {applications_url}, params: {params}, headers={headers}')
    response = requests.get(
        url=applications_url,
        params=params,
        headers=headers,
    )
    log.info(f'{event_id} Response: {response.status_code} {response.reason}')
    log.debug(f'{event_id} response.text: {response.text}')
    if response.status_code != 200:
        raise Exception(f'Response code {response.status_code} received when retrieving open applications')

    # Filter out current application
    open_applications = [application['application/id'] for application in response.json()]
    log.debug(f'{event_id} open_applications: {open_applications}')
    return open_applications


def process_application(operation, application_id, comment, event_id):
    """Process application specified by application_id"""
    assert operation in ['reject', 'revoke'], f'Invalid application operation "{operation}"'
    operation_url = f'{rems_url}/api/applications/{operation}'
    headers = {
        'accept': 'application/json',
        'x-rems-api-key': rems_admin_api_key,
        'x-rems-user-id': rems_admin_userid,
        'Content-Type': 'application/json',
    }
    data = json.dumps(
        {
            "application-id": application_id,
            "comment": comment,
            "attachments": [],
        }
    )

    log.debug(f'{event_id} operation_url: {operation_url}, headers={headers}, data={data}')
    response = requests.post(
        url=operation_url,
        headers=headers,
        data=data,
    )
    log.debug(f'{event_id} response.text: {response.text}')

    if response.status_code != 200:
        raise Exception(f'Response code {response.status_code} received. Reason: {response.reason}')

    if not response.json().get("success"):
        raise Exception(f'{event_id} Application {operation} failed. Errors: {response.json().get("errors") or ""}')


def delete_draft_application(application_id, user_id, event_id):
    """Delete draft application specified by application_id"""
    operation_url = f'{rems_url}/api/applications/delete'
    headers = {
        'accept': 'application/json',
        'x-rems-api-key': rems_admin_api_key,
        'x-rems-user-id': user_id,  # Must impersonate draft application owner
        'Content-Type': 'application/json',
    }
    data = json.dumps(
        {
            "application-id": application_id,
        }
    )

    log.debug(f'{event_id} operation_url: {operation_url}, headers={headers}, data={data}')
    response = requests.post(
        url=operation_url,
        headers=headers,
        data=data,
    )
    log.debug(f'{event_id} response.text: {response.text}')

    if response.status_code != 200:
        raise Exception(f'Response code {response.status_code} received. Reason: {response.reason}')

    if not response.json().get("success"):
        raise Exception(f'{event_id} Application delete failed. Errors: {response.json().get("errors") or ""}')


def handle_duplicate_application(application_id, user_id, resource_id, event_id):
    """
    Reject applications for new applications for specified user_id and resource_id if open applications exist
    Will report errors and continue processing
    """
    if get_open_applications(user_id, resource_id, application_id, event_id):
        # Manually approved stuff needs to be rejected, auto-approved stuff revoked after bot accepts it
        for application_operation in ['reject', 'revoke']:
            try:
                log.info(f'{event_id} Attempting to {application_operation} application {application_id}')
                process_application(application_operation,
                                    application_id,
                                    "Application rejected by auto-rejecter after existing open applications found",
                                    event_id
                                    )
                log.info(f'{event_id} {application_operation} application successful {application_id}')
                break
            except Exception as e:
                log.warning(f'{event_id} Failure to {application_operation} application_id {application_id}: {e}')
    else:
        log.info(f'{event_id} Aapplication {application_id} has no open duplicates')


def application_submitted_event_handler(data, event_id):
    """Handle application.event/submitted event - added to REMSEventHandler.EVENT_HANDLERS"""

    user_id = data['event/application']['application/applicant']['userid']
    resource_id = data['event/application']['application/resources'][0]['resource/ext-id']
    application_id = data['event/application']['application/id']
    log.info(
        f'{event_id} Checking existing applications for user id: {user_id}, resource_id: {resource_id}, application_id: {application_id}')

    handle_duplicate_application(application_id, user_id, resource_id, event_id)


def application_created_event_handler(data, event_id):
    """Handle application.event/created event - added to REMSEventHandler.EVENT_HANDLERS"""

    user_id = data['event/application']['application/applicant']['userid']
    resource_id = data['event/application']['application/resources'][0]['resource/ext-id']
    application_id = data['event/application']['application/id']
    log.info(
        f'{event_id} Checking existing applications for user id: {user_id}, resource_id: {resource_id}, application_id: {application_id}')

    delete_draft_application(application_id, user_id, event_id)


class REMSEventHandler(http.server.BaseHTTPRequestHandler):
    # Specify handled events and their handler functions here
    EVENT_HANDLERS = {
        # 'application.event/applicant-changed': None,
        # 'application.event/approved': None,
        # 'application.event/closed': None,
        # 'application.event/copied-from': None,
        # 'application.event/copied-to': None,
        'application.event/created': application_created_event_handler,
        # 'application.event/decided': None,
        # 'application.event/decider-invited': None,
        # 'application.event/decider-joined': None,
        # 'application.event/decision-requested': None,
        # 'application.event/deleted': None,
        # 'application.event/draft-saved': None,
        # 'application.event/expiration-notifications-sent': None,
        # 'application.event/external-id-assigned': None,
        # 'application.event/licenses-accepted': None,
        # 'application.event/licenses-added': None,
        # 'application.event/member-added': None,
        # 'application.event/member-invited': None,
        # 'application.event/member-joined': None,
        # 'application.event/member-removed': None,
        # 'application.event/member-uninvited': None,
        # 'application.event/rejected': None,
        # 'application.event/remarked': None,
        # 'application.event/resources-changed': None,
        # 'application.event/returned': None,
        # 'application.event/review-requested': None,
        # 'application.event/reviewed': None,
        # 'application.event/reviewer-invited': None,
        # 'application.event/reviewer-joined': None,
        'application.event/revoked': application_revoked_event_handler,
        'application.event/submitted': application_submitted_event_handler,
    }

    def do_PUT(self):
        """Handle PUT request to /event path for specific events defined in REMSEventHandler.EVENT_HANDLERS"""
        log.debug(f'Received PUT request at {self.path}, headers: {self.headers}')
        length = int(self.headers['content-length'])
        payload = self.rfile.read(length).decode("utf-8")

        try:
            data = json.loads(payload)
        except Exception as e:
            msg = f'Unable to parse JSON payload! {type(e).__name__}: {e}'
            log.error(msg)
            log.debug(f'payload: {payload}')
            self.send_response(400, message=msg)
            self.end_headers()
            return

        try:
            event_id = f'event/id:{data["event/id"]}'
        except KeyError:
            msg = f'KeyError: Missing or invalid event_id!'
            log.error(msg)
            log.debug(f'payload: {payload}')
            self.send_response(400, message=msg)
            self.end_headers()
            return

        log.debug(f'{event_id} data: {data}')

        if self.path != '/event':
            msg = f'{event_id} Invalid path "{self.path}"!'
            log.error(msg)
            self.send_response(404, message=msg)
            self.end_headers()
            return

        event_type = data.get('event/type') or '<UNDEFINED>'
        try:
            event_handler = REMSEventHandler.EVENT_HANDLERS.get(event_type)
            if event_handler:
                log.info(f'{event_id} Received valid event notification: {event_type}')
                event_handler(data, event_id)
                self.send_response(200, message='OK')
            else:
                msg = f'{event_id} Received illegal event type: {event_type}. ' \
                      f'Expected one of {list(REMSEventHandler.EVENT_HANDLERS.keys())}'
                log.error(msg)
                self.send_response(400, message=msg)

        except Exception as e:  # Generic exception handling for event handling
            msg = f'{event_id} Error handling event event_type: {type(e).__name__}: {e}'
            log.error(msg)
            self.send_response(500, message=msg)

        self.end_headers()
        return


if __name__ == "__main__":
    handler_class = REMSEventHandler
    http_server = http.server.HTTPServer((url, port), handler_class)
    with http_server:
        try:
            log.info(f'Event listener at \'{url}:{port}\'. Stop with [Ctrl-C].')
            http_server.serve_forever()
        except KeyboardInterrupt:
            log.info('Event listener stopped')
