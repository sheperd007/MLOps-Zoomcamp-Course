from fastapi import APIRouter, status
from fastapi.responses import HTMLResponse


router = APIRouter()


@router.get("/")
async def get_home_page():
    html_content = """
    <html>
        <head>
            <title>Covid Detection Service</title>
        </head>
        <body>
            <h1>Covid Detection Service</h1>
            <br>
            Check out the documentation <a href="/blueprint/docs">here</a>
            <br>
            Developed by hamid Jahani
            <br>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=status.HTTP_200_OK)
