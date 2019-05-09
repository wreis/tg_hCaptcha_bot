FROM python:3.7.3

ENV BASE_DIR /opt/tg_hCaptcha_bot

VOLUME ["$BASE_DIR"]

WORKDIR $BASE_DIR

COPY requirements.txt $BASE_DIR/requirements.txt
RUN pip install --upgrade pip && pip install setuptools && pip install -r requirements.txt

EXPOSE 5000

CMD ["python", "tests.py"]