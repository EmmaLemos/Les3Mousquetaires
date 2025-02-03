from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}


# @app.get("/stop")

# @app.get("/start")
