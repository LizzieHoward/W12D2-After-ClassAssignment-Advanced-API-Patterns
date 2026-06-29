from fastapi import Request
from fastapi.responses import JSONResponse


def error_response(
    request: Request,
    status_code: int,
    code: str,
    message: str,
    details: object | None = None,
) -> JSONResponse:
    request_id = getattr(request.state, "request_id", "")
    error: dict[str, object] = {"code": code, "message": message, "status_code": status_code}
    if details is not None:
        error["details"] = details
    return JSONResponse(status_code=status_code, content={"error": error, "request_id": request_id})
