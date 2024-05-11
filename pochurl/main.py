import logging

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastui import prebuilt_html

from pochurl.api import router as api_router
from pochurl.ui import router as ui_router


LEVEL = logging.INFO
FORMAT = "%(levelname)s: %(filename)s - %(message)s"
logger = logging.getLogger()
logging.basicConfig(format=FORMAT, level=LEVEL)

app = FastAPI(
    title="Pochurl",
    description="App to save and organize links",
)

app.include_router(api_router)
app.include_router(ui_router)


@app.get("/", include_in_schema=False)
def html_landing() -> HTMLResponse:
    return HTMLResponse(prebuilt_html(title="Pochurl", api_root_url="/ui"))
