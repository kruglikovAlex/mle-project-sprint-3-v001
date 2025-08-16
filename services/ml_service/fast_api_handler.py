"""Класс FastApiHandler, который обрабатывает запросы API."""
import os
import mlflow
from dotenv import load_dotenv
import pandas as pd
import numpy as np
from catboost import CatBoostRegressor
import joblib

class FastApiHandler:
    """Класс FastApiHandler, который обрабатывает запрос и возвращает предсказание."""

    def __init__(self):
        """Инициализация переменных класса."""
        
        self.TRACKING_SERVER_HOST = "127.0.0.1"
        self.TRACKING_SERVER_PORT = 5000
            
        # типы параметров запроса для проверки
        self.param_types = {
            "user_id": str,
            "model_params": dict
        }
        
        # необходимые параметры для предсказаний стоимости квартир
        self.required_model_params = [
            'build_type_floors_low_rise','building_area_mean','building_price_mean', 'ceiling_height.1', 'dist_origin_dest', 
            'living_area.1', 'num_fg__KBinsDiscretizer__kitchen_area', 'num_fg__Polynomial__building_type_int kitchen_area^2', 'num_fg__Polynomial__ceiling_height total_area', 
            'num_fg__Polynomial__ceiling_height total_area kitchen_area', 'num_fg__Polynomial__ceiling_height total_area^2', 'num_fg__Polynomial__dist_origin_dest', 
            'num_fg__Polynomial__dist_origin_dest distance_to_metro_fast^2', 'num_fg__Polynomial__dist_origin_dest^2 distance_to_metro_fast', 'num_fg__Polynomial__dist_origin_dest^2 kitchen_area', 
            'num_fg__Polynomial__dist_origin_dest^2 living_area', 'num_fg__Polynomial__dist_origin_dest^2 total_area', 'num_fg__Polynomial__floor building_type_int distance_to_metro_fast', 
            'num_fg__Polynomial__floor building_type_int^2', 'num_fg__Polynomial__floor ceiling_height total_area', 'num_fg__Polynomial__floor total_area^2', 'num_fg__Polynomial__living_area^2', 
            'num_fg__Polynomial__rooms^2', 'num_fg__Polynomial__total_area living_area^2', 'num_fg__Polynomial__total_area^2 kitchen_area', 'num_fg__Polynomial__total_area^2 living_area', 
            'total_area.1', 'total_area_old'
            ]
        
        self.model_path = 'runs:/016a8bed9c27468c869d774ea10d768b/models' #"/models/catboost_churn_model.bin"

        self.load_cost_estimate(model_path=self.model_path)

    def load_cost_estimate(self, model_path: str):
        """Загружаем обученную модель предсказания кредитного рейтинга.
        
            Args:
            model_path (str): Путь до модели.
        """
        try:           
            # подгружаем .env
            load_dotenv()

            os.environ["MLFLOW_S3_ENDPOINT_URL"] = "https://storage.yandexcloud.net" # ваш код здесь
            os.environ['AWS_ACCESS_KEY_ID'] = os.getenv('AWS_ACCESS_KEY_ID')
            os.environ["AWS_SECRET_ACCESS_KEY"] = os.getenv('AWS_SECRET_ACCESS_KEY')
            
            mlflow.set_tracking_uri('http://127.0.0.1:5000')
            mlflow.set_tracking_uri(f"http://{self.TRACKING_SERVER_HOST}:{self.TRACKING_SERVER_PORT}")
            mlflow.set_registry_uri(f"http://{self.TRACKING_SERVER_HOST}:{self.TRACKING_SERVER_PORT}")
            print('TRACKING_SERVER_HOST: ', self.TRACKING_SERVER_HOST)
            print("os.getenv('AWS_ACCESS_KEY_ID'):", os.getenv('AWS_ACCESS_KEY_ID'))
            
            # Load model as a PyFuncModel.
            try:
                self.model = mlflow.pyfunc.load_model(model_path)
            except:
                print('Failed to load model: API request to http://127.0.0.1:5000/api/2.0/mlflow/runs/get')
                self.model = ""
            if type(self.model) != mlflow.pyfunc.PyFuncModel:
                print('Пробуем использовать заранее скачаную модель')
                if os.path.exists('models/best_hparam_model_CBR.pkl'):
                    with open('models/best_hparam_model_CBR.pkl', 'rb') as fd:
                        self.model = joblib.load(fd)
                        print('Модель:', type(self.model))
                else:
                    print('Модель не найдена')
                    self.model = joblib.load('models/best_hparam_model_CBR.pkl')
                    print('Модель:', type(self.model))
        except Exception as e:
            print(f"Failed to load model: {e}")

    def cost_estimate_predict(self, model_params: dict) -> float:
        """Предсказываем стоимость квартир.
        
        Args:
            model_params (dict): Параметры для модели.
        
        Returns:
            float — стоимость квартиры
        """
        X = pd.DataFrame.from_dict(model_params, orient='index').T
        print('X.head()', X.head())
        param_values_list = list(model_params.values())
        print('from cost_estimate_predict X:', model_params)
        #return self.model.predict(pd.DataFrame(param_values_list))
        return self.model.predict(X)
        
    def check_required_query_params(self, query_params: dict) -> bool:
        """Проверяем параметры запроса на наличие обязательного набора.
        
        Args:
            query_params (dict): Параметры запроса.
        
        Returns:
        bool: True — если есть нужные параметры, False — иначе
        """
        if "user_id" not in query_params or "model_params" not in query_params:
            return False
        
        if not isinstance(query_params["user_id"], self.param_types["user_id"]):
            return False
                
        if not isinstance(query_params["model_params"], self.param_types["model_params"]):
            return False
        return True

    
    def check_required_model_params(self, model_params: dict) -> bool:
        """Проверяем параметры для получения предсказаний.
        
        Args:
            model_params (dict): Параметры для получения предсказаний моделью.
        
        Returns:
            bool: True — если есть нужные параметры, False — иначе
        """
        if set(model_params.keys()) == set(self.required_model_params):
            return True
        return False
            

    def validate_params(self, params: dict) -> bool:
        """Проверяем корректность параметров запроса и параметров модели.
        
        Args:
            params (dict): Словарь параметров запроса.
        
        Returns:
            bool: True — если проверки пройдены, False — иначе
        """
        
        if self.check_required_query_params(params):
            print("All query params exist")
        else:
            print("Not all query params exist")
            return False
        
        if self.check_required_model_params(params["model_params"]):
            print("All model params exist")
        else:
            print("Not all model params exist")
            return False
        return True
                
                
    def handle(self, params):
        """Функция для обработки запросов API.
        
        Args:
            params (dict): Словарь параметров запроса.
        
        Returns:
            dict: Словарь, содержащий результат выполнения запроса.
        """
        try:
            # Валидируем запрос к API
            if not self.validate_params(params):
                print("Error while handling request")
                response = {"Error": "Problem with parameters"}
            else:
                model_params = params["model_params"]
                user_id = params["user_id"]
                print(f"Predicting for user_id: {user_id} and model_params:\n{model_params}")
                # Получаем предсказания модели
                y_pred = self.cost_estimate_predict(model_params)
                print('y_pred ', y_pred[0])
                if type(self.model) != mlflow.pyfunc.PyFuncModel:
                    y_pred = np.expm1(y_pred*4) 
                else:
                    y_pred = np.expm1(y_pred) 
                response = {
                        "user_id": user_id, 
                        "prediction": y_pred[0]
                    }

        except Exception as e:
            print(f"Error while handling request: {e}")
            return {"Error": "Problem with request"}
        else:
            return response 
"""        
if __name__ == "__main__":

    # Создаём тестовый запрос
    test_params = {
        "user_id": "123",
        "model_params": {"build_type_floors_low_rise": 1,
                "building_area_mean": 41.049999,
                "building_price_mean": 9100000.0,
                "ceiling_height.1": 2.64,
                "dist_origin_dest": 11.107508,
                "living_area.1": 19.9,
                "num_fg__KBinsDiscretizer__kitchen_area": 0.0,
                "num_fg__Polynomial__building_type_int kitchen_area^2": 588.059955,
                "num_fg__Polynomial__ceiling_height total_area": 92.664,
                "num_fg__Polynomial__ceiling_height total_area kitchen_area": 917.373561,
                "num_fg__Polynomial__ceiling_height total_area^2": 3252.506246,
                "num_fg__Polynomial__dist_origin_dest": 11.107508,
                "num_fg__Polynomial__dist_origin_dest distance_to_metro_fast^2": 5967416.055276,
                "num_fg__Polynomial__dist_origin_dest^2 distance_to_metro_fast": 90431.156286,
                "num_fg__Polynomial__dist_origin_dest^2 kitchen_area": 1221.429517,
                "num_fg__Polynomial__dist_origin_dest^2 living_area": 2455.196753,
                "num_fg__Polynomial__dist_origin_dest^2 total_area": 4330.52281,
                "num_fg__Polynomial__floor building_type_int distance_to_metro_fast": 39580.25709,
                "num_fg__Polynomial__floor building_type_int^2": 324.0,
                "num_fg__Polynomial__floor ceiling_height total_area": 833.975997,
                "num_fg__Polynomial__floor total_area^2": 11088.089036,
                "num_fg__Polynomial__living_area^2": 396.009985,
                "num_fg__Polynomial__rooms^2": 1.0,
                "num_fg__Polynomial__total_area living_area^2": 13899.949863,
                "num_fg__Polynomial__total_area^2 kitchen_area": 12196.89747,
                "num_fg__Polynomial__total_area^2 living_area": 24516.996398,
                "total_area.1": 35.099998,
                "total_area_old": 35.099998
                }
    }

    # создаём обработчик запросов для API
    handler = FastApiHandler()

    # делаем тестовый запрос
    response = handler.handle(test_params)
    print(f"Response: {response}") 
"""