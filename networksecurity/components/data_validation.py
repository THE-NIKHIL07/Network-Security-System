from networksecurity.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from networksecurity.entity.config_entity import DataValidationConfig
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.constant.training_pipeline import SCHEMA_FILE_PATH
from networksecurity.logging.logger import logging
from networksecurity.utils.main_utils.utils import read_yaml_file, write_yaml_file
from scipy.stats import ks_2samp
import pandas as pd
import os, sys


class DataValidation:
    def __init__(self, data_ingestion_artifact: DataIngestionArtifact,
                 data_validation_config: DataValidationConfig):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self.schema_config = read_yaml_file(SCHEMA_FILE_PATH)

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    @staticmethod
    def read_data(file_path: str) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def validate_no_columns(self, df: pd.DataFrame) -> bool:
        try:
            no_of_columns = len(self.schema_config['columns'])
            logging.info(f"Required No of columns: {no_of_columns}")
            logging.info(f"DataFrame has columns: {len(df.columns)}")
            return len(df.columns) == no_of_columns
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def validate_numerical_columns(self, df: pd.DataFrame) -> bool:
        try:
            numerical_cols = self.schema_config["numerical_columns"]
            missing_cols = [col for col in numerical_cols if col not in df.columns]
            if missing_cols:
                logging.error(f"Missing numerical columns: {missing_cols}")
                return False
            return True
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def detect_dataset_drift(self, base_df, current_df, threshold=0.05) -> bool:
        try:
            status = True
            report = {}
            for column in base_df.columns:
                d1 = base_df[column]
                d2 = current_df[column]
                is_same_dist = ks_2samp(d1, d2)

                drift_found = is_same_dist.pvalue < threshold
                if drift_found:
                    status = False

                report.update({
                    column: {
                        "p_value": float(is_same_dist.pvalue),
                        "drift_detected": drift_found
                    }
                })

            drift_report_file_path = self.data_validation_config.drift_report_file_path
            dir_path = os.path.dirname(drift_report_file_path)
            os.makedirs(dir_path, exist_ok=True)

            write_yaml_file(file_path=drift_report_file_path, content=report)

            return status
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def initiate_data_validation(self) -> DataValidationArtifact:
        try:
            train_file_path = self.data_ingestion_artifact.trained_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path

            train_df = self.read_data(train_file_path)
            test_df = self.read_data(test_file_path)

            error_message = ""

            if not self.validate_no_columns(train_df):
                error_message += "Train DF does not contain all required columns.\n"
            if not self.validate_no_columns(test_df):
                error_message += "Test DF does not contain all required columns.\n"

            if not self.validate_numerical_columns(train_df):
                error_message += "Train DF missing required numerical columns.\n"
            if not self.validate_numerical_columns(test_df):
                error_message += "Test DF missing required numerical columns.\n"

            if error_message:
                raise Exception(error_message)

            logging.info("Data validation completed successfully.")

            # check drift
            status = self.detect_dataset_drift(base_df=train_df, current_df=test_df)

            # save validated train and test data
            os.makedirs(os.path.dirname(self.data_validation_config.valid_train_file_path), exist_ok=True)
            train_df.to_csv(self.data_validation_config.valid_train_file_path, index=False, header=True)

            os.makedirs(os.path.dirname(self.data_validation_config.valid_test_file_path), exist_ok=True)
            test_df.to_csv(self.data_validation_config.valid_test_file_path, index=False, header=True)

            data_validation_artifact = DataValidationArtifact(
                validation_status=status,
                valid_train_file_path=self.data_ingestion_artifact.trained_file_path,
                valid_test_file_path=self.data_ingestion_artifact.test_file_path,
                invalid_train_file_path=None,
                invalid_test_file_path=None,
                drift_report_file_path=self.data_validation_config.drift_report_file_path
            )

            return data_validation_artifact

        except Exception as e:
            raise NetworkSecurityException(e, sys)
