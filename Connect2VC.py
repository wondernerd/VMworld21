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
    print(HostContent)

    ###################################################
    # End New Content
    ###################################################

    return 0
   

if __name__ == "__main__":
   main()