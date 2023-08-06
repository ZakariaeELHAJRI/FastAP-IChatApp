FROM python:3.11-alpine

# set working directory
WORKDIR /app

# upgrade pip
RUN pip install --upgrade pip

# install requirements.txt
COPY requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir

# copy source code
COPY . .

# run app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
