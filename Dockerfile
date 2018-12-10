FROM python:2.7.9

ADD app $HOME/app

RUN pip install -U pip setuptools
RUN pip install -r app/requirements.txt

ENTRYPOINT ["python", "app/demo.py", "--token"]
