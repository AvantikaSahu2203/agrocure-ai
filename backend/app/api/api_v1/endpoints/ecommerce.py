from fastapi import APIRouter
from app.schemas.ecommerce import EcommerceSearchRequest, EcommerceSearchResponse
from app.services.ecommerce import generate_search_urls

router = APIRouter()

@router.post("/search", response_model=EcommerceSearchResponse)
def search_ecommerce_links(request: EcommerceSearchRequest):
    """
    Generate search URLs for agricultural medicines on various e-commerce platforms.
    """
    return generate_search_urls(request)
