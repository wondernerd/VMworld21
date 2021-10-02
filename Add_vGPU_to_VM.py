#Add_vGPU_to_VM
from __future__ import print_function
from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vim
from pyVmomi import vmodl

import argparse
import atexit
import getpass
import ssl
from pyVim.task import WaitForTask

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

    vm = None
    TempVMlist = HostContent.viewManager.CreateContainerView(HostContent.rootFolder,\
        [vim.VirtualMachine], True)
    for managed_VM_ref in TempVMlist.view: #Go thought VM list
        if managed_VM_ref.name == "VMworld2021": #find Desired VM
            print(managed_VM_ref)
            print(managed_VM_ref.name)
            vm = managed_VM_ref #Capture VM as an obj to use next
    if vm != None: #Safety to make sure not added to null object
        cspec = vim.vm.ConfigSpec()
        cspec.deviceChange = [vim.VirtualDeviceConfigSpec()]
        cspec.deviceChange[0].operation = 'add'
        cspec.deviceChange[0].device = vim.VirtualPCIPassthrough()
        cspec.deviceChange[0].device.deviceInfo = vim.Description()
        cspec.deviceChange[0].device.deviceInfo.summary = 'NVIDIA GRID vGPU grid_p4-4q'
        cspec.deviceChange[0].device.deviceInfo.label = 'New PCI device'
        cspec.deviceChange[0].device.backing = \
            vim.VirtualPCIPassthroughVmiopBackingInfo(vgpu='grid_p4-4q')
        #cspec.deviceChange[0].device.backing.vgpu =str('grid_p4-2q')
        WaitForTask(vm.Reconfigure(cspec))

        
###################################################
# End New Content
###################################################

    return 0
   

if __name__ == "__main__":
   main()