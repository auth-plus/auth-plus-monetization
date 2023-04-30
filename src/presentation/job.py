from celery import Celery

app = Celery("hello", broker="redis://localhost:6379")


@app.task
def hello():
    return "hello world"
