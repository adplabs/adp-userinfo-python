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


class userInfoURLMap(object):
    """ This class provides the access to the mapping between the high-level
    method calls and the corresponding ADP API calls for the userinfo product """

    urlMap = dict({})

    def __init__(self):
        self.urlMap['getUserInfo'] = '/core/v1/userinfo'

    def getURIfromMap(self, methodname):
            urival = self.urlMap[methodname]
            return urival
