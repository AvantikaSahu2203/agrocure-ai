from pydantic import BaseModel

class EcommerceSearchRequest(BaseModel):
    medicine_name: str
    city: str
    state: str

class EcommerceSearchResponse(BaseModel):
    amazon_url: str
    flipkart_url: str
    bighaat_url: str
    agrostar_url: str
    indiamart_url: str
    google_maps_url: str
