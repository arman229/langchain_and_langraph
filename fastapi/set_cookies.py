from fastapi import APIRouter, Response
from fastapi import Depends
from fastapi.responses import RedirectResponse 
from fastapi.security import OAuth2PasswordBearer  
from fastapi import Depends, HTTPException, status, Request
 

dashboard_routes = APIRouter()


 


@dashboard_routes.get("/login", tags=["dashboard"])
async def get_dashboard_data(response:Response): 
    response.set_cookie(
            key="auth_token",
            value="hatimbinusman",
            httponly=True,  
            secure=True,    
            samesite="lax", 
            max_age=60*60*24*7, 
            path="/"
        )

    return {"message": "Welcome to the dashboard!"}

@dashboard_routes.get("/dashboard", tags=["dashboard"])
async def get_dashboard_data(request: Request):
    cookie = request.cookies.get("auth_token")
    if cookie == "hatimbinusman":
        return {"message": "Welcome to the protected dashboard!"}
    else: 
        raise HTTPException(status_code=401, detail="Unauthorized: Invalid or missing cookie.")