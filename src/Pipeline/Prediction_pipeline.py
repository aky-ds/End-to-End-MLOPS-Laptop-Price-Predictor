from src.exceptions.exception import CustomException
from src.logger.logging import logging
from src.utils.utils import load_object
from pathlib import Path
import pandas as pd
import os, sys

class Prediction:
    def __init__(self):
        logging.info("Predictions pipeline has been started.")

    def predict(self, features):
        try:
            model_path = os.path.join('artifacts', 'model.pkl')
            preprocessing_path = os.path.join('artifacts', 'preprocessing.pkl')
            model = load_object(model_path)
            preprocssor = load_object(preprocessing_path)

            # Select all features by index (assuming features are numerical)
         # Select all columns

            features = preprocssor.transform(features)
            predictions = model.predict(features)
            return predictions
        except Exception as e:
            raise CustomException(e, sys)

class Custom_Data:
    def __init__(self, brand: str, processor_brand: str, processor_name: str, processor_gnrtn: int,
                 ram_gb: int, ram_type: str, ssd: int, hdd: int, os, os_bit: str,
                 graphic_card_gb: str, weight: str, warranty: int, Touchscreen: str,
                 msoffice: str, rating: str, Number_of_Ratings: int, Number_of_Reviews: int):
        self.brand = brand
        self.processor_brand = processor_brand
        self.processor_name = processor_name
        self.processor_gnrtn = processor_gnrtn
        self.ram_gb = ram_gb
        self.ram_type = ram_type
        self.ssd = ssd
        self.hdd = hdd
        self.os = os
        self.os_bit = os_bit
        self.graphic_card_gb = graphic_card_gb
        self.weight = weight
        self.warranty = warranty
        self.Touchscreen = Touchscreen
        self.msoffice = msoffice
        self.rating = rating
        self.Number_of_Ratings = Number_of_Ratings
        self.Number_of_Reviews = Number_of_Reviews

    def get_data_as_dataframe(self):
        try:
            logging.info("Getting data as dataframe")
            dict_data = {
                "brand": [self.brand],
                "processor_brand": [self.processor_brand],
                "processor_gnrtn": [self.processor_gnrtn],
                "processor_name": [self.processor_name],
                "ram_gb": [self.ram_gb],
                "ram_type": [self.ram_type],
                "ssd": [self.ssd],
                "hdd": [self.hdd],
                "os": [self.os],
                "os_bit": [self.os_bit],
                "graphic_card_gb": [self.graphic_card_gb],
                "weight": [self.weight],
                "warranty": [self.warranty],
                "Touchscreen": [self.Touchscreen],
                "msoffice": [self.msoffice],
                "rating": [self.rating],
                "Number of Ratings": [self.Number_of_Ratings],
                "Number of Reviews": [self.Number_of_Reviews]
            }

            df = pd.DataFrame(dict_data)
            logging.info("DataFrame has been created")
            return df # Reshape to single row for prediction
        except Exception as e:
            raise CustomException(e, sys)