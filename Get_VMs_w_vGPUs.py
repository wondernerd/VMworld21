#Get_VMs_w_vGPUs
from __future__ import print_function

from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vim
from pyVmomi import vmodl

import argparse
import atexit
import getpass
import ssl

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

    DataCenterContent = HostContent.rootFolder.childEntity[0] #Assume single DC
    VMs = DataCenterContent.vmFolder.childEntity
    for i in VMs:
        #print("VM Name: "+ i.name)

        if isinstance(i,vim.Folder):
            #**************found a folder***************
            for ChildVM in i.childEntity:
                
                # Does it have a vGPU
                for VMVirtDevice in ChildVM.config.hardware.device:
                    if isinstance(VMVirtDevice, vim.VirtualPCIPassthrough) and \
                        hasattr(VMVirtDevice.backing, "vgpu"):
                        print("VM Name: "+ ChildVM.name)
                        print("In Folder: "+ ChildVM.parent.name)
                        print("Device Backing: " + VMVirtDevice.backing.vgpu)
                        print("Device Label: " + VMVirtDevice.deviceInfo.label)
                        print("Device Summary: " + VMVirtDevice.deviceInfo.summary)
                        print("*************************************")
        #print(i.parent.name)
        #print(i.childType)
        
###################################################
# End New Content
###################################################

    return 0
   

if __name__ == "__main__":
   main()