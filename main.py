from fastapi import FastAPI

from moonapi import moonshot_api

import uvicorn


app = FastAPI()


app.include_router(moonshot_api, tags=["model api request"])


if __name__ == "__main__":
    # 连接的地址是 http://127.0.0.1:8181
    uvicorn.run(app='main:app', host='127.0.0.1', port=8181, reload=True)