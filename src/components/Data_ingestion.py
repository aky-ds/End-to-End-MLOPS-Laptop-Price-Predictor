import os
from pathlib import Path
from src.logger.logging import logging
from src.exceptions.exception import CustomException
from dataclasses import dataclass
import pandas as pd
from sklearn.model_selection import train_test_split
import sys
@dataclass

class DataIngestionConfig:
    train_data_path=os.path.join('artifacts', 'train_data.csv')
    test_data_path=os.path.join('artifacts', 'test_data.csv')
    raw_data_path=os.path.join('artifacts', 'raw_data.csv')
    
class DataIngestion:
    logging.info('Data Ingestion have been started')
    def __init__(self):
        self.dataconfig = DataIngestionConfig()
    def instatiate_dataconfig(self):
        try:
         logging.info('Data Divisin have been instatiated')
         df=pd.read_csv('C:/Users/admin/Desktop/Data.csv')
         os.makedirs(os.path.dirname(os.path.join(self.dataconfig.raw_data_path)), exist_ok=True)
        
         df.to_csv(self.dataconfig.raw_data_path,index=False)
        
         logging.info('Raw Data have been created')
        
         train_data,test_data = train_test_split(df,test_size=0.3)
        
         train_data.to_csv(self.dataconfig.train_data_path,index=False)
        
         logging.info('Training Data have been created')
        
         test_data.to_csv(self.dataconfig.test_data_path,index=False)
        
         logging.info('Test Data have been created')
        
         return self.dataconfig.train_data_path,self.dataconfig.test_data_path
        except Exception as e:
            raise CustomException(e,sys)
    
    
if __name__ == '__main__':
    Dataingest=DataIngestion()
    Dataingest.instatiate_dataconfig()