#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# Copyright © 2013 Julien Danjou <julien@danjou.info>
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import mock
import stubout
import unittest

from climate.inventory import nova


class ServiceTestCase(unittest.TestCase):

    @staticmethod
    def fake_hypervisors_list():
        a = mock.MagicMock()
        a.id = 1
        b = mock.MagicMock()
        b.id = 2
        return [a, b]

    @staticmethod
    def fake_hypervisors_get(h):
        return {'stuff': 'foobar',
                'cpu_info': {'arch': 'x86'}}

    def setUp(self):
        self.i = nova.NovaInventory()
        self.stubs = stubout.StubOutForTesting()
        self.stubs.Set(self.i.novaclient.hypervisors, "list",
                       self.fake_hypervisors_list)
        self.stubs.Set(self.i.novaclient.hypervisors, "get",
                       self.fake_hypervisors_get)

    def test_list_hosts(self):
        hosts = self.i.list_hosts()
        self.assertEqual(len(hosts), 2)

    def test_get_host_detail(self):
        hosts = self.i.list_hosts()
        detail = self.i.get_host_details(hosts[0])
        self.assertEqual(detail['cpu_info']['arch'], 'x86')

    def tearDown(self):
        self.stubs.UnsetAll()
        self.stubs.SmartUnsetAll()
