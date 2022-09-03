FROM python:3.10.6-slim-bullseye

WORKDIR /home/lolicon/web

COPY . /home/lolicon/web

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

EXPOSE 8080

VOLUME [ "/etc/lolicon" ]

CMD [ "/usr/local/bin/python3", "lolicon_web/app.py" ]
