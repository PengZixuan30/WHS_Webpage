from fastapi import FastAPI
from mcstatus import JavaServer
from contextlib import asynccontextmanager
import asyncio, json

cache = {
    "first": None,
    "second": None,
}

def _query_first():
    try:
        server = JavaServer.lookup("h1.getmc.cn:31410")
        status = server.status()
        return {
            "alive": True,
            "online": status.players.online,
            "max": status.players.max,
            "latency": status.latency,
            "version": status.version.name
        }
    except:
        return {
            "alive": False,
            "online": "?",
            "max": "?",
            "latency": "?",
            "version": "?"
        }

def _query_second():
    try:
        server = JavaServer.lookup("wanghaimc.wdsjfwq.com")
        status = server.status()
        return {
            "alive": True,
            "online": status.players.online,
            "max": status.players.max,
            "latency": status.latency,
            "version": status.version.name
        }
    except:
        return {
            "alive": False,
            "online": "?",
            "max": "?",
            "latency": "?",
            "version": "?"
        }

async def _refresh_loop():
    while True:
        cache["first"], cache["second"] = await asyncio.gather(
            asyncio.to_thread(_query_first),
            asyncio.to_thread(_query_second)
        )
        await asyncio.sleep(300)

@asynccontextmanager
async def lifespan(app: FastAPI):
    cache["first"], cache["second"] = await asyncio.gather(
        asyncio.to_thread(_query_first),
        asyncio.to_thread(_query_second)
    )
    task = asyncio.create_task(_refresh_loop())
    yield
    task.cancel()

def load_notice():
    try:
        with open("notice.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return

app = FastAPI(lifespan=lifespan)

@app.get("/")
def root():
    return {"message": "WHS Server API", "status": "OK"}

@app.get("/api/whs/status/first")
def first_status():
    return cache["first"]

@app.get("/api/whs/status/second")
def second_status():
    return cache["second"]

@app.get("/api/whs/notice")
def notice():
    return load_notice()
