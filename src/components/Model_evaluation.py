from src.components.Model_trainer import ModelTrainer
from src.logger.logging import logging
from src.exceptions.exception import CustomException
from sklearn.metrics import r2_score as sklearn_r2_score, mean_absolute_error as sklearn_mean_absolute_error
import os
import sys
import mlflow
import mlflow.sklearn
import numpy as np
import pickle
from src.utils.utils import load_object
from urllib.parse import urlparse

class Evaluate_Model:
    def __init__(self):
        logging.info("Model Evaluation has been started")

    def eval_metrics(self, Y_test, y_predict):
        logging.info("Loading the metrics....")
        # Calculate r2_score and mean_absolute_error here
        r2 = sklearn_r2_score(Y_test, y_predict)
        mae = sklearn_mean_absolute_error(Y_test, y_predict)
        return mae, r2

    def evaluate(self, test_arr):
        X_test, y_test = (test_arr[:, :-1], test_arr[:, -1])

        model_path = os.path.join("artifacts", "model.pkl")

        try:
            # Attempt to load the model using load_object
            model = load_object(model_path)
        except (FileNotFoundError, pickle.UnpicklingError) as e:
            # Handle potential errors during loading:
            # - File not found
            # - Corrupted pickle file
            logging.error(f"Error loading model: {e}")
            raise CustomException("Failed to load model") from e

        logging.info("Model has been loaded")

        tracking_url_type_store = urlparse(mlflow.get_tracking_uri()).scheme

        print(tracking_url_type_store)

        with mlflow.start_run():
            prediction = model.predict(X_test)

            # Use the calculated r2_score and mean_absolute_error here
            mae, r2 = self.eval_metrics(y_test, prediction)

            mlflow.log_metric("r2", r2)
            mlflow.log_metric("mae", mae)

            if tracking_url_type_store != "file":
                # Register the model if tracking URI is not a file store
                # Replace with your specific model registry logic
                mlflow.sklearn.log_model(model, "model", registered_model_name="ml_model")
            else:
                mlflow.sklearn.log_model(model, "model")
