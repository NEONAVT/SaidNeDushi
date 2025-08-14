from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from pygments.regexopt import regex_opt_inner
from starlette.status import HTTP_409_CONFLICT

from dependency import get_request_user_id, get_category_service
from exceptions import CategoryExistAlready, CategoryNotFound
from schemas.tasks import CategorySchema, CategoryCreateSchema
from services.tasks import CategoryService

router = APIRouter(
    prefix="/categories",
    tags=["Categories"]
)

@router.get("/all")
def get_all_categories(
        category_service: Annotated[CategoryService, Depends(get_category_service)]
) -> list[CategorySchema]:
    return category_service.get_all_categories()


@router.get("/{category_id}")
def get_category(
        category_id: int,
        category_service: Annotated[CategoryService, Depends(get_category_service)]
) -> CategorySchema:
    try:
        return category_service.get_category_by_id(category_id)
    except CategoryNotFound as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=e.detail)


@router.post("/create", status_code=status.HTTP_201_CREATED)
def create_category(
        body: CategoryCreateSchema,
        category_service: Annotated[CategoryService, Depends(get_category_service)]
) -> CategorySchema:
    try:
        return category_service.create_category(body)
    except CategoryExistAlready as e:
        raise HTTPException(status_code=HTTP_409_CONFLICT, detail=e.detail)

@router.patch("/patch", response_model=CategorySchema)
def patch_category(
        category_id:int,
        body: CategoryCreateSchema,
        category_service: Annotated[CategoryService, Depends(get_category_service)]

):
    try:
        return category_service.update_category(category_id=category_id, name=body.name, type=body.type)
    except CategoryNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.detail)


@router.delete("/delete")
def delete_category(
        category_id: int,
        category_service: Annotated[CategoryService, Depends(get_category_service)]
):
    try:
        return category_service.delete_category(category_id=category_id)
    except CategoryNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.detail)
