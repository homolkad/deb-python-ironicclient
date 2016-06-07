# Copyright (c) 2016 Mirantis, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from ironicclient.tests.functional import base


class PortSanityTestIronicClient(base.FunctionalTestBase):
    """Sanity tests for testing actions with port.

    Smoke test for the Ironic CLI commands which checks basic actions with
    port command like create, show, update, delete etc.
    """

    def setUp(self):
        super(PortSanityTestIronicClient, self).setUp()
        self.node = self.create_node()
        self.port = self.create_port(self.node['uuid'])

    def test_port_create(self):
        """Test steps:

        1) create node in setUp()
        2) create port in setUp()
        3) check that port has been successfully created
        """
        port_list_uuid = self.get_uuids_from_port_list()
        self.assertIn(self.port['uuid'], port_list_uuid)

    def test_port_delete(self):
        """Test steps:

        1) create node in setUp()
        2) create port in setUp()
        3) check that port has been successfully created
        4) delete port
        5) check that port has been successfully deleted
        """
        port_list_uuid = self.get_uuids_from_port_list()
        self.assertIn(self.port['uuid'], port_list_uuid)

        self.delete_port(self.port['uuid'])

        port_list_uuid = self.get_uuids_from_port_list()
        self.assertNotIn(self.port['uuid'], port_list_uuid)

    def test_port_show(self):
        """Test steps:

        1) create node in setUp()
        2) create port in setUp()
        3) check that port-show returns the same port UUID as port-create
        """
        port_show = self.show_port(self.port['uuid'])
        self.assertEqual(self.port['uuid'], port_show['uuid'])

    def test_port_update(self):
        """Test steps:

        1) create node in setUp()
        2) create port in setUp()
        3) create node to replace
        4) update port replacing node
        5) check that port has been successfully updated
        """
        node_to_replace = self.create_node()
        updated_port = self.update_port(self.port['uuid'],
                                        'replace',
                                        'node_uuid={0}'
                                        .format(node_to_replace['uuid']))

        self.assertEqual(node_to_replace['uuid'], updated_port['node_uuid'])
        self.assertNotEqual(self.port['node_uuid'], updated_port['node_uuid'])
