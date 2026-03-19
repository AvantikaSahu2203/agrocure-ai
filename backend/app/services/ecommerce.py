import urllib.parse
from app.schemas.ecommerce import EcommerceSearchRequest, EcommerceSearchResponse

def generate_search_urls(request: EcommerceSearchRequest) -> EcommerceSearchResponse:
    """
    Generate search URLs for various e-commerce platforms and Google Maps.
    """
    encoded_medicine = urllib.parse.quote(request.medicine_name)
    encoded_location = urllib.parse.quote(f"{request.city} {request.state}")

    return EcommerceSearchResponse(
        amazon_url=f"https://www.amazon.in/s?k={encoded_medicine}",
        flipkart_url=f"https://www.flipkart.com/search?q={encoded_medicine}",
        bighaat_url=f"https://www.bighaat.com/search?q={encoded_medicine}",
        # AgroStar search is app-centric, fallback to google search for agrostar or general query if specific url not found
        # Using a probable search URL structure for web if available, otherwise just linking to site might be less useful. 
        # Let's use a google search restricted to agrostar.in as a fallback or the direct search if it works.
        # Research suggested direct search might not be standard. 
        # Let's use a generic query param which is common.
        agrostar_url=f"https://www.google.com/search?q=site:agrostar.in+{encoded_medicine}", 
        indiamart_url=f"https://dir.indiamart.com/search.mp?ss={encoded_medicine}",
        google_maps_url=f"https://www.google.com/maps/search/{encoded_medicine}+store+near+{encoded_location}"
    )
