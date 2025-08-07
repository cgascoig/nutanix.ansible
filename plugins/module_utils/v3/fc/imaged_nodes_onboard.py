from __future__ import absolute_import, division, print_function

from copy import deepcopy

from .fc import FoundationCentral
from .hardware_managers import HardwareManager

__metaclass__ = type


class ImagedNodeOnboard(FoundationCentral):
    entity_type = "intersight_nodes_to_be_onboarded"

    def __init__(self, module):
        resource_type = "/imaged_nodes/onboard"
        super(ImagedNodeOnboard, self).__init__(module, resource_type=resource_type)

    def onboard_node_by_serial(self, serial):
        hw_mgr = HardwareManager(self.module)
        hw_mgr_res = hw_mgr.list({})
        self.module.log(msg=f"hw_mgr_res: {hw_mgr_res}")
        hw_mgrs = hw_mgr_res["hardware_managers"]

        for hwm in hw_mgrs:
            hw_node_controller = FoundationCentral(
                self.module,
                resource_type=f"/hardware_managers/{hwm["hardware_manager_uuid"]}/nodes",
            )
            hw_nodes = hw_node_controller.list({})["nodes"]

            for node in hw_nodes:
                if node["node_serial"] == serial:
                    onboard_body = deepcopy(node)
                    onboard_body["entityId"] = node["node_serial"]
                    onboard_body["entityType"] = "intersight_nodes_to_be_onboarded"
                    onboard_body.update(
                        node["hardware_manager_data"]["intersight_data"]
                    )

                    onboard = FoundationCentral(
                        self.module, resource_type="/imaged_nodes/onboard"
                    )
                    return onboard.create(data=onboard_body)

        return None
