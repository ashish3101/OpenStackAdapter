import os
import time
import glanceclient
import logging

import keystoneclient.v2_0.client as ksclient
from credentials import get_keystone_creds

import novaclient.v1_1.client as nvclient
from credentials import get_nova_creds


class Image_Adapter(object):

    """docstring for Image_Adapter"""
            
    def __init__(self, image_name, image_path):           

        """
        Constructor to create a Connection and an Image Instance.
    
        :param image_name: The name of the image to be created.
        :param image_path: The path of the image for creation.
        """

        logging.basicConfig(filename='openstack.log', level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s' , datefmt='%m/%d/%Y %I:%M:%S %p')
        
        logging.info('Establishing Connection.')

        # Establishing Connections --------------------             
        try:
            # Connections with keystoneClient(identity API) --------------------
            creds = get_keystone_creds()
            self.keystone = ksclient.Client(**creds)
  
            # Connections with novaClient(compute API) --------------------    
            creds = get_nova_creds()
            self.nova = nvclient.Client(**creds)   
        except:
            logging.error('Connection not Established.')
            raise     

        # Creating IMAGE instance --------------------             
        try:
            logging.info('Creating Image.')
            self.is_image_present = False
            image = self.create(image_name, image_path)  
            self.image = image
        except:
            logging.error('Image not Created.')
            main.delete()
            raise     


    # Create Image --------------------
    def create(self, image_name, image_path):

        """
        Create an Image.
    
        :param image_name: The name of the image to be created.
        :param image_path: The path of the image for creation.
        :rtype: :object: Image Object.
        """

        try:
            logging.info('Waiting for Image to Create.')
           
            endpoint = self.keystone.service_catalog.url_for(service_type='image', endpoint_type='publicURL')
            
            image_config = glanceclient.Client(version='1', endpoint=endpoint, token=self.keystone.auth_token)
            
            with open(image_path, 'rb') as fimage:
                image = image_config.images.create(name=image_name, is_public=True, disk_format="qcow2", container_format="bare", data=fimage)
            self.is_image_present = True
            return image
        except:
            logging.error('Image not Created.')
            raise

    
    # Delete Image --------------------  
    def delete(self):

        """
        Delete an Image.
        
        :rtype: NULL
        """

        try:
            assert(self.is_image_present)
        except:
            logging.warning('Image does not exist.')
            raise

        try:
            self.image.delete()   
            logging.info('Waiting for Image to Terminate....')
            logging.info('Terminated Image Name is %s', self.image.name)
            logging.info('Terminated Image ID is %s', self.image.id)
            del self.image
            self.is_image_present = False
            logging.info('Image has now been Terminated.')
        except:
            logging.error('Image not Terminated.')  
            raise  