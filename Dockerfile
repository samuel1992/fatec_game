FROM python:3.8

EXPOSE 8000

RUN mkdir /fatec_game
WORKDIR /fatec_game

COPY requirements.txt /fatec_game
RUN pip install -r requirements.txt

COPY . /fatec_game

CMD /fatec_game/manage.py runserver 0.0.0.0:8000
