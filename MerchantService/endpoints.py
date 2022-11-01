from merchant_event_sender import MerchantEventSender
from fastapi import APIRouter, Depends
from models import OrderModel
from merchant_repository import MerchantRepository
from dependency_injector.wiring import inject, Provide
from container import Container

router = APIRouter()


