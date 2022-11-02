from order_event_sender import OrderEventSender
from fastapi import APIRouter, Depends
from models import OrderModel
from order_repository import OrderRepository
from dependency_injector.wiring import inject, Provide
from container import Container

router = APIRouter()


@router.post('/orders')
@inject
async def create_order(order: OrderModel, 
                        order_repository: OrderRepository = Depends(Provide[Container.order_repository_provider]),
                        order_event_sender: OrderEventSender = Depends(Provide[Container.order_event_sender_provider])):
    res = order_repository.create_order(order)
    order_event_sender.send_event(order)
    return res

@router.get('/orders/{order_id}')
@inject
async def get_order(order_id: int,
                    order_repository: OrderRepository = Depends(Provide[Container.order_repository_provider])):
    return order_repository.get_order(order_id)