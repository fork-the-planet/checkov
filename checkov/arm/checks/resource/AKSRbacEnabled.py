from __future__ import annotations

from typing import Any

from checkov.common.models.enums import CheckResult, CheckCategories
from checkov.arm.base_resource_check import BaseResourceCheck


class AKSRbacEnabled(BaseResourceCheck):
    def __init__(self) -> None:
        # apiVersion 2017-08-03 = Fail - No enableRBAC option to configure
        name = "Ensure RBAC is enabled on AKS clusters"
        id = "CKV_AZURE_5"
        supported_resources = ('Microsoft.ContainerService/managedClusters',)
        categories = (CheckCategories.KUBERNETES,)
        super().__init__(name=name, id=id, categories=categories, supported_resources=supported_resources)

    def scan_resource_conf(self, conf: dict[str, Any]) -> CheckResult:
        if "apiVersion" in conf:
            if conf["apiVersion"] == "2017-08-31":
                # No enableRBAC option to configure
                self.evaluated_keys = ["apiVersion"]
                return CheckResult.FAILED

        self.evaluated_keys = ["properties"]
        properties = conf.get('properties')
        if not properties or not isinstance(properties, dict):
            return CheckResult.FAILED
        enable_RBAC = properties.get('enableRBAC')
        if str(enable_RBAC).lower() == "true":
            return CheckResult.PASSED
        self.evaluated_keys.append("properties/enableRBAC")
        return CheckResult.FAILED


check = AKSRbacEnabled()
