from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from starlette.requests import Request

from sse_starlette.sse import EventSourceResponse

from generator import match_event_generator, simple_event_generator


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="templates")


@app.get("/events")
async def sse_endpoint():
    return EventSourceResponse(simple_event_generator())


@app.get("/live-scores")
async def live_scores_endpoint():
    return EventSourceResponse(match_event_generator('Inter', 'Milan', 20))


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
