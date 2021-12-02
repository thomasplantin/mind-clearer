FROM python:3.9.0
ADD . /app
WORKDIR /app
RUN pip3 install -r requirements.txt
# ENV PORT 5000
# EXPOSE 5000
# ENTRYPOINT [ "python3" ]
# CMD [ "app.py" ]