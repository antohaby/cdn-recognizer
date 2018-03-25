FROM pypy:3

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "gunicorn", \
      "--reload", \
      "-b", "0.0.0.0:8000", \
      "server:api" ]