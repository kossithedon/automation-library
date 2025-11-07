import json

import requests
from requests import Response
from sekoia_automation.action import Action


class FortigateDisableLocalUserAction(Action):
    """
    Action to disable a local user on a remote fortigate
    """

    def run(self, arguments: dict) -> dict:
        """
        Parameters
        ----------
        name: the fw local user account name (type string)

        Returns
        -------
        Http status code: 200 if ok, 4xx if an error occurs
        """

        name = arguments["name"]

        payload: dict = {
            "json": {
                "status": "disable",
            }
        }

        for firewall in self.module.configuration["firewalls"]:
            base_ip: str = firewall.get("base_ip")
            base_port: str = firewall.get("base_port")
            api_key: str = firewall.get("api_key")
            vdom: str = firewall.get("vdom", "root")

            try:
                response: Response = requests.put(
                    "https://" + base_ip + ":" + base_port + "/api/v2/cmdb/user/local/" + name,
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {api_key}",
                    },
                    params={"vdom": vdom},
                    data=json.dumps(payload),
                    verify=False,
                    timeout=10,
                )
                response.raise_for_status()

            except requests.exceptions.Timeout:
                self.log("Time out session on a firewall", fw_ip=base_ip, level="error")

            except Exception:
                self.log(
                    "Impossible to disable the local user account on the firewall",
                    level="error",
                    fw_ip=base_ip,
                    fw_port=base_port,
                    data=payload,
                    account_name=name,
                )
                pass

        return payload
