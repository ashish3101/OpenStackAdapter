import os
import time
import logging

from Image_Adapter import Image_Adapter
from VM_Adapter import VM_Adapter
from Cloud_Attributes import Cloud_Attributes

import keystoneclient.v2_0.client as ksclient
from credentials import get_keystone_creds

import novaclient.v1_1.client as nvclient
from credentials import get_nova_creds


class Main(object):

    """docstring for Main"""
            

    def __init__(self, image_name, image_path, vm_name, vm_ram, vm_disk, vm_vcpus):           

        """
        Constructor to create a Connection, an Image Instance and a VM Instance
    
        :param image_name: The name of the image to be created.
        :param image_path: The path of the image for creation.
        :param vm_name: The name of the virtual machine to create
        :param vm_ram: The ram size of the virtual machine.
        :param vm_disk: The disk size of the virtual machine.
        :param vm_vcpus: Number of CPU's required by the virtual machine.
        """

        logging.basicConfig(filename='openstack.log', level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s' , datefmt='%m/%d/%Y %I:%M:%S %p')

        try:
            cloud_adapter = Cloud_Attributes()
            
            logging.info('Establishing Connection.')

            # Connections with keystoneClient(identity API) --------------------
            creds = get_keystone_creds()
            self.keystone = ksclient.Client(**creds)

            # Connections with novaClient(compute API) --------------------    
            creds = get_nova_creds()
            self.nova = nvclient.Client(**creds)
        except:
            logging.error('Invalid Credentials.')
            logging.critical('Connection Aborted.')
            raise
        
        # Creating IMAGE instance --------------------             
        try:
            logging.info('Creating Image Instance.')
            image = Image_Adapter(image_name, image_path)  
        except:
            logging.error('Image not Created.')
            raise     
        
        # Creating VM instance --------------------                
        try:
            logging.info('Creating Virtual Machine.')
            
            image_list = cloud_adapter.get_os_specific_image_list(image_name)
            image_details = image_list.get(image_name)           
            image_id = image_details.get('Image_ID')
            
            instance = VM_Adapter(vm_name, image_id, vm_ram, vm_disk, vm_vcpus)  
        except:
            logging.error('Virtual Machine not Created.')
            raise


main = Main(image_name='ubuntu', image_path='/home/openstack/Downloads/precise-server-cloudimg-amd64-disk1.img', vm_name='ubuntu_vm', vm_ram=2048, vm_disk=10, vm_vcpus=3)