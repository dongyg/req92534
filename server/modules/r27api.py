#!/usr/bin/env python
#-*- encoding: utf-8 -*-

from config import *

from . import r27db

urls_rest = (
    '',                                 'CtrlIndex',
    '/',                                'CtrlIndex',
    '/event',                           'CtrlEvent1',
    '/events',                          'CtrlEvent2',
    '/events/severity/(.+)/area/(.+)',  'CtrlFilter',
)
app_api = web.application(urls_rest, locals())

################################################################################
class CtrlIndex:
    def GET(self):
        ipaddress = get_client_ip()
        realhome = web.ctx.get('realhome', 'host')
        return "Hello %s, you are accessing %s"%(ipaddress, realhome)

################################################################################
#2. As a user, I want to save the data retrieved from the REST APIs to a database for the further process.
# API for saving the data that the client side gets from api.open511.gov.bc.ca
# ps: Should have authorization checking based on user sign in
class CtrlEvent1:
    def POST(self):
        # create: events
        # input:
        #   events - A json string of event array. Refer Open511 `event`
        web.header("Content-Type", "text/json")
        params = web.input(events='')
        events = formator.json_object(params.events, [])
        retval = 0
        if events:
            retval = r27db.insertEvents(events)
        r27db.insertApiCall(web.ctx.env['REQUEST_URI'], get_client_ip())
        return formator.json_string({"code":retval})

################################################################################
#4. As a user, I want to provide two REST API endpoints to give data access to other applications. The REST API endpoints include creating new events and getting highest severity events by Areas.
# APIs for others application
# ps: API open to other applications should have authorization checking
class CtrlEvent2:
    def POST(self):
        # create: events
        # input:
        #   events - A json string of event array. Refer Open511 `event`
        web.header("Content-Type", "text/json")
        params = web.input(events='')
        events = formator.json_object(params.events, [])
        retval = 0
        if events:
            retval = r27db.insertEvents(events)
        r27db.insertApiCall(web.ctx.env['REQUEST_URI'], get_client_ip())
        return formator.json_string({"code":retval})

class CtrlFilter:
    def GET(self, severity, areaid):
        # query: severity events by areas
        # url format: /api/events/severity/{severity}/area/{areaid}?offset=&limit=
        #   {severity}: MINOR, MODERATE, MAJOR, UNKNOWN. Refer Open511 `event.severity`
        #     {areaid}: refer Open511 ID
        # eg: /api/events/severity/MAJOR/area/drivebc.ca/1
        web.header("Content-Type", "text/json")
        params = web.input()
        r27db.insertApiCall(web.ctx.env['REQUEST_URI'], get_client_ip())
        retval = r27db.listEvents(severity, areaid, params.get('offset') or 0, params.get('limit') or 50)
        return formator.json_string(retval)
