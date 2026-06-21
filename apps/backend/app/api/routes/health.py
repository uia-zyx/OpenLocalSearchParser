from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get(
    "/health",
    operation_id="get_health_status",
    summary="Check backend health",
)
async def health() -> dict[str, str]:
    return {"status": "ok"}

