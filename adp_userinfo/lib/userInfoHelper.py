#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of adp-api-client.
# https://github.com/adplabs/adp-userinfo-python

# Copyright © 2015-2016 ADP, LLC.

# Licensed under the Apache License, Version 2.0 (the “License”);
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

# http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an “AS IS” BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
# express or implied.  See the License for the specific language
# governing permissions and limitations under the License.

from adp_connection.lib.adpapiconnection import *
from userinfoexceptions import *
from userinfourlmap import *
from adp_userinfo import __version__


class UserInfoHelper(object):
    """ Helper class for the user_info API Product

    Attributes:
    connObj: instance of ADPAPIConnection - could be either ClientCredentialsConnection
    or AuthorizationCodeConnection """

    def __init__(self, connObj):
        """ Initializes the UserInfoHelper instance with the connection
        and the api url map """
        self.adpapiconnection = connObj
        self.userInfoMap = userInfoURLMap()
        self.userAgent = 'adp-userinfo-python/' + __version__

    def callAPI(self, apiuri):
        """ ADP API requester that makes the actual api calls and returns the
        responses

        Attibutes:
        apiri: the actual API uri to be called
        Returns: response from the api GET request """
        connectionConfiguration = self.adpapiconnection.getConfig()
        headers = {'Authorization': 'Bearer ' + self.adpapiconnection.getAccessToken(), 'user-agent': self.userAgent}
        r = requests.get(connectionConfiguration.getApiRequestURL() + apiuri,
                         cert=(connectionConfiguration.getSSLCertPath(),
                               connectionConfiguration.getSSLKeyPath()),
                         headers=headers)
        logging.debug(r.status_code)
        logging.debug(r.json())
        return r

    def getUserInfo(self):
        """ Helper method to get the user_info by calling the proper
        ADP API.

        Returns: UserInfo JSON object upon a successful response
        An unsuccessful response raises the APICallError containing the
        status code and message returned by the api call """
        apiuri = self.userInfoMap.getURIfromMap('getUserInfo')
        r = self.callAPI(apiuri)
        if r.status_code == requests.codes.ok:
            return r.json()
        else:
            raise APICallError(self.__class__.__name__, str(r.status_code), r.text)
