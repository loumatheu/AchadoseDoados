import httpx
from geopy.distance import geodesic
from geopy.geocoders import Nominatim
from typing import Optional
from app.geolocation.models import Coordinates, AddressInfo

geolocator = Nominatim(user_agent="admin_achadosedoados")

class GeolocationService:

    async def get_coordinates_from_cep(self, cep: str) -> Optional[Coordinates]:
        """
        Converte um CEP em latitude e longitude.
        Primeiro tenta ViaCEP para obter o endereço, depois Nominatim para coordenadas.
        """
        cep = cep.replace("-", "").replace(".", "")

        # Tentar ViaCEP para obter informações de endereço
        viacep_url = f"https://viacep.com.br/ws/{cep}/json/"
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(viacep_url, timeout=5)
                response.raise_for_status()
                data = response.json()

                if data.get("erro"):
                    print(f"Erro ao buscar CEP no ViaCEP: {cep} - CEP não encontrado.")
                    return None

                # Montar o endereço completo para o Nominatim
                full_address_parts = [
                    data.get('logradouro'),
                    data.get('bairro'),
                    data.get('localidade'),
                    data.get('uf'),
                    data.get('cep')
                ]
                # Filtra partes vazias ou nulas e junta com vírgula
                full_address = ", ".join(filter(None, full_address_parts))
                
                # 2. Usar Nominatim para obter as coordenadas do endereço completo
                return await self._get_coordinates_from_address(full_address)

            except httpx.RequestError as e:
                print(f"Erro de conexão com ViaCEP para o CEP {cep}: {e}")
                return None
            except Exception as e:
                print(f"Erro inesperado ao processar ViaCEP para o CEP {cep}: {e}")
                return None

    async def _get_coordinates_from_address(self, address: str) -> Optional[Coordinates]:
        """
        Converte um endereço completo em latitude e longitude usando Nominatim.
        """
        print(f"Geocodificando endereço com Nominatim: {address}")
        try:
            # O método geocode da Nominatim é síncrono, então usamos run_in_executor
            # para não bloquear o loop de eventos do FastAPI.
            import concurrent.futures
            loop = concurrent.futures.ThreadPoolExecutor()
            location = await loop.submit(geolocator.geocode, address, timeout=10)

            if location:
                print(f"Coordenadas encontradas para '{address}': {location.latitude}, {location.longitude}")
                return Coordinates(latitude=location.latitude, longitude=location.longitude)
            else:
                print(f"Não foi possível geocodificar o endereço: '{address}'")
                return None
        except Exception as e:
            print(f"Erro ao geocodificar '{address}' com Nominatim: {e}")
            return None

    async def calculate_distance(self, origin: Coordinates, destination: Coordinates) -> float:
        """
        Calcula a distância entre duas coordenadas em quilômetros.
        """
        coords_origin = (origin.latitude, origin.longitude)
        coords_destination = (destination.latitude, destination.longitude)
        distance = geodesic(coords_origin, coords_destination).kilometers
        return distance