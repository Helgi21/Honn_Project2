from order_event_sender import OrderEventSender
from fastapi import APIRouter, Depends
from dependency_injector.wiring import inject, Provide

from models import BuyerModel
from buyer_repository import BuyerRepository
from container import Container

router = APIRouter()


@router.post('/buyers')
@inject
async def create_buyer(buyer: BuyerModel, 
                        buyer_repository: BuyerRepository = Depends(Provide[Container.buyer_repository_provider])):
    return buyer_repository.create_buyer(buyer)

@router.get('/buyers/{buyer_id}')
@inject
async def get_buyer(buyer_id: int,
                    buyer_repository: BuyerRepository = Depends(Provide[Container.buyer_repository_provider])):
    return buyer_repository.get_buyer(buyer_id)