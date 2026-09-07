from fastapi import HTTPException

def not_found(message: str):
    return HTTPException(
        status_code=404,
        detail=message
    )

def already_exists(message: str):
    return HTTPException(
        status_code=409,
        detail=message
    )

def bad_request(message: str):
    return HTTPException(
        status_code=400,
        detail=message
    )

def unauthorized(message: str = "Unauthorized"):
    return HTTPException(
        status_code=401,
        detail=message
    )

def forbidden(message: str = "Forbidden"):
    return HTTPException(
        status_code=403,
        detail=message
    )