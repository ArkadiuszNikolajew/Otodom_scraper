FROM python:3.9-alpine
RUN pip install pipenv
COPY Pipfile* app/
RUN pipenv lock --keep-outdated -r > app/requirements.txt
RUN pip install -r /app/requirements.txt
COPY . app/