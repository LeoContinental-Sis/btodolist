FROM python:3.11-slim-buster

WORKDIR /app

COPY requirements.txt .

RUN apt-get update && apt-get install -y --no-install-recommends wget build-essential

# Descargar e instalar una versión específica de SQLite (la más reciente estable)
RUN wget https://www.sqlite.org/2024/sqlite-autoconf-3450100.tar.gz
RUN tar xzf sqlite-autoconf-3450100.tar.gz
WORKDIR /app/sqlite-autoconf-3450100
RUN ./configure --prefix=/usr/local
RUN make -j$(nproc)
RUN make install
RUN ldconfig
WORKDIR /app
RUN rm -rf sqlite-autoconf-3450100 sqlite-autoconf-3450100.tar.gz

RUN sqlite3 --version

COPY . .

RUN pip install -r requirements.txt  # <-- Mueve esta línea aquí

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]