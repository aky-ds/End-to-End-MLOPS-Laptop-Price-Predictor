from src.components.Data_ingestion import DataIngestion
from src.components.Data_Transformation import DataTransformation
from src.components.Model_trainer import ModelTrainer
from src.components.Model_evaluation import Evaluate_Model


obj=DataIngestion()
train_data,test_data=obj.instatiate_dataconfig()

data_transform=DataTransformation()

train_arr,test_arr=data_transform.instantiate_preprocessing(train_data,test_data)

modeltrain=ModelTrainer()

modeltrain.InstantiateModel(train_arr,test_arr)

model_evaluate=Evaluate_Model()

model_evaluate.evaluate(test_arr)