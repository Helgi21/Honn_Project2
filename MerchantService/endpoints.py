from fastapi import APIRouter, Depends
from models import MerchantModel
from merchant_repository import MerchantRepository
from dependency_injector.wiring import inject, Provide
from container import Container

router = APIRouter()

@router.post('/merchants')
@inject
async def create_merchant(merchant: MerchantModel, 
                          merchant_repository: MerchantRepository = Depends(Provide[Container.merchant_repository_provider]),):
    res = merchant_repository.create_merchant(merchant)
    return res

@router.get('/merchants/{merchant_id}')
@inject
async def get_merchant(merchant_id: int,
                       merchant_repository: MerchantRepository = Depends(Provide[Container.merchant_repository_provider])):
    return merchant_repository.get_merchant(merchant_id)