FROM python:3.9

# add django user and group which should be the one running the service
RUN groupadd -g 500 django && useradd -r -u 500 -g django django

ENV PYTHONUNBUFFERED 1
ENV IN_DOCKER 1

ENV PROJECT_ROOT /app
WORKDIR $PROJECT_ROOT
RUN chown -R 500:500 $PROJECT_ROOT

EXPOSE 8000

ENTRYPOINT ["sh", "entrypoint.sh"]

COPY requirements.txt Makefile ./
RUN make install_requirements_txt
COPY --chown=django:django . .

CMD ["uwsgi", "--http", "0.0.0.0:8000", "--uid", "500", "--chdir", "/app/src", "--wsgi-file", "/app/src/config/wsgi.py", "--callable", "application", "--processes", "2", "--threads", "4", "--master"]