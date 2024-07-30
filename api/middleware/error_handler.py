from fastapi.responses import JSONResponse

def return_error(request, exc):
    status_code = 500
    return JSONResponse(
        status_code=status_code,
        content={
            "success": False,
            "status": status_code,
            "message": str(exc),
        },
    )
