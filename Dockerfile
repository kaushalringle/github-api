FROM python:3.8.5-alpine3.12

ENV VIR_ENV=/opt/env 

RUN python3 -m venv ${VIR_ENV}

ENV PATH = "${VIR_ENV}/bin:${PATH}"

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY github-manager.py . 

ENTRYPOINT ["python", "github-manager.py"]