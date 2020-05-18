FROM python:3.6

EXPOSE 8000

RUN mkdir /fatec_game
WORKDIR /fatec_game

ADD . /fatec_game

RUN pip install -r requirements.txt

CMD /fatec_game/manage.py runserver 0.0.0.0:8000
