import os
import sys
import json
import logging
from pathlib import Path
from typing import List, Dict

import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
from dotenv import load_dotenv
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging 
# Load .env
load_dotenv()



POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = int(os.getenv("POSTGRES_PORT", 5432))
POSTGRES_DB = os.getenv("POSTGRES_DB", "NetworkSecurity")
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "")


class NetworkDataExtract:
    """ETL class for PostgreSQL, mimicking MongoDB Atlas workflow."""

    def __init__(self):
        try:
            self.conn = psycopg2.connect(
                host=POSTGRES_HOST,
                port=POSTGRES_PORT,
                database=POSTGRES_DB,
                user=POSTGRES_USER,
                password=POSTGRES_PASSWORD
            )
            self.cursor = self.conn.cursor()
            logging.info(" Connected to PostgreSQL successfully.")
        except Exception as e:
            logging.error(f" Connection failed: {e}")
            sys.exit(1)

    def csv_to_json_convertor(self, file_path: str) -> List[Dict]:
        """Convert CSV to list of dictionaries"""
        try:
            data = pd.read_csv(file_path)
            data.reset_index(drop=True, inplace=True)
            records = data.to_dict(orient="records")
            logging.info(" CSV converted to JSON-like list of dictionaries.")
            return records
        except Exception as e:
            logging.error(f" CSV conversion failed: {e}")
            raise

    def ensure_table_exists(self, table_name: str):
        """Create table if it doesn't exist, with JSONB column."""
        create_sql = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            id SERIAL PRIMARY KEY,
            data JSONB
        );
        """
        try:
            self.cursor.execute(create_sql)
            self.conn.commit()
            logging.info(f" Ensured table '{table_name}' exists.")
        except Exception as e:
            self.conn.rollback()
            logging.error(f" Failed to ensure table exists: {e}")
            raise

    def insert_data_postgres(self, records: List[Dict], table_name: str) -> int:
        """Insert JSON data into PostgreSQL table, same as MongoDB workflow."""
        try:
            values = [(json.dumps(record),) for record in records]
            sql = f"INSERT INTO {table_name} (data) VALUES %s;"
            execute_values(self.cursor, sql, values)
            self.conn.commit()
            logging.info(f" Inserted {len(records)} rows into '{table_name}'.")
            return len(records)
        except Exception as e:
            self.conn.rollback()
            logging.error(f" Insert failed: {e}")
            raise
        finally:
            self.cursor.close()
            self.conn.close()


if __name__ == "__main__":
    FILE_PATH = Path(__file__).parent / "Network_Data" / "phisingData.csv"
    DATABASE_TABLE = "phishing_data"

    networkobj = NetworkDataExtract()
    networkobj.ensure_table_exists(DATABASE_TABLE)
    records = networkobj.csv_to_json_convertor(str(FILE_PATH))
    no_of_records = networkobj.insert_data_postgres(records, DATABASE_TABLE)
    logging.info(f"Total records inserted: {no_of_records}")
