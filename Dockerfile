# base image
FROM python:3.8.2-alpine
LABEL maintainer="sagarsharma8397@gmail.com"

# prevent writing pyc files to disc
ENV PYTHONDONTWRITEBYTECODE 1
# no buffer (for streaming the output directly)
ENV PYTHONUNBUFFERED 1

# define default environment
ENV DJANGO_SETTINGS_MODULE=app.settings

# Install system dependencies
RUN apk --update add python3-dev postgresql-dev gcc musl-dev


# copy entrypoint
COPY ./entrypoint.sh .

# copy project
COPY . .

# install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Run entry scripts when container launches
RUN chmod +x entrypoint.sh
ENTRYPOINT ["bin/sh", "entrypoint.sh"]
