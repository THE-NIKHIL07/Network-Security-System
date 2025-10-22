import sys

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.data_transformation import DataTransformation
from networksecurity.entity.config_entity import (DataIngestionConfig,TrainingPipelineConfig,
                                                  DataValidationConfig,DataTransformationConfig,
                                                  ModelTrainerConfig)
from networksecurity.components.model_trainer import ModelTrainer
if __name__=='__main__':
    try :
        training_pipeline_config=TrainingPipelineConfig()

        data_ingestion_config=DataIngestionConfig(training_pipeline_config)
        data_ingestion=DataIngestion(data_ingestion_config)

        logging.info("Initiate the data ingestion")
        data_ingestion_artifact=data_ingestion.initiate_data_ingestion()
        logging.info("Data Initiation completed")
        print(data_ingestion_artifact)

        datavalidationconfig=DataValidationConfig(training_pipeline_config)
        logging.info("Initiate the data validation")
        data_validation=DataValidation(data_ingestion_artifact,datavalidationconfig)
        logging.info("Data Validation completed")
        data_validation_artifact=data_validation.initiate_data_validation()
        print(data_validation_artifact)

        data_transformation_config=DataTransformationConfig(training_pipeline_config)
        logging.info("Data Transformation  Started")
        data_transformation=DataTransformation(data_validation_artifact,data_transformation_config)
        data_transformation_artifact=data_transformation.initiate_data_transformartion()
        print(data_transformation_artifact)
        logging.info("data tarnsformation completed")

        logging.info("Model Training started")
        model_trainer_config=ModelTrainerConfig(training_pipeline_config)
        model_trainer=ModelTrainer(model_trainer_config=model_trainer_config,data_transformation_artifact=data_transformation_artifact)
        model_trainer_artifact=model_trainer.initiate_model_trainer()

        logging.info("model training artifact created")
    except Exception as e:
        raise NetworkSecurityException(e,sys)