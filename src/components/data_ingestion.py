import pandas as pd
import os, sys
import logging
from ucimlrepo import fetch_ucirepo 
from sklearn.model_selection import train_test_split
from dataclasses import dataclass

@dataclass
class DataIngestionConfig:
    train_data_path: str=os.path.join('artifacts',"train.csv")
    test_data_path: str=os.path.join('artifacts',"test.csv")
    raw_data_path: str=os.path.join('artifacts',"data.csv")

class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()

    def initiate_data_ingestion(self):
        logging.info("Entered the data ingestion method or component:")
        try:
            # Fetch the dataset from the UCI ML repository
            energy_efficiency = fetch_ucirepo(id=242)

            # Extract features (X) and targets (y)
            X = energy_efficiency.data.features
            y = energy_efficiency.data.targets

            # Combine X and y into a single DataFrame for easier handling
            df = pd.concat([X, y], axis=1)
            logging.info("Fetched and combined dataset as dataframe")

            # Create directories if they do not exist
            os.makedirs(self.ingestion_config.train_data_path, exist_ok=True)

            # Save the full dataset to an Excel file
            df.to_excel(self.ingestion_config.raw_data_path, index=False, header=True)

            # Split the dataset into training and testing sets
            train_set, test_set = train_test_split(df, test_size=0.2, random_state=42)

            # Save the training and testing sets to separate Excel files
            train_set.to_excel(self.ingestion_config.train_data_path, index=False, header=True)
            test_set.to_excel(self.ingestion_config.test_data_path, index=False, header=True)

            logging.info("Ingestion of data is completed")

        except Exception as e:
            raise CustomException(e, sys)

# Example of how CustomException might be defined
class CustomException(Exception):
    def __init__(self, message, original_exception):
        super().__init__(message)
        self.original_exception = original_exception

    def __str__(self):
        return f'{self.message} (caused by {self.original_exception})'

# You would need to define the DataIngestionConfig class as well if it isn't defined
