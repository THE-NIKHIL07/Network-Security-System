import os
import sys
import numpy as np
import pandas as pd

'''
defining common constant variable for training pipeline
'''
TARGET_COLUMN="Result"
PIPELINE_NAME:str="NetworkSecurity"
ARTIFACT_DIR:str="Artifacts"
FILE_NAME:str="phisingData.csv"
TRAIN_FILE_NAME:str="train.csv"
TEST_SPLIT_NAME:str="test.csv"





"""
Data Ingestion Constants for PostgreSQL ETL
"""

# Table & Database
DATA_INGESTION_TABLE_NAME: str = "phishing_data"   # PostgreSQL table name
DATA_INGESTION_SCHEMA_NAME: str = "public"         # Schema name (default)

# Directories
DATA_INGESTION_DIR_NAME: str = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR: str = "feature_store"
DATA_INGESTION_INGESTION_DIR: str = "ingested"

# Train-test split
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO: float = 0.2
