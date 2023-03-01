#!/usr/bin/env bash

curl -X 'PUT' \
  'http://localhost:3009/event' \
  -H 'accept: */*' \
  -H 'Content-Type: application/json' \
  -d '{
	"event/application": {
		"application/user-roles": {
			"http://cilogon.org/serverE/users/26179": [
				"handler"
			],
			"expirer-bot": [
				"expirer"
			],
			"rejecter-bot": [
				"handler"
			],
			"http://cilogon.org/serverE/users/26416": [
				"applicant"
			],
			"approver-bot": [
				"handler"
			],
			"http://cilogon.org/serverE/users/4497": [
				"reporter"
			],
			"http://cilogon.org/serverE/users/26178": [
				"handler"
			]
		},
		"application/workflow": {
			"workflow/type": "workflow/default",
			"workflow/id": 25,
			"workflow.dynamic/handlers": [
				{
					"email": "alerts@example.com",
					"userid": "approver-bot",
					"name": "Approver Bot",
					"handler/active?": true
				},
				{
					"email": "handler@example.com",
					"userid": "http://cilogon.org/serverE/users/26178",
					"name": "Steele Cooke"
				},
				{
					"email": "admin@example.com",
					"userid": "http://cilogon.org/serverE/users/26179",
					"name": "Alex Ip",
					"handler/active?": true
				},
				{
					"email": "alerts@example.com",
					"userid": "rejecter-bot",
					"name": "Rejecter Bot"
				}
			]
		},
		"application/external-id": "2023/127",
		"application/first-submitted": "2023-03-01T06:16:30.595Z",
		"application/blacklist": [
			{
				"blacklist/resource": {
					"resource/ext-id": "https://dev-binderhub.atap-binder.cloud.edu.au/"
				},
				"blacklist/user": {
					"email": "user@example.com",
					"userid": "http://cilogon.org/serverE/users/26416",
					"name": "Alex Ip"
				}
			}
		],
		"application/id": 162,
		"application/applicant": {
			"email": "user@example.com",
			"userid": "http://cilogon.org/serverE/users/26416",
			"name": "Alex Ip"
		},
		"application/copied-from": {
			"application/external-id": "2023/126",
			"application/id": 161
		},
		"application/todo": null,
		"application/members": [],
		"application/resources": [
			{
				"catalogue-item/end": null,
				"catalogue-item/expired": false,
				"catalogue-item/enabled": true,
				"resource/id": 25,
				"catalogue-item/title": {
					"en": "ATAP Development BinderHub on NeCTAR"
				},
				"catalogue-item/infourl": {},
				"resource/ext-id": "https://dev-binderhub.atap-binder.cloud.edu.au/",
				"catalogue-item/start": "2023-02-16T02:52:18.575Z",
				"catalogue-item/archived": false,
				"catalogue-item/id": 30
			}
		],
		"application/accepted-licenses": {
			"http://cilogon.org/serverE/users/26416": [
				23
			]
		},
		"application/forms": [
			{
				"form/internal-name": "Application for access to ATAP BinderHub hosted on NeCTAR",
				"form/fields": [
					{
						"field/private": false,
						"field/info-text": {
							"en": "The full name of the applicant - some identity providers do not provide this detail"
						},
						"field/title": {
							"en": "Full Name of Applicant"
						},
						"field/max-length": null,
						"field/visible": true,
						"field/type": "text",
						"field/value": "Alex Ip (user@example.com)",
						"field/previous-value": "Alex Ip (user@example.com)",
						"field/id": "fld1",
						"field/optional": false,
						"field/placeholder": {
							"en": "Dr Jane Doe"
						}
					},
					{
						"field/private": false,
						"field/info-text": {
							"en": "The name of the research or educational institution with which the applicant is affiliated - some identity providers do not provide this detail"
						},
						"field/title": {
							"en": "Institutional Affiliation"
						},
						"field/max-length": null,
						"field/visible": true,
						"field/type": "text",
						"field/value": "AARNet",
						"field/previous-value": "AARNet",
						"field/id": "fld2",
						"field/optional": false,
						"field/placeholder": {
							"en": "University of Somewhere"
						}
					},
					{
						"field/private": false,
						"field/info-text": {
							"en": "The applicant'"'"'s field of research or study - this is to help ATAP serve users'"'"' needs better into the future"
						},
						"field/title": {
							"en": "Field of Research or Study"
						},
						"field/max-length": null,
						"field/visible": true,
						"field/type": "text",
						"field/value": "eResearch Infrastructure",
						"field/previous-value": "eResearch Infrastructure",
						"field/id": "fld3",
						"field/optional": false,
						"field/placeholder": {
							"en": "Linguistics"
						}
					}
				],
				"form/title": "Application for access to ATAP BinderHub hosted on NeCTAR",
				"form/id": 10,
				"form/external-title": {
					"en": "Application for access to ATAP BinderHub hosted on NeCTAR"
				}
			}
		],
		"application/invited-members": [],
		"application/description": "",
		"application/generated-external-id": "2023/127",
		"application/last-activity": "2023-03-01T06:22:17.055Z",
		"application/events": [
			{
				"application/external-id": "2023/127",
				"event/actor-attributes": {
					"email": "user@example.com",
					"userid": "http://cilogon.org/serverE/users/26416",
					"name": "Alex Ip"
				},
				"application/id": 162,
				"event/time": "2023-03-01T06:16:26.669Z",
				"workflow/type": "workflow/default",
				"application/resources": [
					{
						"resource/ext-id": "https://dev-binderhub.atap-binder.cloud.edu.au/",
						"catalogue-item/id": 30
					}
				],
				"application/forms": [
					{
						"form/id": 10
					}
				],
				"workflow/id": 25,
				"event/actor": "http://cilogon.org/serverE/users/26416",
				"event/type": "application.event/created",
				"event/id": 652,
				"application/licenses": [
					{
						"license/id": 23
					}
				]
			},
			{
				"event/actor-attributes": {
					"email": "user@example.com",
					"userid": "http://cilogon.org/serverE/users/26416",
					"name": "Alex Ip"
				},
				"application/id": 162,
				"event/time": "2023-03-01T06:16:26.669Z",
				"application/field-values": [
					{
						"value": "Alex Ip (user@example.com)",
						"field": "fld1",
						"form": 10
					},
					{
						"value": "AARNet",
						"field": "fld2",
						"form": 10
					},
					{
						"value": "eResearch Infrastructure",
						"field": "fld3",
						"form": 10
					}
				],
				"event/actor": "http://cilogon.org/serverE/users/26416",
				"event/type": "application.event/draft-saved",
				"event/id": 653
			},
			{
				"event/actor-attributes": {
					"email": "user@example.com",
					"userid": "http://cilogon.org/serverE/users/26416",
					"name": "Alex Ip"
				},
				"application/id": 162,
				"event/time": "2023-03-01T06:16:26.669Z",
				"application/copied-from": {
					"application/external-id": "2023/126",
					"application/id": 161
				},
				"event/actor": "http://cilogon.org/serverE/users/26416",
				"event/type": "application.event/copied-from",
				"event/id": 654
			},
			{
				"event/actor-attributes": {
					"email": "user@example.com",
					"userid": "http://cilogon.org/serverE/users/26416",
					"name": "Alex Ip"
				},
				"application/id": 162,
				"event/time": "2023-03-01T06:16:28.223Z",
				"application/accepted-licenses": [
					23
				],
				"event/actor": "http://cilogon.org/serverE/users/26416",
				"event/type": "application.event/licenses-accepted",
				"event/id": 656
			},
			{
				"event/actor-attributes": {
					"email": "user@example.com",
					"userid": "http://cilogon.org/serverE/users/26416",
					"name": "Alex Ip"
				},
				"application/id": 162,
				"event/time": "2023-03-01T06:16:30.438Z",
				"application/field-values": [
					{
						"value": "Alex Ip (user@example.com)",
						"field": "fld1",
						"form": 10
					},
					{
						"value": "AARNet",
						"field": "fld2",
						"form": 10
					},
					{
						"value": "eResearch Infrastructure",
						"field": "fld3",
						"form": 10
					}
				],
				"event/actor": "http://cilogon.org/serverE/users/26416",
				"event/type": "application.event/draft-saved",
				"event/id": 657,
				"application/duo-codes": []
			},
			{
				"event/actor-attributes": {
					"email": "user@example.com",
					"userid": "http://cilogon.org/serverE/users/26416",
					"name": "Alex Ip"
				},
				"application/id": 162,
				"event/time": "2023-03-01T06:16:30.595Z",
				"event/actor": "http://cilogon.org/serverE/users/26416",
				"event/type": "application.event/submitted",
				"event/id": 658
			},
			{
				"event/actor-attributes": {
					"email": "alerts@example.com",
					"userid": "approver-bot",
					"name": "Approver Bot"
				},
				"application/id": 162,
				"event/time": "2023-03-01T06:16:30.628Z",
				"application/comment": "",
				"event/actor": "approver-bot",
				"event/type": "application.event/approved",
				"event/id": 659
			},
			{
				"event/actor-attributes": {
					"email": "user@example.com",
					"userid": "http://cilogon.org/serverE/users/26416",
					"name": "Alex Ip"
				},
				"application/id": 162,
				"event/time": "2023-03-01T06:16:32.053Z",
				"event/actor": "http://cilogon.org/serverE/users/26416",
				"event/type": "application.event/copied-to",
				"event/id": 663,
				"application/copied-to": {
					"application/external-id": "2023/128",
					"application/id": 163
				}
			},
			{
				"event/actor-attributes": {
					"email": "admin@example.com",
					"userid": "http://cilogon.org/serverE/users/26179",
					"name": "Alex Ip"
				},
				"application/id": 162,
				"event/time": "2023-03-01T06:22:17.055Z",
				"application/comment": "Hopefully this triggers a application.event/revoked event",
				"event/actor": "http://cilogon.org/serverE/users/26179",
				"event/type": "application.event/revoked",
				"event/attachments": [],
				"event/id": 673
			}
		],
		"application/attachments": [],
		"application/licenses": [
			{
				"license/type": "link",
				"license/title": {
					"en": "ATAP BinderHub on NeCTAR - Terms of Use"
				},
				"license/link": {
					"en": "https://cloudstor.aarnet.edu.au/plus/s/KUSoqQ5hohgTvxG"
				},
				"license/id": 23,
				"license/enabled": true,
				"license/archived": false
			}
		],
		"application/created": "2023-03-01T06:16:26.669Z",
		"application/role-permissions": {
			"past-reviewer": [
				"see-everything"
			],
			"decider": [
				"see-everything"
			],
			"everyone-else": [],
			"expirer": [
				"application.command/send-expiration-notifications",
				"application.command/delete"
			],
			"member": [
				"application.command/copy-as-new"
			],
			"reporter": [
				"see-everything"
			],
			"past-decider": [
				"see-everything"
			],
			"applicant": [
				"application.command/copy-as-new"
			],
			"reviewer": [
				"see-everything"
			],
			"handler": [
				"see-everything",
				"application.command/remark"
			]
		},
		"application/state": "application.state/revoked",
		"application/copied-to": [
			{
				"application/external-id": "2023/128",
				"application/id": 163
			}
		],
		"application/modified": "2023-03-01T06:16:30.438Z"
	},
	"application/id": 162,
	"event/time": "2023-03-01T06:22:17.055Z",
	"application/comment": "Hopefully this triggers a application.event/revoked event",
	"event/actor": "http://cilogon.org/serverE/users/26179",
	"event/type": "application.event/revoked",
	"event/attachments": [],
	"event/id": 673
}'