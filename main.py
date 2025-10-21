import sys

from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.components.data_validation import DataValidation

from networksecurity.entity.config_entity import DataIngestionConfig,TrainingPipelineConfig,DataValidationConfig
if __name__=='__main__':
    try :
        trainingpipelineconfig=TrainingPipelineConfig()
        dataingestionconfig=DataIngestionConfig(trainingpipelineconfig)
        data_ingestion=DataIngestion(dataingestionconfig)
        logging.info("Initiate the data ingestion")
        dataingestionartifact=data_ingestion.initiate_data_ingestion()
        logging.info("Data Initiation completed")
        print(dataingestionartifact)
        datavalidationconfig=DataValidationConfig(trainingpipelineconfig)
        logging.info("Initiate the data validation")
        data_validation=DataValidation(dataingestionartifact,datavalidationconfig)
        logging.info("Data Validation completed")
        data_validation_artifact=data_validation.initiate_data_validation()
        print(data_validation_artifact)



    except Exception as e:
        raise NetworkSecurityException(e,sys)