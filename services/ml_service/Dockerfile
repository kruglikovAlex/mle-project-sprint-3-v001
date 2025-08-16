FROM python:3.11-slim
LABEL author=${LABEL}


COPY . ./ml_service
WORKDIR ml_service 

RUN pip3 install -r requirements.txt

EXPOSE 1702

CMD uvicorn cost_estimate_app:app --reload --port 1702 --host 0.0.0.0