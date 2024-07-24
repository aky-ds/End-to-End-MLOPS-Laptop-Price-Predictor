import os
from pathlib import Path
from src.components.Data_Transformation import DataTransformation
from src.logger.logging import logging
from src.components.Data_ingestion import DataIngestion
from src.exceptions.exception import CustomException
from dataclasses import dataclass
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, AdaBoostRegressor
from sklearn.svm import LinearSVR
from sklearn.neighbors import KNeighborsRegressor
import sys
from src.utils.utils import evaluate_model, save_obj

@dataclass
class ModelTrainerConfig:
    model_train_configer = os.path.join('artifacts', 'model.pkl')

class ModelTrainer:
    def __init__(self):
        logging.info('Initializing the trained model')
        self.model_train_config = ModelTrainerConfig()
        
    def InstantiateModel(self, train_arr, test_arr):
        try:
            logging.info('Data splitting has been started')
            X_train, X_test, Y_train, Y_test = train_arr[:, :-1], test_arr[:, :-1], train_arr[:, -1], test_arr[:, -1]
            logging.info('Loading the models')
            models = {
                'RandomForestRegressor': RandomForestRegressor(),
                'AdaBoostRegressor': AdaBoostRegressor(),
                'GradientBoostRegressor': GradientBoostingRegressor(),
                'KNNRegressor': KNeighborsRegressor(),
                'SVCRegressor': LinearSVR(),
                'LinearRegressor': LinearRegression()
            }
            
            logging.info('Making the models report')
            model_report = evaluate_model(X_train, Y_train, X_test, Y_test, models)
            logging.info('Model reporting has been prepared')
            
            best_model_score = max(sorted(model_report.values()))
            best_model_name = list(model_report.keys())[list(model_report.values()).index(best_model_score)]
            best_model = models[best_model_name]
            
            logging.info(f'Best model is {best_model} with a score of {best_model_score}')
            
            save_obj(self.model_train_config.model_train_configer, best_model)
            logging.info(f'Model saved to {self.model_train_config.model_train_configer}')
            
            return X_test, Y_test, best_model
        except Exception as e:
            logging.error(f'Error during model training: {e}')
            raise CustomException(e, sys)

if __name__ == "__main__":
    obj = DataIngestion()
    train_data, test_data = obj.instatiate_dataconfig()

    data_transform = DataTransformation()
    train_arr, test_arr = data_transform.instantiate_preprocessing(train_data, test_data)

    modeltrain = ModelTrainer()
    modeltrain.InstantiateModel(train_arr, test_arr)
