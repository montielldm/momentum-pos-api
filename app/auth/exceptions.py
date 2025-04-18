from fastapi import HTTPException, status

def UnauthorizedUser():
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="UNAUTHORIZED_USER",
        headers={"WWW-Authenticate": "Bearer"}
    )

def CouldNotValidateCredentials():
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="COULD_NOT_VALIDATE_CREDENTIALS",
        headers={"WWW-Authenticate": "Bearer"}
    )