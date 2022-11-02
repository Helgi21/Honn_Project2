from fastapi import APIRouter, Depends
from models import ProductModel
from product_repository import ProductRepository
from dependency_injector.wiring import inject, Provide
from container import Container

router = APIRouter()


@router.post('/products')
@inject
async def create_product(product: ProductModel, 
                        product_repository: ProductRepository = Depends(Provide[Container.product_repository_provider])):
    res = product_repository.create_product(product)
    return res

@router.get('/profucts/{product_id}')
@inject
async def get_order(product_id: int,
                    product_repository: ProductRepository = Depends(Provide[Container.product_repository_provider])):
    return product_repository.get_product(product_id)