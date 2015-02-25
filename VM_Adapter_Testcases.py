import unittest
import time
from Image_Adapter import Image_Adapter
from VM_Adapter import VM_Adapter
from Cloud_Attributes import Cloud_Attributes
from Main import Main


class TddInPython(unittest.TestCase):     
    
    def test_create(self):
        try:
            cloud_adapter = Cloud_Attributes()
            test_image = Image_Adapter(image_name='test_image', image_path='/home/openstack/Downloads/precise-server-cloudimg-amd64-disk1.img')
            image_list = cloud_adapter.get_os_specific_image_list('test_image')
            image_details = image_list.get('test_image')           
            image_id = image_details.get('Image_ID')
            
            prev_vm_list = cloud_adapter.get_vm_list()
            assert('testvm' not in prev_vm_list)
            
            vm_instance = VM_Adapter('testvm', image_id, 2048, 20, 1)
            count = 0
            while count <= 4:  
                time.sleep(pow(2,count))
                count+=1
            
            cur_vm_list = cloud_adapter.get_vm_list()
            assert('testvm' in cur_vm_list)
            print 'Virtual Machine successfully created.'
     
            vm_instance.destroy()
            test_image.delete()
        except:
            print 'Virtual Machine creation failed.'               
            test_image.delete()
            raise   
    
    
    def test_destroy(self):
        try:
            cloud_adapter = Cloud_Attributes()
            test_image = Image_Adapter(image_name='test_image', image_path='/home/openstack/Downloads/precise-server-cloudimg-amd64-disk1.img')
            image_list = cloud_adapter.get_os_specific_image_list('test_image')
            image_details = image_list.get('test_image')           
            image_id = image_details.get('Image_ID')
            
            vm_instance = VM_Adapter('testvm', image_id, 2048, 20, 1)
            count = 0
            while count <= 4:  
                time.sleep(pow(2,count))
                count+=1
        except:
            print 'Connection not establised.'   
            raise               
        try:
            prev_vm_list = cloud_adapter.get_vm_list()
            assert('testvm' in prev_vm_list)
            vm_instance.destroy()
            count = 0
            while count <= 4:  
                time.sleep(pow(2,count))
                count+=1
            cur_vm_list = cloud_adapter.get_vm_list()
            assert('testvm' not in cur_vm_list)
            print 'Virtual Machine successfully destroyed.'
            test_image.delete()
        except:
            print 'Virtual Machine not found.'   
            vm_instance.destroy()
            test_image.delete()
            raise
    

    def test_start(self):
        try:
            cloud_adapter = Cloud_Attributes()            
            test_image = Image_Adapter(image_name='test_image', image_path='/home/openstack/Downloads/precise-server-cloudimg-amd64-disk1.img')
            image_list = cloud_adapter.get_os_specific_image_list('test_image')
            image_details = image_list.get('test_image')           
            image_id = image_details.get('Image_ID')
            
            vm_instance = VM_Adapter('testvm', image_id, 2048, 20, 1)
            count = 0
            while count <= 4:  
                time.sleep(pow(2,count))
                count+=1
        except:
            print 'Connection not establised.'   
            raise               
        try:
            vm_instance.stop()
            count = 0
            while count <= 4:  
                time.sleep(pow(2,count))
                count+=1

            prev_vm_list = cloud_adapter.get_running_vm_list()
            assert('testvm' not in prev_vm_list)
            
            vm_instance.start()
            count = 0
            while count <= 4:  
                time.sleep(pow(2,count))
                count+=1

            cur_vm_list = cloud_adapter.get_running_vm_list()
            assert('testvm' in cur_vm_list)
            print 'Virtual Machine successfully started .'
            vm_instance.destroy()
            test_image.delete()
        except:
            print 'Virtual Machine not found.'   
            vm_instance.destroy()
            test_image.delete()
            raise  
    

    def test_stop(self):
        try:
            cloud_adapter = Cloud_Attributes()
            test_image = Image_Adapter(image_name='test_image', image_path='/home/openstack/Downloads/precise-server-cloudimg-amd64-disk1.img')
            image_list = cloud_adapter.get_os_specific_image_list('test_image')
            image_details = image_list.get('test_image')           
            image_id = image_details.get('Image_ID')
            
            vm_instance = VM_Adapter('testvm', image_id, 2048, 20, 1)
            count = 0
            while count <= 4:  
                time.sleep(pow(2,count))
                count+=1
        except:
            print 'Connection not establised.'   
            raise               
        try:
            prev_vm_list = cloud_adapter.get_running_vm_list()
            assert('testvm' in prev_vm_list)
            vm_instance.stop()
            count = 0
            while count <= 4:  
                time.sleep(pow(2,count))
                count+=1
            cur_vm_list = cloud_adapter.get_running_vm_list()
            assert('testvm' not in cur_vm_list)
            print 'Virtual Machine successfully stopped.'
            vm_instance.destroy()
            test_image.delete()
        except:
            print 'Virtual Machine not found.'   
            vm_instance.destroy()
            test_image.delete()
            raise   
    

    def test_suspend(self):
        try:
            cloud_adapter = Cloud_Attributes()
            test_image = Image_Adapter(image_name='test_image', image_path='/home/openstack/Downloads/precise-server-cloudimg-amd64-disk1.img')
            image_list = cloud_adapter.get_os_specific_image_list('test_image')
            image_details = image_list.get('test_image')           
            image_id = image_details.get('Image_ID')
            
            vm_instance = VM_Adapter('testvm', image_id, 2048, 20, 1)
            count = 0
            while count <= 4:  
                time.sleep(pow(2,count))
                count+=1
        except:
            print 'Connection not establised.'   
            raise               
        try:
            prev_vm_list = cloud_adapter.get_running_vm_list()
            assert('testvm' in prev_vm_list)
            vm_instance.suspend()
            count = 0
            while count <= 4:  
                time.sleep(pow(2,count))
                count+=1
            cur_vm_list = cloud_adapter.get_running_vm_list()
            assert('testvm' not in cur_vm_list)
            print 'Virtual Machine successfully suspended.'
            vm_instance.destroy()
            test_image.delete()
        except:
            print 'Virtual Machine not found.'   
            vm_instance.destroy()
            test_image.delete()
            raise   

    
    def test_pause(self):
        try:
            cloud_adapter = Cloud_Attributes()
            test_image = Image_Adapter(image_name='test_image', image_path='/home/openstack/Downloads/precise-server-cloudimg-amd64-disk1.img')
            image_list = cloud_adapter.get_os_specific_image_list('test_image')
            image_details = image_list.get('test_image')           
            image_id = image_details.get('Image_ID')
            
            vm_instance = VM_Adapter('testvm', image_id, 2048, 20, 1)
            count = 0
            while count <= 4:  
                time.sleep(pow(2,count))
                count+=1
        except:
            print 'Connection not establised.'   
            raise               
        try:
            prev_vm_list = cloud_adapter.get_running_vm_list()
            assert('testvm' in prev_vm_list)
            vm_instance.pause()
            count = 0
            while count <= 4:  
                time.sleep(pow(2,count))
                count+=1
            cur_vm_list = cloud_adapter.get_running_vm_list()
            assert('testvm' not in cur_vm_list)
            print 'Virtual Machine successfully paused.'
            vm_instance.destroy()
            test_image.delete()
        except:
            print 'Virtual Machine not found.'   
            vm_instance.destroy()
            test_image.delete()
            raise
    

    def test_get_ip(self):
        try:
            cloud_adapter = Cloud_Attributes()
            test_image = Image_Adapter(image_name='test_image', image_path='/home/openstack/Downloads/precise-server-cloudimg-amd64-disk1.img')
            image_list = cloud_adapter.get_os_specific_image_list('test_image')
            image_details = image_list.get('test_image')           
            image_id = image_details.get('Image_ID')
            
            vm_instance = VM_Adapter('testvm', image_id, 2048, 20, 1)
            count = 0
            while count <= 4:  
                time.sleep(pow(2,count))
                count+=1
        except:
            print 'Connection not establised.'   
            raise               
        try:
            vm_ip = vm_instance.get_ip()
            print '\n\nVirtual Machine IP :\n',vm_ip
            vm_instance.destroy()
            test_image.delete()
        except:
            print 'Virtual Machine not found.'   
            vm_instance.destroy()
            test_image.delete()
            raise
    

    def test_get_ram(self):
        try:
            cloud_adapter = Cloud_Attributes()
            test_image = Image_Adapter(image_name='test_image', image_path='/home/openstack/Downloads/precise-server-cloudimg-amd64-disk1.img')
            image_list = cloud_adapter.get_os_specific_image_list('test_image')
            image_details = image_list.get('test_image')           
            image_id = image_details.get('Image_ID')
            
            vm_instance = VM_Adapter('testvm', image_id, 2048, 20, 1)
            count = 0
            while count <= 4:  
                time.sleep(pow(2,count))
                count+=1
        except:
            print 'Connection not establised.'   
            raise               
        try:
            vm_ram = vm_instance.get_ram()
            print '\n\nVirtual Machine Ram Size :\n',vm_ram
            vm_instance.destroy()
            test_image.delete()
        except:
            print 'Virtual Machine not found.'   
            vm_instance.destroy()
            test_image.delete()
            raise


    def test_get_disk(self):
        try:
            cloud_adapter = Cloud_Attributes()
            test_image = Image_Adapter(image_name='test_image', image_path='/home/openstack/Downloads/precise-server-cloudimg-amd64-disk1.img')
            image_list = cloud_adapter.get_os_specific_image_list('test_image')
            image_details = image_list.get('test_image')           
            image_id = image_details.get('Image_ID')
            
            vm_instance = VM_Adapter('testvm', image_id, 2048, 20, 1)
            count = 0
            while count <= 4:  
                time.sleep(pow(2,count))
                count+=1
        except:
            print 'Connection not establised.'   
            raise               
        try:
            vm_disk = vm_instance.get_disk()
            print '\n\nVirtual Machine Disk Size :\n',vm_disk
            vm_instance.destroy()
            test_image.delete()
        except:
            print 'Virtual Machine not found.'   
            vm_instance.destroy()
            test_image.delete()
            raise


    def test_get_flavor(self):
        try:
            cloud_adapter = Cloud_Attributes()
            test_image = Image_Adapter(image_name='test_image', image_path='/home/openstack/Downloads/precise-server-cloudimg-amd64-disk1.img')
            image_list = cloud_adapter.get_os_specific_image_list('test_image')
            image_details = image_list.get('test_image')           
            image_id = image_details.get('Image_ID')
            
            vm_instance = VM_Adapter('testvm', image_id, 2048, 20, 1)
            count = 0
            while count <= 4:  
                time.sleep(pow(2,count))
                count+=1
        except:
            print 'Connection not establised.'   
            raise               
        try:
            vm_flavor = vm_instance.get_flavor()
            print '\n\nVirtual Machine Flavor Size :\n',vm_flavor
            vm_instance.destroy()
            test_image.delete()
        except:
            print 'Virtual Machine not found.'   
            vm_instance.destroy()
            test_image.delete()
            raise
           

    def test_change_ram(self):
        try:
            cloud_adapter = Cloud_Attributes()
            test_image = Image_Adapter(image_name='test_image', image_path='/home/openstack/Downloads/precise-server-cloudimg-amd64-disk1.img')
            image_list = cloud_adapter.get_os_specific_image_list('test_image')
            image_details = image_list.get('test_image')           
            image_id = image_details.get('Image_ID')
            
            vm_instance = VM_Adapter('testvm', image_id, 2048, 20, 1)
            count = 0
            while count <= 4:  
                time.sleep(pow(2,count))
                count+=1
        except:
            print 'Connection not establised.'   
            raise        
        try:
            prev_ram = vm_instance.get_ram()
            print '\nPrevious RAM SIZE',prev_ram
            
            vm_instance.change_ram(4096)
            count = 0
            while count <= 4:  
                time.sleep(pow(2,count))
                count+=1
            cur_ram = vm_instance.get_ram()
            print '\nCurrent RAM SIZE',cur_ram
        
            print 'Ram Size of the Virtual Machine changed successfully.'
            vm_instance.destroy()
            test_image.delete()
        except:
            print 'Virtual Machine not found.'   
            vm_instance.destroy()
            test_image.delete()
            raise
    
    
    def test_change_disk(self):
        try:
            cloud_adapter = Cloud_Attributes()
            test_image = Image_Adapter(image_name='test_image', image_path='/home/openstack/Downloads/precise-server-cloudimg-amd64-disk1.img')
            image_list = cloud_adapter.get_os_specific_image_list('test_image')
            image_details = image_list.get('test_image')           
            image_id = image_details.get('Image_ID')
            
            vm_instance = VM_Adapter('testvm', image_id, 2048, 20, 1)
            count = 0
            while count <= 4:  
                time.sleep(pow(2,count))
                count+=1
        except:
            print 'Connection not establised.'   
            raise        

        try:
            prev_disk = vm_instance.get_disk()
            print '\nPrevious DISK SIZE',prev_disk
            
            vm_instance.change_disk(40)
            count = 0
            while count <= 4:  
                time.sleep(pow(2,count))
                count+=1
            cur_disk = vm_instance.get_disk()
            print '\nCurrent DISK SIZE',cur_disk
        
            print 'Disk Size of the Virtual Machine changed successfully.'
            vm_instance.destroy()
            test_image.delete()
        except:
            print 'Virtual Machine not found.'   
            vm_instance.destroy()
            test_image.delete()
            raise
    
    
    def test_change_flavor(self):
        try:
            cloud_adapter = Cloud_Attributes()
            test_image = Image_Adapter(image_name='test_image', image_path='/home/openstack/Downloads/precise-server-cloudimg-amd64-disk1.img')
            image_list = cloud_adapter.get_os_specific_image_list('test_image')
            image_details = image_list.get('test_image')           
            image_id = image_details.get('Image_ID')
            
            vm_instance = VM_Adapter('testvm', image_id, 2048, 20, 1)
            count = 0
            while count <= 4:  
                time.sleep(pow(2,count))
                count+=1
        except:
            print 'Connection not establised.'   
            raise        
        try:
            prev_flavor_details = vm_instance.get_flavor()
            prev_flavor = prev_flavor_details.get('Flavor_Name')
            
            prev_flavor_list = cloud_adapter.get_flavor_list()
            assert(prev_flavor in prev_flavor_list)
            
            vm_instance.change_flavor(4096, 30)
            count = 0
            while count <= 4:  
                time.sleep(pow(2,count))
                count+=1

            cur_flavor_details = vm_instance.get_flavor()
            cur_flavor = cur_flavor_details.get('Flavor_Name')
            
            cur_flavor_list = cloud_adapter.get_flavor_list()
            assert(cur_flavor in cur_flavor_list)
            
            print 'Flavor Size of the Virtual Machine changed successfully.'
            vm_instance.destroy()
            test_image.delete()
        except:
            print 'Virtual Machine not found.'   
            vm_instance.destroy()
            test_image.delete()
            raise
    

    def test_restart_active(self):
        try:
            cloud_adapter = Cloud_Attributes()
            test_image = Image_Adapter(image_name='test_image', image_path='/home/openstack/Downloads/precise-server-cloudimg-amd64-disk1.img')
            image_list = cloud_adapter.get_os_specific_image_list('test_image')
            image_details = image_list.get('test_image')           
            image_id = image_details.get('Image_ID')
            
            vm_instance_active = VM_Adapter('testvm_active', image_id, 2048, 20, 1)
            count = 0
            while count <= 4:  
                time.sleep(pow(2,count))
                count+=1
        except:
            print 'Connection not establised.'   
            raise       

        try:
            prev_vm_list = cloud_adapter.get_running_vm_list()
            assert('testvm_active' in prev_vm_list)
            
            vm_instance_active.restart()
            count = 0
            while count <= 4:  
                time.sleep(pow(2,count))
                count+=1
            
            cur_vm_list = cloud_adapter.get_running_vm_list()
            assert('testvm_active' not in cur_vm_list)
            
            vm_instance_active.destroy()
            test_image.delete()
            print 'Virtual Machines restart successfully checked.'   
        except:
            print 'Virtual Machines not found.'   
            vm_instance_active.destroy()
            test_image.delete()
            raise


    def test_restart_pause(self):
        try:
            cloud_adapter = Cloud_Attributes()
            test_image = Image_Adapter(image_name='test_image', image_path='/home/openstack/Downloads/precise-server-cloudimg-amd64-disk1.img')
            image_list = cloud_adapter.get_os_specific_image_list('test_image')
            image_details = image_list.get('test_image')           
            image_id = image_details.get('Image_ID')
            
            vm_instance_pause = VM_Adapter('testvm_pause', image_id, 2048, 20, 1)
            count = 0
            while count <= 4:  
                time.sleep(pow(2,count))
                count+=1
        except:
            print 'Connection not establised.'   
            raise               
        try:
            vm_instance_pause.pause()
            count = 0
            while count <= 4:  
                time.sleep(pow(2,count))
                count+=1
                        
            prev_vm_list = cloud_adapter.get_running_vm_list()
            assert('testvm_pause' not in prev_vm_list)
            
            vm_instance_pause.restart()
            count = 0
            while count <= 4:  
                time.sleep(pow(2,count))
                count+=1
            
            cur_vm_list = cloud_adapter.get_running_vm_list()
            assert('testvm_pause' not in cur_vm_list)
            
            vm_instance_pause.destroy()
            test_image.delete()
            print 'Virtual Machines restart successfully checked.'   
        except:
            print 'Virtual Machines not found.'   
            vm_instance_pause.destroy()
            test_image.delete()
            raise

    
    def test_restart_suspend(self):
        try:
            cloud_adapter = Cloud_Attributes()
            test_image = Image_Adapter(image_name='test_image', image_path='/home/openstack/Downloads/precise-server-cloudimg-amd64-disk1.img')
            image_list = cloud_adapter.get_os_specific_image_list('test_image')
            image_details = image_list.get('test_image')           
            image_id = image_details.get('Image_ID')
            
            vm_instance_suspend = VM_Adapter('testvm_suspend', image_id, 2048, 20, 1)
            count = 0
            while count <= 4:  
                time.sleep(pow(2,count))
                count+=1
        except:
            print 'Connection not establised.'   
            raise               
        try:
            vm_instance_suspend.suspend()
            count = 0
            while count <= 4:  
                time.sleep(pow(2,count))
                count+=1
            
            prev_vm_list = cloud_adapter.get_running_vm_list()
            assert('testvm_suspend' not in prev_vm_list)
            
            vm_instance_suspend.restart()
            count = 0
            while count <= 4:  
                time.sleep(pow(2,count))
                count+=1
            
            cur_vm_list = cloud_adapter.get_running_vm_list()
            assert('testvm_suspend' not in cur_vm_list)
            
            vm_instance_suspend.destroy()
            test_image.delete()
            print 'Virtual Machine restart successfully checked.'   
        except:
            print 'Virtual Machine not found.'   
            vm_instance_suspend.destroy()
            test_image.delete()
            raise