import unittest
from Cloud_Attributes import Cloud_Attributes
from Image_Adapter import Image_Adapter
from Main import Main

class TddInPython(unittest.TestCase):

    def test_create(self):
        try:
            cloud_adapter = Cloud_Attributes()

            prev_image_list = cloud_adapter.get_image_list()
            assert('test_image' not in prev_image_list)
            test_image = Image_Adapter(image_name='test_image', image_path='/home/openstack/Downloads/precise-server-cloudimg-amd64-disk1.img')
            
            cur_image_list = cloud_adapter.get_image_list()
            assert('test_image' in cur_image_list)
            print 'Image Instance Created successfully.'
        
            test_image.delete()
        except:
            print 'Image Instance Creation failed.'   
            raise	

    
    def test_destroy(self):
        try:
            cloud_adapter = Cloud_Attributes()
            test_image = Image_Adapter('test_image', '/home/openstack/Downloads/precise-server-cloudimg-amd64-disk1.img')
            
        except:
            print 'Connection not Establised.'   
            raise               

        try:
            prev_image_list = cloud_adapter.get_image_list()
            assert('test_image' in prev_image_list)
            
            test_image.delete()
            
            cur_image_list = cloud_adapter.get_image_list()
            assert('test_image' not in cur_image_list)
            
            print 'Image Instance successfully Destroyed.'  
        except:
            print 'Image Instance not found.'   
            test_image.delete()
            raise