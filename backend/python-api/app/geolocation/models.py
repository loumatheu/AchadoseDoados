from pydantic import BaseModel, Field
from typing import List, Optional

class Coordinates(BaseModel):
    latitude: float = Field(..., description="Latitude do local")
    longitude: float = Field(..., description="Longitude do local")

class AddressInfo(BaseModel):
    cep: str = Field(..., pattern=r"^\d{8}$", description="CEP do endereço (apenas números)")
    street: Optional[str] = Field(None, description="Nome da rua")
    neighborhood: Optional[str] = Field(None, description="Nome do bairro")
    city: Optional[str] = Field(None, description="Nome da cidade")
    state: Optional[str] = Field(None, description="Sigla do estado")
    coordinates: Optional[Coordinates] = Field(None, description="Coordenadas geográficas do endereço")

class DistanceCalculationRequest(BaseModel):
    origin_cep: str = Field(..., pattern=r"^\d{8}$", description="CEP de origem (apenas números)")
    destination_cep: str = Field(..., pattern=r"^\d{8}$", description="CEP de destino (apenas números)")

class DistanceResponse(BaseModel):
    origin_cep: str
    destination_cep: str
    distance_km: float = Field(..., description="Distância entre os CEPs em quilômetros")
    origin_coordinates: Coordinates
    destination_coordinates: Coordinates