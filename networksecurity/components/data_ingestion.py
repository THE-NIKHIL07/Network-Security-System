from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import DataIngestionConfig
from networksecurity.entity.artifact_entity import DataIngestionArtifact

import os
import sys
import pandas as pd
import psycopg2
from psycopg2.extras import RealDictCursor
from typing import List
from sklearn.model_selection import train_test_split
from dotenv import load_dotenv

load_dotenv()

POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = int(os.getenv("POSTGRES_PORT", 5432))
POSTGRES_DB = os.getenv("POSTGRES_DB", "NetworkSecurity")
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "")


class DataIngestion:
    def __init__(self, data_ingestion_config: DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config

            # Connect to PostgreSQL
            self.conn = psycopg2.connect(
                host=POSTGRES_HOST,
                port=POSTGRES_PORT,
                database=POSTGRES_DB,
                user=POSTGRES_USER,
                password=POSTGRES_PASSWORD,
                cursor_factory=RealDictCursor
            )
            self.cursor = self.conn.cursor()
            logging.info(" Connected to PostgreSQL successfully.")
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def export_table_as_dataframe(self) -> pd.DataFrame:
        """Read JSON data from PostgreSQL table and return as DataFrame"""
        try:
            table = self.data_ingestion_config.table_name
            schema = self.data_ingestion_config.schema_name

            query = f"SELECT data FROM {schema}.{table};"
            self.cursor.execute(query)
            rows = self.cursor.fetchall()

            dataframe = pd.json_normalize([row['data'] for row in rows])
            logging.info(" Exported PostgreSQL table to DataFrame successfully.")
            return dataframe
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def export_data_into_feature_store(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        """Save the full dataframe to feature store CSV"""
        try:
            feature_store_file_path = self.data_ingestion_config.feature_store_file_path
            os.makedirs(os.path.dirname(feature_store_file_path), exist_ok=True)
            dataframe.to_csv(feature_store_file_path, index=False, header=True)
            logging.info(" Exported data into feature store successfully.")
            return dataframe
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def split_data_as_train_test(self, dataframe: pd.DataFrame):
        """Split the dataframe into train and test CSV files"""
        try:
            train_set, test_set = train_test_split(
                dataframe, test_size=self.data_ingestion_config.train_test_split_ratio
            )
            logging.info(" Performed train-test split on the dataframe.")

            # Ensure directories exist
            os.makedirs(os.path.dirname(self.data_ingestion_config.training_file_path), exist_ok=True)
            os.makedirs(os.path.dirname(self.data_ingestion_config.testing_file_path), exist_ok=True)

            # Save CSVs
            train_set.to_csv(self.data_ingestion_config.training_file_path, index=False, header=True)
            test_set.to_csv(self.data_ingestion_config.testing_file_path, index=False, header=True)
            logging.info(" Exported train and test CSV files successfully.")

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        """Full pipeline: PostgreSQL table -> feature store -> train/test CSV"""
        try:
            dataframe = self.export_table_as_dataframe()
            dataframe = self.export_data_into_feature_store(dataframe)
            self.split_data_as_train_test(dataframe)

            artifact = DataIngestionArtifact(
                trained_file_path=self.data_ingestion_config.training_file_path,
                test_file_path=self.data_ingestion_config.testing_file_path
            )
            return artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        finally:
            self.cursor.close()
            self.conn.close()
