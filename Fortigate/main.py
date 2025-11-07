# third parties
from sekoia_automation.module import Module

# internals
from fortigate.action_fortigate_disable_local_user import FortigateDisableLocalUserAction

if __name__ == "__main__":
    module = Module()

    module.register(FortigateDisableLocalUserAction, "fortigate_disable_local_user")
    module.run()
