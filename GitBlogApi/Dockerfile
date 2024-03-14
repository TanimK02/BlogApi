FROM python:3.12
WORKDIR /BlogApi
COPY ./requirements.txt requirements.txt
RUN  pip install -r requirements.txt
COPY . .
CMD ["flask", "run", "--host=0.0.0.0", "-p", "3000"]
EXPOSE 3000