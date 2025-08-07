#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_foundation_central_imaged_nodes_onboard
short_description: Nutanix module to onboard a node from a hardware manager (e.g. Intersight)
version_added: 2.2.0
description: 'Nutanix module to onboard a node from a hardware manager (e.g. Intersight)'
options:
  serial:
    description:
      - Serial number of node to onboard
    type: str
extends_documentation_fragment:
      - nutanix.ncp.ntnx_credentials
      - nutanix.ncp.ntnx_operations
author:
 - Chris Gascoigne (@cgascoig)
"""

EXAMPLES = r"""
- name: onboard nodes from Intersight
  ntnx_foundation_central:
    nutanix_host: '{{ pc }}'
    nutanix_username: '{{ username }}'
    nutanix_password: '{{ password }}'
    validate_certs: false
    serial: "ABC12345DEF"
"""

RETURN = r"""
response:
  description: Sample response when onboarding node
  returned: always
  type: dict
  sample: {
    "imaged_node_uuid": "6dc8f33c-c293-42df-5988-6c37b88f7bff"
  }
"""

import time  # noqa: E402

from ..module_utils.base_module import BaseModule  # noqa: E402
from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v3.fc.imaged_nodes import ImagedNode  # noqa: E402
from ..module_utils.v3.fc.imaged_nodes_onboard import ImagedNodeOnboard  # noqa: E402


def onboard_nodes(module, result):
    av = ImagedNode(module)
    node, _ = av.node_details_by_node_serial(module.params["serial"])
    if node is not None:
        # Node already onboarded
        result["response"] = node
        return

    onboarding = ImagedNodeOnboard(module)
    if module.check_mode:
        result["response"] = {}  # TODO: FIX
        return

    res = onboarding.onboard_node_by_serial(serial=module.params["serial"])
    if res is None:
        module.fail_json(msg="serial not found")
        return

    result["response"] = res
    result["changed"] = True


def get_module_spec():
    module_args = dict(serial=dict(type="str", required=True, default=None))

    return module_args


def run_module():
    module = BaseModule(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
    )
    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "error": None,
        "response": None,
        "imaged_cluster_uuid": None,
    }
    state = module.params["state"]
    if state == "present":
        onboard_nodes(module, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
