"""FastAPI-приложение для модели оттока."""

from fastapi import FastAPI, Body
from ml_service.fast_api_handler import FastApiHandler
from prometheus_fastapi_instrumentator import Instrumentator
import numpy as np
from prometheus_client import Histogram
from prometheus_client import Counter

"""
Пример запуска из директории mle-sprint3/app:
uvicorn cost_estimate_app:app --reload --port 8081 --host 0.0.0.0

Для просмотра документации API и совершения тестовых запросов зайти на  http://127.0.0.1:8081/docs

Если используется другой порт, то заменить 8081 на этот порт Порт надо проверить
"""

# создаём приложение FastAPI
app = FastAPI()

# создаём обработчик запросов для API
app.handler = FastApiHandler()

# инициализируем и запускаем экпортёр метрик
instrumentator = Instrumentator()
instrumentator.instrument(app).expose(app)

main_app_predictions = Histogram(
    # имя метрики
    "main_app_predictions",
    #описание метрики
    "Histogram of predictions",
    #указаываем корзины для гистограммы
    buckets=(10000.000, 250000.000, 1000000.000, 500000000.000, 1000000000.000)
)

main_app_counter_pos = Counter("main_app_counter_pos", "Count of positive predictions")

# обрабатываем запросы к корню приложения
@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/api/cost_estimate/") 
def get_prediction_for_item(user_id: str, model_params: dict):
    """Функция для получения стоимости квартиры.

    Args:
        user_id (str): Идентификатор пользователя.
        model_params (dict): Параметры пользователя, которые нужно передать в модель.

    Returns:
        dict: Предсказание, уйдёт ли пользователь из сервиса.
    """
    required_response_params = {'user_id', 'prediction'}
            
    all_params = {
        "user_id": user_id,
        "model_params": model_params
    }
    
    response = app.handler.handle(all_params) 
    
    main_app_counter_pos.inc()
    
    if set(response.keys()) == set(required_response_params):
        print('Переход в Prometheus all')
        print('response["prediction"]', response["prediction"])
        main_app_predictions.observe(response["prediction"])
        
    return response