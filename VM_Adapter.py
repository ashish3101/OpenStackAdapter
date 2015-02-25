import os
import time
import boto.ec2
import boto.manage.cmdshell
import logging
import random
import subprocess
from datetime import date,timedelta

import novaclient.v1_1.client as nvclient
from credentials import get_nova_creds
       

class VM_Adapter(object):

    """docstring for VM_Adapter"""
            
    def __init__(self, vm_name, image_id, vm_ram, vm_disk, vm_vcpus):  

        """
        Constructor to create a connection and a Virtual Machine.
    
        :param vm_name: The name of the Virtual Machine to create
        :param image_name: The name of the image through which we create.
        :param vm_ram: The ram size of the Virtual Machine.
        :param vm_disk: The disk size of the Virtual Machine.
        :param vm_vcpus: Number of CPU's required by the Virtual Machine.
        """

        logging.basicConfig(filename='openstack.log', level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s' , datefmt='%m/%d/%Y %I:%M:%S %p')
        
        try:
        	# Connections with novaClient(compute API) --------------------
            logging.info('Establishing Connection.')    
            creds = get_nova_creds()
            self.nova = nvclient.Client(**creds)
        except:
            logging.error('Invalid Credentials.')
            logging.critical('Connection Aborted.')
            raise        
        
        try:
        	# Connections with novaClient(compute API) --------------------
            is_instance_present = False
            instance = self.create(vm_name, image_id, vm_ram, vm_disk, vm_vcpus)
            self.instance = instance
        except:
            logging.error('Virtual Machine not Created.')    
            raise

    # Creating Virtual Machine --------------------                
    def create(self, vm_name, image_id, vm_ram, vm_disk, vm_vcpus):

    	"""
        Create a VM Instance.
    
        :param vm_name: The name of the Virtual Machine to create
        :param image_name: The name of the image through which we create.
        :param vm_ram: The ram size of the Virtual Machine.
        :param vm_disk: The disk size of the Virtual Machine.
        :param vm_vcpus: Number of CPU's required by the Virtual Machine.
        :rtype: :object: Virtual Machine object.
        """

        try:   
            self.key_name = 'key_pair'        
            logging.info('Waiting for Virtual Machine to Create.')

            if not self.nova.keypairs.findall(name=self.key_name):
                with open(os.path.expanduser('~/.ssh/id_rsa.pub')) as fpubkey:
                    self.nova.keypairs.create(name=self.key_name, public_key=fpubkey.read())
            
            vm_flavor = self.set_flavor(vm_ram, vm_disk, vm_vcpus)
            image_object = self.nova.images.get(image_id)
            
            instance = self.nova.servers.create(name=vm_name, image=image_object, flavor=vm_flavor, meta=None, key_name=self.key_name)
            logging.info('Virtual Machine is in Pending State.')
            self.is_instance_present = True
            return instance
        except:
            logging.error('Virtual Machine not Created.')
            raise


    # Set Flavor for Virtual Machine --------------------
    def set_flavor(self, vm_ram, vm_disk, vm_vcpus):

        """
        Set the Flavor for a Virtual Machine.
    
        :param vm_ram: The ram size of the Virtual Machine.
        :param vm_disk: The disk size of the Virtual Machine.
        :param vm_vcpus: Number of CPU's required by the Virtual Machine.
        :rtype: string: The ID of the flavor.
        """

        try:
            logging.info('Flavor is being set.')
            flavor_flag = 0
            for flavor in self.nova.flavors.list():
                if (flavor.ram == vm_ram) and (flavor.disk == vm_disk) and (flavor.vcpus == vm_vcpus):
                    flavor_flag = 1
                    vm_flavor = flavor.id 
                    logging.info('Flavor set from the existing flavors.')
            
            if flavor_flag == 0:
                flavor_name = 'flavor_'+str(vm_ram)+'_'+str(vm_disk)+'_'+str(vm_vcpus)
                flavor = self.nova.flavors.create(name=flavor_name, ram=vm_ram, vcpus=vm_vcpus, disk=vm_disk)
                vm_flavor = flavor.id
                logging.info('Flavor set by creating a new flavor.')
            return vm_flavor
        except:
            logging.error('Flavor not created.')
            raise

    
    # Destroy Virtual Machine --------------------
    def destroy(self):

        """
        Destroy(Delete) a Virtual Machine.
    
        :rtype: NULL
        """
        
        try:
       	    assert(self.is_instance_present)
        except:
            logging.warning('Virtual Machine does not exist.')
            raise
        try:
            logging.info('Waiting for Virtual Machine to Terminate.')
            logging.info('Terminated Virtual Machine IP is %s', self.instance.networks)
            logging.info('Terminated Virtual Machine ID is %s', self.instance.id)
            self.instance = self.nova.servers.get(self.instance.id)
            self.is_instance_present = False
            self.instance.delete()
            del self.instance
            logging.info('Virtual Machine has now been Terminated.')
        except:
            logging.error('Virtual Machine not Terminated.')    
            raise  


    # Start Virtual Machine -------------------- 
    def start(self):

        """
        Start a Virtual Machine.
   
        :rtype: NULL
        """

        try:
            assert(self.is_instance_present)
        except:
            logging.warning('Virtual Machine does not exist.')
            raise
        try:
            self.instance = self.nova.servers.get(self.instance.id)
            if self.instance.status == 'ACTIVE':     
                logging.info('%s Virtual Machine is already Running', self.instance.id)
            elif self.instance.status != 'ACTIVE':    
                logging.info('Waiting for Virtual Machine to Start.')
                self.instance.start()
                logging.info('Virtual Machine is now getting Started.')
                logging.info('Started Virtual Machine IP is %s', self.instance.networks)
                logging.info('Started Virtual Machine ID is %s', self.instance.id)
        except:
            logging.error('Virtual Machine not Started.')
            raise  


    # Stop Virtual Machine -------------------- 
    def stop(self):

        """
        Stop a Virtual Machine.

        :rtype: NULL
        """

        try:
            assert(self.is_instance_present)
        except:
            logging.warning('Virtual Machine does not exist.')
            raise       
        try:
            if self.instance.status == 'SHUTOFF':
                logging.info('%s Virtual Machine is already Stopped.', self.instance.id)
            elif self.instance.status != 'SHUTOFF':
                self.instance.stop()
                logging.info('Waiting for Virtual Machine to Stop.....')
                logging.info('Stopped Virtual Machine IP is %s', self.instance.networks)
                logging.info('Stopped Virtual Machine ID is %s', self.instance.id)
        except:
            logging.info('Virtual Machine is not Stopped(Shut Off).')
            raise  
             

    # Suspend Virtual Machine -------------------- 
    def suspend(self):

        """
        Suspend a Virtual Machine.

        :rtype: NULL
        """
        
        try:
            assert(self.is_instance_present)
        except:
            logging.warning('Virtual Machine does not exist.')
            raise        
        try:
            if self.instance.status == 'SUSPENDED':
                logging.info('%s Virtual Machine is already Suspended', self.instance.id)
            elif self.instance.status != 'SUSPENDED':
                self.instance.suspend()
                logging.info('Waiting for Virtual Machine to Suspend.')
                logging.info('Suspended Virtual Machine IP is %s', self.instance.networks)
                logging.info('Suspended Virtual Machine ID is %s', self.instance.id)
        except:
            logging.info('Virtual Machine is not Suspended.')
            raise  


    # Pause Virtual Machine -------------------- 
    def pause(self):

        """
        Pause a Virtual Machine.

        :rtype: NULL
        """

        try:
            assert(self.is_instance_present)
        except:
            logging.warning('Virtual Machine does not exist.')
            raise
        try:
            if self.instance.status == 'PAUSED':
                logging.info('%s Virtual Machine is already Paused', self.instance.id)
            elif self.instance.status != 'PAUSED':
                self.instance.pause()
                logging.info('Waiting for Virtual Machine to Pause.')
                logging.info('Paused Virtual Machine IP is %s', self.instance.networks)
                logging.info('Paused Virtual Machine ID is %s', self.instance.id)
        except:
            logging.info('Virtual Machine is not Paused.')
            raise  


    # Validate Virtual Machine ID -------------------- 
    def validate_vm_id(self):
        
        """
        Check validity of a Virtual Machine.
                
        :rtype: NULL 
        """
        
        try:
            assert(self.is_instance_present)
        except:
            logging.warning('Virtual Machine does not exist.')
            raise        
        try:
            vm_list = self.nova.servers.list()
            for vm in vm_list:
                if self.instance.id == vm.id:
                    logging.info('%s Virtual Machine is a valid Instance.', self.instance.id)
                    logging.info('Virtual Machine IP is %s', self.instance.networks)
                    logging.info('Virtual Machine ID is %s', self.instance.id)
                    return self.instance.id
        except:
            logging.info('%s Virtual Machine is a invalid Instance.', self.instance.id)
            raise  
                

    # Is Running Virtual Machine -------------------- 
    def is_running_vm(self):

        """
        Check whether Virtual Machine is running or not.

        :rtype: string: Returning the status of the Virtual Machine.
        """

        try:
            assert(self.is_instance_present)
        except:
            logging.warning('Virtual Machine does not exist.')
            raise        
        try:
            if self.instance.status == 'ACTIVE':
                logging.info('%s Virtual Machine is a Running Instance.', self.instance.id)
                logging.info('Running Virtual Machine IP is %s', self.instance.networks)
                logging.info('Running Virtual Machine ID is %s', self.instance.id)
                return self.instance.status
            else:
                logging.info('%s Instance is a not Running Instance.', self.instance.id)
                logging.info('Not Running Virtual Machine IP is %s', self.instance.networks)
                logging.info('Not Running Virtual Machine ID is %s', self.instance.id)
                return self.instance.status
        except:
            logging.error('%s Virtual Machine details are incomplete. Status cant be retrieved.', self.instance.id)
            raise  
                

    # Get Virtual Machine IP -------------------- 
    def get_ip(self):

        """
        Get IP of a Virtual Machine.

        :rtype: string: IP Address of the Virtual Machine.
        """

        try:
            assert(self.is_instance_present)
        except:
            logging.warning('Virtual Machine does not exist.')
            raise        
        try:
            logging.info('Virtual Machine IP is %s', self.instance.networks)
            logging.info('Virtual Machine ID is %s', self.instance.id)
            return self.instance.networks
        except:
            logging.error('%s Virtual Machine details are incomplete. IP cant be retrieved.', self.instance.id)
            raise  
                

    # Get RAM Size of a Virtual Machine -------------------- 
    def get_ram(self):
        
        """
        Get ram size of a Virtual Machine.

        :rtype: integer: Ram Size of the Virtual Machine.
        """

        try:
            assert(self.is_instance_present)
        except:
            logging.warning('Virtual Machine does not exist.')
            raise        
        try:
            flavor_id = self.instance.flavor.get('id')
            flavor_object = self.nova.flavors.get(flavor_id)
            ram = flavor_object.ram
            logging.info('Virtual Machine ID is %s', self.instance.id)
            logging.info('Virtual Machine RAM Size is %s', ram)
            return ram
        except:
            logging.error('%s Virtual Machine details are incomplete. Ram Size cant be retrieved.', self.instance.id)
            raise  
                

    # Get Disk Size of a Virtual Machine -------------------- 
    def get_disk(self):

        """
        Get disk size of a Virtual Machine.

        :rtype: integer: Disk Size of the Virtual Machine. 
        """
        
        try:
            assert(self.is_instance_present)
        except:
            logging.warning('Virtual Machine does not exist.')
            raise
        try:
            flavor_id = self.instance.flavor.get('id')
            flavor_object = self.nova.flavors.get(flavor_id)
            disk = flavor_object.disk
            logging.info('Virtual Machine ID is %s', self.instance.id)
            logging.info('Virtual Machine DISK Size is %s', disk)
            return disk
        except:
            logging.error('%s Virtual Machine details are incomplete. Disk Size cant be retrieved.', self.instance.id)
            raise  


    # Get flavor of Virtual Machine -------------------- 
    def get_flavor(self):

        """
        Get flavor of a Virtual Machine.
                
        :rtype: dict: Details of the Virtual Machine flavor 
        """
        
        try:
            assert(self.is_instance_present)
        except:
            logging.warning('Virtual Machine does not exist.')
            raise        
        try:
            flavor_id = self.instance.flavor.get('id')
            flavor_object = self.nova.flavors.get(flavor_id)                
            flavor = {}
            flavor['Virtual_Machine_Name'] = str(self.instance.name)    
            flavor['Virtual_Machine_ID'] = str(self.instance.id)
            flavor['Flavor_Name'] = str(flavor_object.name)  
            flavor['Flavor_ID'] = str(flavor_object.id)  
            flavor['Ram_Size'] = flavor_object.ram  
            flavor['Disk_Size'] = flavor_object.disk  
            logging.info('Virtual Machine ID is %s', self.instance.id)
            logging.info('Virtual Machine Flavor is %s', flavor)
            return flavor
        except:
            logging.error('%s Virtual Machine details are incomplete. Flavor cant be retrieved.', self.instance.id)
            raise  
        
    
    # Change RAM size of a Virtual Machine -------------------- 
    def change_ram(self, new_ram):

        """
        Change ram size (keeping other things same) of a Virtual Machine.

        :param new_ram: The new ram size to be allocated.
        :rtype: NULL 
        """

        try:
            assert(self.is_instance_present)
        except:
            logging.warning('Virtual Machine does not exist.')
            raise
        try:     
            flavor_id = self.instance.flavor.get('id')
            flavor_object = self.nova.flavors.get(flavor_id)
            vm_disk = flavor_object.disk
            vm_vcpus = flavor_object.vcpus
            
            new_flavor_id = self.set_flavor(new_ram, vm_disk, vm_vcpus)
            new_flavor_object = self.nova.flavors.get(new_flavor_id)
              
            logging.info('New_Flavor_Object %s', new_flavor_object)
            logging.info('New_Flavor_ID %s', new_flavor_id)
                
            self.nova.servers.resize(server=self.instance.id, flavor=new_flavor_object)  
            self.instance = self.nova.servers.get(self.instance.id)
                
            while self.instance.status != 'VERIFY_RESIZE':
                time.sleep(5)         
                logging.info('Checking for Confirmation')
                self.instance = self.nova.servers.get(self.instance.id)
            
            self.nova.servers.confirm_resize(server=self.instance)
                
            logging.info('Confirmation Done')
            logging.info('Virtual Machine ID is %s', self.instance.id)
            logging.info('Virtual Machine FLAVOR is %s', new_flavor_object.name)
            logging.info('Virtual Machine RAM Size is %s', new_flavor_object.ram)
            logging.info('Virtual Machine DISK Size is %s', new_flavor_object.disk)
            logging.info('Virtual Machine VCPUS Size is %s', new_flavor_object.vcpus)
        except:
            logging.error('%s Virtual Machine details are incomplete. Ram Size cant be changed.', self.instance.id)
            raise  
                 

    # Change DISK size of a Virtual Machine -------------------- 
    def change_disk(self, new_disk):

        """
        Change disk size (keeping other things same) of a Virtual Machine.

        :param new_disk: The new disk size to be allocated.
        :rtype: NULL 
        """

        try:
            assert(self.is_instance_present)
        except:
            logging.warning('Virtual Machine does not exist.')
            raise
        try:     
            flavor_id = self.instance.flavor.get('id')
            flavor_object = self.nova.flavors.get(flavor_id)
            vm_ram = flavor_object.ram
            vm_vcpus = flavor_object.vcpus
            
            new_flavor_id = self.set_flavor(vm_ram, new_disk, vm_vcpus)
            new_flavor_object = self.nova.flavors.get(new_flavor_id)
              
            logging.info('New_Flavor_Object %s', new_flavor_object)
            logging.info('New_Flavor_ID %s', new_flavor_id)
                
            self.nova.servers.resize(server=self.instance.id, flavor=new_flavor_object)  
            self.instance = self.nova.servers.get(self.instance.id)
                
            while self.instance.status != 'VERIFY_RESIZE':
                time.sleep(5)         
                logging.info('Checking for Confirmation')
                self.instance = self.nova.servers.get(self.instance.id)
            
            self.nova.servers.confirm_resize(server=self.instance)
                
            logging.info('Confirmation Done')
            logging.info('Virtual Machine ID is %s', self.instance.id)
            logging.info('Virtual Machine FLAVOR is %s', new_flavor_object.name)
            logging.info('Virtual Machine RAM Size is %s', new_flavor_object.ram)
            logging.info('Virtual Machine DISK Size is %s', new_flavor_object.disk)
            logging.info('Virtual Machine VCPUS Size is %s', new_flavor_object.vcpus)
        except:
            logging.error('%s Virtual Machine details are incomplete. Disk Size cant be changed.', self.instance.id)
            raise  


    # Change flavor of Virtual Machine -------------------- 
    def change_flavor(self, new_ram, new_disk):
        
        """
        Change flavor of a Virtual Machine.

        :param new_ram: The new ram size to be allocated.
        :param new_disk: The new disk size to be allocated.
        :rtype: NULL 
        """

        try:
            assert(self.is_instance_present)
        except:
            logging.warning('Virtual Machine does not exist.')
            raise
        try:     
            flavor_id = self.instance.flavor.get('id')
            flavor_object = self.nova.flavors.get(flavor_id)
            vm_vcpus = flavor_object.vcpus
            
            new_flavor_id = self.set_flavor(new_ram, new_disk, vm_vcpus)
            new_flavor_object = self.nova.flavors.get(new_flavor_id)
            
            logging.info('New_Flavor_Object %s', new_flavor_object)
            logging.info('New_Flavor_ID %s', new_flavor_id)
                
            self.nova.servers.resize(server=self.instance.id, flavor=new_flavor_object)  
            self.instance = self.nova.servers.get(self.instance.id)
                
            while self.instance.status != 'VERIFY_RESIZE':
                time.sleep(5)         
                logging.info('Checking for Confirmation')
                self.instance = self.nova.servers.get(self.instance.id)
            
            self.nova.servers.confirm_resize(server=self.instance)
            self.instance = self.nova.servers.get(self.instance.id)
                
            logging.info('Virtual Machine ID is %s', self.instance.id)
            logging.info('Virtual Machine FLAVOR is %s', new_flavor_object.name)
            logging.info('Virtual Machine DISK Size is %s', new_flavor_object.disk)
            logging.info('Virtual Machine RAM Size is %s', new_flavor_object.ram)
            logging.info('Virtual Machine VCPUS Size is %s', new_flavor_object.vcpus)
        except:
            logging.error('%s Virtual Machine details are incomplete. DISK Size cant be changed.', self.instance.id)
            raise  

    
    # Restart Virtual Machine -------------------- 
    def restart(self):

        """
        Restart a Virtual Machine.

        :rtype: NULL
        """

        try:
            assert(self.is_instance_present)
        except:
            logging.warning('Virtual Machine does not exist.')
            raise        
        try:     
            logging.info('Present status of Virtual Machine is %s', self.instance.status)
            self.instance = self.nova.servers.get(self.instance.id)
             
            if self.instance.status == 'ACTIVE':
                logging.info('Rebooting an ACTIVE Virtual Machine')
                self.instance = self.nova.servers.get(self.instance.id)
                self.nova.servers.reboot(self.instance,reboot_type='SOFT')
                logging.info('Waiting for the Virtual Machine to Reboot')
                
            elif self.instance.status == 'PAUSED':
                logging.info('Unpausing(Starting) a PAUSED Virtual Machine')
                self.nova.servers.unpause(self.instance)
                while self.instance.status != 'ACTIVE':    
                    time.sleep(20)
                    self.instance = self.nova.servers.get(self.instance.id)
                    logging.info('Waiting for the Virtual Machine to Unpause(Start)')
                logging.info('Rebooting an ACTIVE Virtual Machine')
                self.instance = self.nova.servers.get(self.instance.id)
                self.nova.servers.reboot(self.instance,reboot_type='SOFT') 
                
            elif self.instance.status == 'SUSPENDED':
                logging.info('Resuming(Starting) a SUSPENDED Virtual Machine')
                self.nova.servers.resume(self.instance)
                self.instance = self.nova.servers.get(self.instance.id)
                while self.instance.status != 'ACTIVE':    
                    time.sleep(20)
                    self.instance = self.nova.servers.get(self.instance.id)
                    logging.info('Waiting for the Virtual Machine to Resume(Start)')
                logging.info('Rebooting an ACTIVE Virtual Machine')
                self.instance = self.nova.servers.get(self.instance.id)
                self.nova.servers.reboot(self.instance,reboot_type='SOFT') 
                logging.info('Waiting for the Virtual Machine to Reboot')
        except:
            logging.error('%s Virtual Machine details are incomplete. Virtual Machine REBOOT is not possible.', self.instance.id)
            raise  

    

#vm_1 = VM_Adapter(vm_name='h2', image_name='image1', vm_ram=2048, vm_disk=20, vm_vcpus=1)
#vm_1.set_flavor(vm_ram=2000, vm_disk=2, vm_vcpus=1)
#vm_1.stop() 
#vm_1.start() 
#vm_1.restart() 
#vm_1.suspend()
#vm_1.restart()
#vm_1.pause()
#vm_1.restart()
#vm_1.validate_vm_id()
#vm_1.is_running_vm()
#vm_1.get_ip()
#vm_1.get_ram()
#vm_1.get_disk()
#vm_1.get_flavor()
#vm_1.change_ram(new_ram=3000)
#vm_1.change_disk(new_disk=30)
#vm_1.change_flavor(new_ram=3000, new_disk=35)
#vm_1.destroy()

#vm_1 = VM_Adapter(vm_name='h1', image_id='2df7f480-587a-401d-af2f-fab947303dfb', vm_ram=2048, vm_disk=20, vm_vcpus=1)
#time.sleep(10)
#vm_1.ssh_connect_to_vm()
