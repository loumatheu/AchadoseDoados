from fastapi import APIRouter, HTTPException, Depends, status
from typing import Optional 
from app.geolocation.models import Coordinates, DistanceCalculationRequest, DistanceResponse, AddressInfo
from app.geolocation.services import GeolocationService


async def get_geolocation_service() -> GeolocationService:
    return GeolocationService()

router = APIRouter()

@router.post(
    "/convert-cep-to-coords",
    response_model=AddressInfo,
    summary="Convert CEP to coordinates (latitude/longitude)",
    description="Do the conversion and returns 404 Not Found if the CEP is not found or cannot be geocoded."
)
async def convert_cep_to_coordinates_endpoint(
    cep: str,
    geolocation_service: GeolocationService = Depends(get_geolocation_service) # Dependency injection for the service
):
    coordinates = await geolocation_service.get_coordinates_from_cep(cep)
    if not coordinates:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Could not retrieve coordinates for CEP: {cep}. Please check the CEP or try again later."
        )
    
    return AddressInfo(cep=cep, coordinates=coordinates)


@router.post(
    "/calculate-distance",
    response_model=DistanceResponse,
    summary="Calculate distance between two CEPs",
    description="Calculates the distance in kilometers between two provided CEPs. Returns 404 Not Found if one of the CEPs cannot be geocoded."
)
async def calculate_distance_endpoint(
    request: DistanceCalculationRequest,
    geolocation_service: GeolocationService = Depends(get_geolocation_service)
):
    origin_coords = await geolocation_service.get_coordinates_from_cep(request.origin_cep)
    if not origin_coords:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Could not retrieve coordinates for origin CEP: {request.origin_cep}"
        )

    destination_coords = await geolocation_service.get_coordinates_from_cep(request.destination_cep)
    if not destination_coords:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Could not retrieve coordinates for destination CEP: {request.destination_cep}"
        )

    distance_km = await geolocation_service.calculate_distance(origin_coords, destination_coords)

    return DistanceResponse(
        origin_cep=request.origin_cep,
        destination_cep=request.destination_cep,
        distance_km=distance_km,
        origin_coordinates=origin_coords,
        destination_coordinates=destination_coords
    )