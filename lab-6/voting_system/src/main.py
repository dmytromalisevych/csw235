import os
import logging
from pathlib import Path

from fastapi import FastAPI, Depends, HTTPException, Response, status, Request
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
from typing import List, Optional
from jose import JWTError, jwt

from database.models import User, Poll, Vote
from database import SessionLocal, engine
from schemas.poll_schema import UserCreate, PollCreate, VoteCreate, Poll as PollSchema, User as UserSchema, VoteResponse
from services.poll_service import (
    get_user_by_username,
    verify_password,
    create_user,
    get_active_polls,
    get_poll,
    create_poll,
    create_vote
)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(title="Voting System")

BASE_DIR = Path(__file__).resolve().parent

app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")

templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token", auto_error=False)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    if token is None:
        return None
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            return None
    except JWTError:
        return None
    
    user = get_user_by_username(db, username)
    return user

@app.get("/")
async def home(request: Request, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        active_polls = get_active_polls(db)
        template_data = {
            "request": request,
            "user": current_user,
            "polls": active_polls,
            "debug_message": "This is a debug message"
        }

        print("Rendering template with data:", template_data)
        
        return templates.TemplateResponse(
            "index.html",
            template_data
        )
    except Exception as e:
        import traceback
        print("Error occurred:")
        print(traceback.format_exc())
        
        return templates.TemplateResponse(
            "404.html",
            {
                "request": request,
                "error_message": str(e)
            },
            status_code=500
        )
@app.post("/login")
async def login(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    logger.info(f"Login attempt for user: {form_data.username}")
    
    try:
        user = db.query(User).filter(User.username == form_data.username).first()
        
        logger.info(f"Found user: {user}")
        
        if not user:
            logger.warning(f"User not found: {form_data.username}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Невірний логін або пароль"
            )
            
        if not verify_password(form_data.password, user.password_hash):
            logger.warning(f"Invalid password for user: {form_data.username}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Невірний логін або пароль"
            )
            
        access_token = create_access_token(data={"sub": user.username})
        
        response = RedirectResponse(url="/", status_code=302)
        response.set_cookie(
            key="access_token",
            value=f"Bearer {access_token}",
            httponly=True,
            max_age=1800,
            samesite="lax"
        )
        
        logger.info(f"Successful login for user: {form_data.username}")
        return response
        
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Помилка при авторизації"
        )

@app.get("/")
async def root(request: Request):
    logger.info("Accessing root page")
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "user": None,  
            "polls": [],  
            "debug_message": "This is a debug message"
        }
    )

@app.get("/login")
async def login_page(request: Request):
    logger.info("Accessing login page")
    return templates.TemplateResponse(
        "login.html",
        {"request": request, "title": "Вхід в систему"}
    )

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    logger.error(f"HTTP error: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    logger.error(f"General error: {str(exc)}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal server error"}
    )

@app.get("/polls/active")
async def get_active_polls(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        polls = db.query(Poll).filter(Poll.is_active == True).all()
        return {"polls": [poll.to_dict() for poll in polls]}
    except Exception as e:
        logger.error(f"Error getting active polls: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Помилка при отриманні голосувань"
        )

@app.get("/api/polls/{poll_id}", response_model=PollSchema)
def read_poll(poll_id: int, db: Session = Depends(get_db)):
    poll = get_poll(db, poll_id)
    if poll is None:
        raise HTTPException(status_code=404, detail="Poll not found")
    
    # Підрахунок голосів
    for option in poll.options:
        option.votes_count = db.query(func.count(Vote.id))\
            .filter(Vote.option_id == option.id)\
            .scalar()
    poll.total_votes = sum(option.votes_count for option in poll.options)
    return poll

@app.post("/api/polls", response_model=PollSchema)
def create_poll_endpoint(
    poll: PollCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return create_poll(db, poll, current_user.id)

@app.post("/api/vote", response_model=VoteResponse)
def create_vote_endpoint(
    vote: VoteCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )

    poll = get_poll(db, vote.poll_id)
    if not poll or not poll.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Poll is not active"
        )

    if poll.ends_at and poll.ends_at < datetime.utcnow():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Poll has ended"
        )

    if not poll.allow_multiple:
        existing_vote = db.query(Vote)\
            .filter(Vote.user_id == current_user.id, 
                   Vote.poll_id == vote.poll_id)\
            .first()
        if existing_vote:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You have already voted in this poll"
            )

    success = create_vote(db, vote, current_user.id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not create vote"
        )
    return {"message": "Vote registered successfully"}

@app.get("/admin")
async def admin_panel(
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not current_user or not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    all_polls = db.query(Poll).all()
    return templates.TemplateResponse(
        "admin.html",
        {
            "request": request,
            "user": current_user,
            "polls": all_polls
        }
    )

@app.get("/polls/{poll_id}")
async def view_poll(
    request: Request,
    poll_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    poll = get_poll(db, poll_id)
    if poll is None:
        raise HTTPException(status_code=404, detail="Poll not found")
    
    for option in poll.options:
        option.votes_count = db.query(func.count(Vote.id))\
            .filter(Vote.option_id == option.id)\
            .scalar()
    poll.total_votes = sum(option.votes_count for option in poll.options)

    user_voted = False
    if current_user:
        user_voted = db.query(Vote)\
            .filter(Vote.user_id == current_user.id,
                   Vote.poll_id == poll_id)\
            .first() is not None

    return templates.TemplateResponse(
        "poll.html",
        {
            "request": request,
            "user": current_user,
            "poll": poll,
            "user_voted": user_voted
        }
    )

@app.post("/api/register", response_model=UserSchema)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_username(db, user.username)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    return create_user(db, user)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app", 
        host="127.0.0.1", 
        port=8000,  
        reload=True,  
        workers=1,  
        log_level="info" 
    )