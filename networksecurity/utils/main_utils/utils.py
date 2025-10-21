import os,sys
import numpy as np
import dill
import pickle
import yaml

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging


def read_yaml_file(filepath:str)-> dict :
    try:
        with open(filepath,"rb") as yaml_file :
            return yaml.safe_load(yaml_file)
    except Exception as e :
        raise NetworkSecurityException(e,sys) 
    
def write_yaml_file(file_path:str,content:object,replace:bool=False)->None:
        try:
             if replace :
                  if os.path.exists(file_path):
                       os.remove(file_path)
                  os.makedirs(os.path.dirname(file_path),exist_ok=True)
                  with open(file_path,"w") as file :
                       yaml.dump(content,file)
        except Exception as e:
             raise NetworkSecurityException(e,sys) 

def save_numpy_array_data(filepath:str,array:np.array):
     try:
          dir_path=os.path.dirname(filepath)
          os.makedirs(dir_path,exist_ok=True)

          with open(filepath,"wb") as file :
                np.save(file,array)
     except Exception as e :
          raise NetworkSecurityException(e,sys)           

def save_object(file_path:str,obj:object)->None :
     try:
          logging.info("Entered the save_object method of MainUtils class")
          os.makedirs(os.path.dirname(file_path),exist_ok=True)
          with open(file_path,"wb") as file :
               pickle.dump(obj,file)
          logging.info("Exited the save_ovject method of mainutils class")
     except Exception as e :                                       
        raise NetworkSecurityException(e,sys)