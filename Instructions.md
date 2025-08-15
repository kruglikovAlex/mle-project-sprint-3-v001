# Инструкции по запуску микросервиса

Каждая инструкция выполняется из директории репозитория mle-sprint3-completed
Если необходимо перейти в поддиректорию, напишите соотвесвтующую команду

## 1. FastAPI микросервис в виртуальном окружение
```python
# 1. микросервис mlflow для загрузки актуальной ML модели 
#    в микросервис прогнозирования

cd services
cd mlflow_server
# создание виртуального окружения
python3 -m venv .venv_mlflow
source .venv_mlflow/bin/activate
# установки необходимых библиотек 
pip3 install -r requirements.txt
# установка разрешений
sudo chmod +x ./run_mlflow_registry.sh
# запуск сервиса
./run_mlflow_registry.sh

(http://127.0.0.1:5000)

# 2. микросервис погнозирования
#    команды создания виртуального окружения
#    и установки необходимых библиотек в него
cd ..
cd ml_service
# создание виртуального окружения
python3 -m venv .venv_ml
source .venv_ml/bin/activate
# установки необходимых библиотек 
pip3 install -r requirements.txt
# запуск сервиса
uvicorn cost_estimate_app:app --reload --port 8081 --host 0.0.0.0

(http://localhost:8081)
```

### Пример curl-запроса к микросервису

```bash
curl -X 'POST' \
  'http://localhost:8081/api/cost_estimate/?user_id=112233' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{"build_type_floors_low_rise": 0,"building_area_mean": 61.049999, "building_price_mean": 9100000.0, "ceiling_height.1": 2.64, "dist_origin_dest": 11.107508, "living_area.1": 19.9, "num_fg__KBinsDiscretizer__kitchen_area": 0.0, "num_fg__Polynomial__building_type_int kitchen_area^2": 588.059955, "num_fg__Polynomial__ceiling_height total_area": 92.664, "num_fg__Polynomial__ceiling_height total_area kitchen_area": 917.373561, "num_fg__Polynomial__ceiling_height total_area^2": 3252.506246, "num_fg__Polynomial__dist_origin_dest": 11.107508, "num_fg__Polynomial__dist_origin_dest distance_to_metro_fast^2": 5967416.055276, "num_fg__Polynomial__dist_origin_dest^2 distance_to_metro_fast": 90431.156286, "num_fg__Polynomial__dist_origin_dest^2 kitchen_area": 1221.429517, "num_fg__Polynomial__dist_origin_dest^2 living_area": 2455.196753, "num_fg__Polynomial__dist_origin_dest^2 total_area": 4330.52281, "num_fg__Polynomial__floor building_type_int distance_to_metro_fast": 39580.25709, "num_fg__Polynomial__floor building_type_int^2": 324.0, "num_fg__Polynomial__floor ceiling_height total_area": 833.975997, "num_fg__Polynomial__floor total_area^2": 11088.089036, "num_fg__Polynomial__living_area^2": 396.009985, "num_fg__Polynomial__rooms^2": 1.0, "num_fg__Polynomial__total_area living_area^2": 13899.949863, "num_fg__Polynomial__total_area^2 kitchen_area": 12196.89747, "num_fg__Polynomial__total_area^2 living_area": 24516.996398, "total_area.1": 35.099998, "total_area_old": 35.099998}'
```


## 2. FastAPI микросервис в Docker-контейнере

```bash
# команда перехода в нужную директорию

# команда для запуска микросервиса в режиме docker compose
```

### Пример curl-запроса к микросервису

```bash
curl -X 'POST' \
  'http://localhost:...' \
```

## 3. Docker compose для микросервиса и системы моониторинга

```bash
# команда перехода в нужную директорию

# команда для запуска микросервиса в режиме docker compose

```

### Пример curl-запроса к микросервису

```bash
curl -X 'POST' \
  'http://localhost:
```

## 4. Скрипт симуляции нагрузки
Скрипт генерирует <...> запросов в течение <...> секунд ...

```
# команды необходимые для запуска скрипта
...
```

Адреса сервисов:
- микросервис: http://localhost:<port>
- Prometheus: ...
- Grafana: ...