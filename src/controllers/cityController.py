from models.city import City


class CityController:
    def __init__(self):
        self.cities = []  # Simulando um banco de dados em memória

    def create_city(self, city: City) -> bool:
        if any(c.idcity == city.idcity for c in self.cities):
            return False  # Evita IDs duplicados
        self.cities.append(city)
        return True

    def get_city(self, idcity: str) -> City | None:
        for city in self.cities:
            if city.idcity == idcity:
                return city
        return None

    def update_city(self, idcity: str, new_name: str) -> bool:
        city = self.get_city(idcity)
        if city:
            city.name_city = new_name
            return True
        return False

    def delete_city(self, idcity: str) -> bool:
        for city in self.cities:
            if city.idcity == idcity:
                self.cities.remove(city)
                return True
        return False

    def list_cities(self) -> list[City]:
        return self.cities
