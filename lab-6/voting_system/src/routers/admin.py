from fastapi import APIRouter, Depends, HTTPException, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database.database import get_db
from database.models import Poll, PollOption
from typing import List
import secrets

router = APIRouter()
templates = Jinja2Templates(directory="src/templates")

@router.get("/", response_class=HTMLResponse)
async def admin_panel(request: Request):
    return templates.TemplateResponse(
        "admin/index.html",
        {"request": request}
    )

@router.post("/polls")
async def create_poll(
    title: str = Form(...),
    description: str = Form(...),
    options: List[str] = Form(...),
    allow_multiple: bool = Form(False),
    db: Session = Depends(get_db)
):
    poll = Poll(
        title=title,
        description=description,
        allow_multiple=allow_multiple
    )
    db.add(poll)
    db.flush()

    for option in options:
        poll_option = PollOption(poll_id=poll.id, text=option)
        db.add(poll_option)

    db.commit()
    return {"status": "success", "poll_id": poll.id}