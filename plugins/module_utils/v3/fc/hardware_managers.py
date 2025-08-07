from __future__ import absolute_import, division, print_function

from copy import deepcopy

from .fc import FoundationCentral

__metaclass__ = type


class HardwareManager(FoundationCentral):
    entity_type = "hardware_managers"

    def __init__(self, module):
        resource_type = "/hardware_managers"
        super(HardwareManager, self).__init__(module, resource_type=resource_type)
        self.build_spec_methods = {}

    def _get_default_spec(self):
        return deepcopy({})
