import os
from jose import jwt, JWTError, ExpiredSignatureError
from dotenv import load_dotenv
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from datetime import datetime, timedelta, timezone
from app.auth.exceptions import CouldNotValidateCredentials
import resend

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
SECRET_KEY_REFRESH = os.getenv('SECRET_KEY_REFRESH')
SECRET_KEY_FORGOT_PASSWORD = os.getenv('SECRET_KEY_FORGOT_PASSWORD')
RESEND_API_KEY = os.getenv('RESEND_API_KEY')

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440
REFRESH_TOKEN_EXPIRE_DAYS = 7
FORGOT_TOKEN_EXPITE_MINUTES = 15

# Set resend api key.
resend.api_key = RESEND_API_KEY

oauth2scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encode_jwt

def create_refresh_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    encode_jwt = jwt.encode(to_encode, SECRET_KEY_REFRESH, algorithm=ALGORITHM)
    return encode_jwt

def get_current_user(token: str = Depends(oauth2scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="Token inválido"
            )
        
        return user_id
    except ExpiredSignatureError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Token inválido"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, 
            detail=str(e)
        )

def verify_refresh_token_service(refresh_token: str):
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY_REFRESH, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            CouldNotValidateCredentials()
    
        return user_id
    except JWTError:
        CouldNotValidateCredentials()

def create_forgot_password_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=FORGOT_TOKEN_EXPITE_MINUTES)
    to_encode.update({"exp": expire})
    encode_jwt = jwt.encode(to_encode, SECRET_KEY_FORGOT_PASSWORD, algorithm=ALGORITHM)
    return encode_jwt

def verfiy_forgot_password_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY_FORGOT_PASSWORD, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            CouldNotValidateCredentials()
    
        return user_id
    except JWTError:
        CouldNotValidateCredentials()

def send_email_service(token: str, email_to: str, user):
    reset_link = f"http://localhost:3000/reset-password?token={token}&email={email_to}&user={user}"
    content = f"""
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <title>Recuperar contraseña</title>
        </head>
        <body>
            <p>Hola,</p>
            <p>Para restablecer tu contraseña, haz clic en el siguiente enlace:</p>
            <p><a href="{reset_link}">Restablecer contraseña</a></p>
            <p>Si no solicitaste este cambio, ignora este correo.</p>
            <p>Gracias,</p>
            <p>El equipo de soporte</p>
        </body>
        </html>
    """

    params: resend.Emails.SendParams = {
        "from": "no-reply@ldmontielm.com",
        "to": [email_to],
        "subject": "Recovery Password",
        "html": content
    }

    email: resend.Email = resend.Emails.send(params)
    return email