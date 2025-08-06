import random
from datetime import timedelta

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from auth import (create_access_token, get_current_user, get_password_hash,
                  verify_password, verify_token)
from config import settings
from database import engine, get_db
from models import Base, Post, User
from schemas import Token
from schemas import User as UserSchema
from schemas import UserCreate, UserWithPosts

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="FastAPI Demo", description="A simple FastAPI project with PostgreSQL")


@app.post("/signup", response_model=UserSchema)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user account with email and password
    """
    # Check if user already exists
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Create new user with hashed password
    hashed_password = get_password_hash(user.password)
    db_user = User(
        email=user.email,
        name=user.name,
        password=hashed_password
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


@app.post("/token", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Login endpoint to get JWT token
    """
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=settings.jwt_access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/random")
def random_endpoint(db: Session = Depends(get_db)):
    """
    Generate random integer 1-1000, create JWT for a random user, decode it, and return user's posts
    """
    # Generate random integer from 1-1000
    random_number = random.randint(1, 1000)

    # Get a random user from the database
    users = db.query(User).all()
    if not users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No users found in database"
        )

    random_user = random.choice(users)

    # Create JWT token for the random user
    access_token_expires = timedelta(minutes=settings.jwt_access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": random_user.email}, expires_delta=access_token_expires
    )

    # Decode the JWT token to verify it
    try:
        from jose import jwt
        payload = jwt.decode(access_token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
        decoded_email = payload.get("sub")

        if decoded_email != random_user.email:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="JWT token verification failed"
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"JWT token decoding failed: {str(e)}"
        )

    # Get all posts for the user
    user_posts = db.query(Post).filter(Post.user_id == random_user.id).all()

    return {
        "random_number": random_number,
        "user": {
            "id": random_user.id,
            "name": random_user.name,
            "email": random_user.email
        },
        "jwt_token": access_token,
        "posts": [
            {
                "id": post.id,
                "title": post.title,
                "content": post.content,
                "created_at": post.created_at,
                "updated_at": post.updated_at
            }
            for post in user_posts
        ]
    }


@app.get("/users/me", response_model=UserSchema)
def read_users_me(current_user: User = Depends(get_current_user)):
    """
    Get current user information
    """
    return current_user


@app.get("/users/me/posts")
def read_user_posts(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    Get all posts for the current user
    """
    posts = db.query(Post).filter(Post.user_id == current_user.id).all()
    return posts


@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI Demo", "docs": "/docs"}


@app.get("/{anything:path}")
def catch_all(anything: str):
    """
    Generic catch-all route that echoes the path segment.
    """
    return anything
