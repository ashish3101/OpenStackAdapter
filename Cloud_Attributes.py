import os
import time
import logging

import novaclient.v1_1.client as nvclient
from credentials import get_nova_creds


class Cloud_Attributes(object):

    """docstring for Cloud_Attributes"""

    def __init__(self):           

        """
        Constructor to create a Connection.
        """

        logging.basicConfig(filename='openstack.log', level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s' , datefmt='%m/%d/%Y %I:%M:%S %p')
        
        try:
            # Connections with novaClient(compute API) --------------------    
            logging.info('Establishing Connection.')
            creds = get_nova_creds()
            self.nova = nvclient.Client(**creds)
        except:
            logging.error('Connection not Establised')
            raise

    
    # Get Image List -------------------- 
    def get_image_list(self):          

        """
        List Images.

        :rtype: dict: Image List
        """

        try:
            logging.info('Retrieving the Image List.')
            images = self.nova.images.list(detailed=True)
            image_list = {}
            for image in images:
                image_detail = {}
                image_detail['Image_ID'] = str(image.id)
                image_detail['Image_Name'] = str(image.name)
                image_detail['Image_Status'] = str(image.status)
                image_list[str(image.name)] = image_detail
            logging.info('Retrieving the Image List with details.')
            return image_list
        except:
            logging.error('The Image List cant be Retrieved.')
            raise


    # Get os specific image --------------------
    def get_os_specific_image_list(self, os_name): 

        """
        List OS Specific Images.

        :rtype: dict: OS Specific Image List
        """

        try:
            logging.info('Retrieving the OS Specific Image List.')
            images = self.nova.images.list(detailed=True)
            os_image_list = {}
            for image in images:
            	if image.name == os_name:
                    image_detail = {}
                    image_detail['Image_ID'] = str(image.id)
                    image_detail['Image_Name'] = str(image.name)
                    image_detail['Image_Status'] = str(image.status)
                    os_image_list[str(image.name)] = image_detail
            logging.info('Retrieving the OS Specific Image List with details.')
            return os_image_list
        except:
            logging.error('The OS Specific Image List cant be Retrieved.')
            raise


    # Get list of all Virtual Machine -------------------- 
    def get_vm_list(self):

        """
        List of all Virtual Machine.

        :rtype: dict: Virtual Machine List
        """
        
        try:
            logging.info('Retrieving the Virtual Machines List.')
            vms = self.nova.servers.list()
            vm_list = {}
            for vm in vms:
            	vm_detail = {}
                vm_detail['Virtual_Machine_Name'] = str(vm.name)
                vm_detail['Virtual_Machine_ID'] = str(vm.id)
                vm_detail['Virtual_Machine_Status'] = str(vm.status)
                vm_list[str(vm.name)] = vm_detail
                
            logging.info('Retrieving the Virtual Machine list with details.')
            return vm_list
        except:
            logging.error('The Virtual Machine List cant be Retrieved.')
            raise


    # Get list of all running Virtual Machines -------------------- 
    def get_running_vm_list(self):

        """
        List of all Running Virtual Machine.

        :rtype: dict: Running Virtual Machine List   
        """
        
        try:
            logging.info('Retrieving the RUNNING Virtual Machine List.')
            vms = self.nova.servers.list()
            vm_list = {}
            for vm in vms:
                if vm.status == 'ACTIVE':
                    vm_detail = {}
                    vm_detail['Virtual_Machine_Name'] = str(vm.name)    
                    vm_detail['Virtual_Machine_ID'] = str(vm.id) 
                    vm_detail['Virtual_Machine_Status'] = str(vm.status) 
                    vm_list[str(vm.name)] = vm_detail 
                logging.info('Retrieving the Running Virtual Machine list with details.')
                return vm_list
        except:
            logging.error('The Running Virtual Machine list cant be Retrieved.')
            raise
 

    # Get count of Virtual Machine --------------------  
    def get_vm_count(self):

        """
        Get Total Number of Virtual Machine.

        :rtype: int: Number of Virtual Machine.
        """
        
        try:
            logging.info('Retrieving the Total Number of Virtual Machines present(count).')
            vm_list = self.nova.servers.list()
            vm_count = len(vm_list)
            return vm_count
        except:
            logging.error('The Virtual Machines Count cant be Retrieved.')
            raise

    
    # Get list of all Flavors -------------------- 
    def get_flavor_list(self):

        """
        List of all flavors.

        :rtype: dict: Flavor List 
        """
        try:
            logging.info('Retrieving the Flavor List.')
            flavorlist = self.nova.flavors.list()
            flavor_list = {}
            for flavor in flavorlist:
            	flavor_detail = {}
                flavor_detail['Flavor_Name'] = str(flavor.name)
                flavor_detail['Flavor_ID'] = str(flavor.id)
                flavor_detail['Flavor_Ram'] = str(flavor.ram)
                flavor_detail['Flavor_Disk'] = str(flavor.disk)
                flavor_detail['Flavor_vCPUs'] = str(flavor.vcpus)
                flavor_list[str(flavor.name)] = flavor_detail
                
            logging.info('Retrieving the Flavor List with details.')
            return flavor_list
        except:
            logging.error('The Flavor List cant be Retrieved.')
            raise