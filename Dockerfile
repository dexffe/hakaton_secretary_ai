FROM python:3.11

RUN mkdir /hakaton_ai

WORKDIR /hakaton_ai

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

CMD ["/bin/bash", "-c", "python bot/bot.py"]