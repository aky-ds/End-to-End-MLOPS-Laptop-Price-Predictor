import os
from pathlib import Path
from src.components.Data_ingestion import DataIngestion
from src.logger.logging import logging
from src.exceptions.exception import CustomException
from src.utils.utils import save_obj
from dataclasses import dataclass
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
import pandas as pd
import numpy as np
import sys

@dataclass
class DataTransformationConfig:
    preprocessing_file = os.path.join('artifacts', 'preprocessing.pkl')

class DataTransformation:
    logging = logging.info("Data transformation has been started")
    
    def __init__(self):
        self.config = DataTransformationConfig()

    def preprocessing(self):
        try: 
            num_cols = ['processor_gnrtn', 'ram_gb', 'ssd', 'hdd', 'graphic_card_gb', 'warranty', 'Number of Ratings', 'Number of Reviews']
            cat_cols = ['brand', 'processor_brand', 'processor_name', 'ram_type', 'os', 'os_bit', 'weight', 'Touchscreen', 'msoffice', 'rating']
            
            logging.info('Creating a Pipeline')
            
            num_pipeline = Pipeline(
                steps=[
                    ('Imputer', SimpleImputer(strategy='median')),
                    ('StandardScaler', StandardScaler())
                ]
            )
            
            cat_pipeline = Pipeline(
                steps=[
                    ('Imputer', SimpleImputer(strategy='most_frequent')),
                    ('OneHotEncoder', OneHotEncoder(handle_unknown='ignore'))
                ]
            )
            
            preprocessing_pipeline = ColumnTransformer(
                [
                    ('num_pipeline', num_pipeline, num_cols),
                    ('cat_pipeline', cat_pipeline, cat_cols)
                ]
            )
            
            return preprocessing_pipeline
        except Exception as e:
            raise CustomException(e, sys)

    def instantiate_preprocessing(self, train_data_path, test_data_path):
        try:
            logging.info('Data preprocessing has been started')
            
            train_data = pd.read_csv(train_data_path)
            test_data = pd.read_csv(test_data_path)
            
            train_data.drop('Unnamed: 0',axis=1,inplace=True)
            
            test_data.drop('Unnamed: 0',axis=1,inplace=True)
            
            logging.info('Splitting the data into training and testing dependent and independent data')
            
            dropped_column = ['Price']
            
            train_data_input = train_data.drop(dropped_column, axis=1)
            train_data_output = train_data[dropped_column]
            
            test_data_input = test_data.drop(dropped_column, axis=1)
            test_data_output = test_data[dropped_column]
            
            logging.info('Loading the preprocessing object...')
            
            preprocessing_obj = self.preprocessing()
            
            train_data_input_array = preprocessing_obj.fit_transform(train_data_input)
            test_data_input_array = preprocessing_obj.transform(test_data_input)
            
            logging.info('Data preprocessing has been applied')
            
            train_arr = np.c_[train_data_input_array, np.array(train_data_output)]
            test_arr = np.c_[test_data_input_array, np.array(test_data_output)]
            
            save_obj(self.config.preprocessing_file, preprocessing_obj)
            
            logging.info('Preprocessing object has been saved')
            
            return train_arr, test_arr
        except Exception as e:
            raise CustomException(e, sys)

if __name__ == '__main__':
    data_ingest = DataIngestion()
    training_data, test_data = data_ingest.instatiate_dataconfig()
    data_preprocess = DataTransformation()
    data_preprocess.instantiate_preprocessing(training_data, test_data)
