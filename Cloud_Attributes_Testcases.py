import unittest
from Cloud_Attributes import Cloud_Attributes


class TddInPython(unittest.TestCase):

    def test_get_image_list(self):
        try:   
            cloud_adapter = Cloud_Attributes()
        except:
            print '\n\nUnable to Connect to OpenStack.'  
            raise
        
        try:
            image_list = cloud_adapter.get_image_list()
            print '\n\nImage List :\n',image_list
        except:
            print '\n\nUnable to find Images.'
            raise


    def test_get_os_specific_image_list(self):
        try:   
            cloud_adapter = Cloud_Attributes()
        except:
            print '\n\nUnable to Connect to OpenStack.'  
            raise
        
        try:
            image_list = cloud_adapter.get_os_specific_image_list('cirros-0.3.2-x86_64-uec-kernel')
            print '\n\nOS Specific Image List :\n',image_list
        except:
            print '\n\nUnable to find OS Specific Images.'
            raise


    def test_get_vm_list(self):
        try:   
            cloud_adapter = Cloud_Attributes()
        except:
            print '\n\nUnable to Connect to OpenStack.'  
            raise

        try:
            vm_list = cloud_adapter.get_vm_list()
            print '\n\nVM Instances List :\n',vm_list
        except:
            print '\n\nUnable to find Virtual Machine.'
            raise


    def test_get_running_vm_list(self):
        try:   
            cloud_adapter = Cloud_Attributes()
        except:
            print '\n\nUnable to Connect to OpenStack.'  
            raise

        try:
            running_vm_list = cloud_adapter.get_vm_list()
            print '\n\nRunning Virtual Machine List :\n',running_vm_list
        except:
            print '\n\nUnable to find Running Virtual Machine.'
            raise


    def test_get_vm_count(self):
        try:   
            cloud_adapter = Cloud_Attributes()
        except:
            print '\n\nUnable to Connect to OpenStack.'  
            raise        

        try:
            vm_count = cloud_adapter.get_vm_count()
            print '\n\nTotal Number(Count) of Virtual Machines :\n',vm_count
        except:
            print '\n\nUnable to find Total Number(Count) of Virtual Machines.'
            raise

    def test_get_flavor_list(self):
        try:   
            cloud_adapter = Cloud_Attributes()
        except:
            print '\n\nUnable to Connect to OpenStack.'  
            raise

        try:
            flavor_list = cloud_adapter.get_flavor_list()
            print '\n\nFlavor List :\n',flavor_list
        except:
            print '\n\nUnable to find Flavors.'
            raise