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

from preggy import expect
from mock import patch
from adp_connection.lib import *
from adp_userinfo.lib import *
from tests.base import TestCase


class UserInfoTestCase(TestCase):

    def test_userInfo_for_403(self):
        config = dict({})
        config['clientID'] = '88a73992-07f2-4714-ab4b-de782acd9c4d'
        config['clientSecret'] = 'a130adb7-aa51-49ac-9d02-0d4036b63541'
        config['sslCertPath'] = 'tests_certs/cert.pem'
        config['sslKeyPath'] = 'tests_certs/cert.key'
        config['tokenServerURL'] = 'https://iat-api.adp.com/auth/oauth/v2/token'
        config['disconnectURL'] = 'https://iat-accounts.adp.com/auth/oauth/v2/logout'
        config['apiRequestURL'] = 'https://iat-api.adp.com'
        config['grantType'] = 'client_credentials'

        try:
            ClientCredentialsConfiguration = ConnectionConfiguration().init(config)
            ccConnection = ADPAPIConnectionFactory().createConnection(ClientCredentialsConfiguration)
            ccConnection.connect()
            if (ccConnection.isConnectedIndicator()):
                userInfoHelper = UserInfoHelper(ccConnection)
                userinfo = userInfoHelper.getUserInfo()
                print str(userinfo)
        except APICallError as apierr:
            expect(apierr.code).to_equal('403')

    @patch("adp_userinfo.lib.userInfoHelper.requests")
    def test_userInfo_for_success(self, mock_requests):
        # def test_userInfo_for_success(self):
        config = dict({})
        config['clientID'] = '88a73992-07f2-4714-ab4b-de782acd9c4d'
        config['clientSecret'] = 'a130adb7-aa51-49ac-9d02-0d4036b63541'
        config['sslCertPath'] = 'tests_certs/cert.pem'
        config['sslKeyPath'] = 'tests_certs/cert.key'
        config['tokenServerURL'] = 'https://iat-api.adp.com/auth/oauth/v2/token'
        config['disconnectURL'] = 'https://iat-accounts.adp.com/auth/oauth/v2/logout'
        config['apiRequestURL'] = 'https://iat-api.adp.com'
        config['grantType'] = 'client_credentials'

        try:
            ClientCredentialsConfiguration = ConnectionConfiguration().init(config)
            ccConnection = ADPAPIConnectionFactory().createConnection(ClientCredentialsConfiguration)
            ccConnection.connect()
            if (ccConnection.isConnectedIndicator()):
                ccConnection.getConfig().setGrantType('authorization_code')
                userInfoHelper = UserInfoHelper(ccConnection)
                userinfo = userInfoHelper.callAPI('/core/v1/userinfo')
                mock_requests.get.assert_called_with(config['apiRequestURL']+'/core/v1/userinfo',
                                                     cert=('tests_certs/cert.pem', 'tests_certs/cert.key'),
                                                     headers={'Authorization': 'Bearer ' + ccConnection.getAccessToken()})
                expect(userinfo).to_equal(mock_requests.get.return_value)
        except Exception as apierr:
            print 'error is ' + str(apierr)
