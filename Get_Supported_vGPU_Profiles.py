#Get_Supported_GPUs
from __future__ import print_function

from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vim
from pyVmomi import vmodl

import argparse
import atexit
import getpass
import ssl

from pyVmomi.VmomiSupport import NoneType

def main():
    context = None
    if hasattr(ssl, '_create_unverified_context'):
        context = ssl._create_unverified_context()
    si = SmartConnect(host="vsa01.wondernerd.local",
                        user="VMworld21@wondernerd.local",
                        pwd="VMware-1",
                        port=443,
                        sslContext=context)
    if not si:
        print("Could not connect to the specified host using specified "
             "username and password")
        return -1

    atexit.register(Disconnect, si)

###################################################
# New Content
###################################################

    HostContent=si.content
    TempHold = HostContent.viewManager.CreateContainerView(
        HostContent.rootFolder,[vim.HostSystem], True)
    for managed_object_ref in TempHold.view:
        print(managed_object_ref.name)
        try:
            #print(isinstance(managed_object_ref.config, NoneType))
            if isinstance(managed_object_ref.config, NoneType) == False:
                if managed_object_ref.config.graphicsInfo != []:
                    for GPU_Profile in managed_object_ref.config.sharedPassthruGpuTypes:
                        print(GPU_Profile)
                else:
                    print("No GPUs found")
            else:
                print("Host powered off")
        except:
            print("Host not accessable")

###################################################
# End New Content
###################################################

    return 0
   

if __name__ == "__main__":
   main()
