FROM python:3.11.4
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /youpayroll
COPY requirements.txt /youpayroll/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . /youpayroll/
