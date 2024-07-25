from src.components.Data_ingestion import DataIngestion
from src.components.Data_Transformation import DataTransformation
from src.components.Model_trainer import ModelTrainer
from src.components.Model_evaluation import Evaluate_Model
from src.logger.logging import logging
from src.exceptions.exception import CustomException
import sys
obj=DataIngestion()
train_data,test_data=obj.instatiate_dataconfig()

data_transform=DataTransformation()

train_arr,test_arr=data_transform.instantiate_preprocessing(train_data,test_data)

modeltrain=ModelTrainer()

modeltrain.InstantiateModel(train_arr,test_arr)

model_evaluate=Evaluate_Model()

model_evaluate.evaluate(test_arr)


class Training_Pipeline:
    def start_data_ingestion(self):
        try:
            data_ingestion=DataIngestion()
            train_path,test_path=data_ingestion.instatiate_dataconfig()
            return train_path,test_path
        except Exception as e:
            raise CustomException(e,sys)
    def start_data_transform(self,train_path,test_path):
        try:
            data_transform=DataTransformation()
            train_arr,test_arr=data_transform.instantiate_preprocessing(train_path,test_path)
            return train_arr,test_arr
        except Exception as e:
            raise CustomException(e,sys)
    
    def start_model_trainer(self,train_err,test_arr):
        try:
            model_trainer=ModelTrainer()
            X_test,y_test,best_model=model_trainer.InstantiateModel()
            return best_model
        except Exception as e:
            raise CustomException(e,sys)
    def start_training(self):
        try:
            train_path,test_path=self.start_data_ingestion()
            train_arr,test_arr=self.start_data_transform(train_path,test_path)
            self.start_model_trainer(train_arr,test_arr)
        except Exception as e:
            raise CustomException(e,sys)
    
    
