# RA 210000

# Se necessario importe suas bibliotecas aqui
from dataclasses import dataclass
from sys import stdin
from date import Data

def main():
    controller = FlightControl()

    for instruction in stdin:
        instruction = instruction.strip()

        if instruction == "registrar":
            flight = int(input())
            destination = tuple(input().split())
            date = Data(input())
            price = float(input())

            flight = Voo(flight, destination, date, price)
            controller.add(flight)
        elif instruction == "alterar":
            flight, price = input().split()
            flight = int(flight)
            price = float(price)

            controller[flight].price = price
        elif instruction == "cancelar":
            flight = int(input())
            del controller[flight]
        elif instruction == "planejar":
            airport = input()
            date_o, date_f = map(Data, input().split())

            flights = controller.flights_for(airport)
            candidate_flights = {}

            for flight in flights:
                if flight.date - date_o <= 0:
                    continue

                destination = flight.route[1]

                # pega somente o primeiro com o destino, pois estão ordenados
                if destination not in candidate_flights:
                    candidate_flights[destination] = flight

            best_trip = None
            best_price = None

            for (destination, first_flight) in candidate_flights.items():
                last_flight = None

                for flight in controller.flights_for(destination):
                    if date_f - flight.date <= 0 or flight.date - first_flight.date < 4:
                        continue

                    if flight.route[1] == airport:
                        last_flight = flight
                        break

                if not last_flight:
                    continue # voo de volta nao encontrado

                price = first_flight.price + last_flight.price

                if not best_trip or best_price > price:
                    best_trip = (first_flight, last_flight)
                    best_price = price

            print(*best_trip, sep="\n")

@dataclass
class Voo:
    _flight: int
    _route: tuple[str, str]
    _date: Data
    _price: int

    def __init__(self, flight: int, route: tuple[str, str], date: Data, price: int | float):
        self._flight = flight
        self._route = route
        self._date = date

        if type(price) == float:
            price = int(price * 100)

        self._price = price

    @property
    def flight(self):
        return self._flight

    @property
    def route(self):
        return self._route

    @property
    def date(self):
        return self._date

    @property
    def price(self):
        return self._price / 100

    @price.setter
    def price(self, new_price: int | float):
        if type(new_price) == float:
            new_price = int(new_price * 100)

        print(f"{self.flight} valor alterado de {self.price} para {new_price / 100}")
        self._price = new_price

    def __str__(self) -> str:
        return str(self.flight)

@dataclass
class FlightControl:
    _flights: dict[str, Voo]
    _routes: dict[str, list[str]]

    def __init__(self):
        self._flights = {}
        self._routes = {}

    def __getitem__(self, flight: str):
        return self._flights[flight]

    def __delitem__(self, flight: str):
        it = self._flights[flight] # raises
        del self._flights[flight]

        if len(self._routes[it.route[0]]) > 1:
            self._routes[it.route[0]].remove(flight)
        else:
            del self._routes[it.route[0]]

    def add(self, new_flight: Voo):
        self._flights[new_flight.flight] = new_flight

        if (start := new_flight.route[0]) in self._routes:
            self._routes[start].append(new_flight.flight)
            self._routes[start].sort(key=lambda voo: self._flights[voo].price)
        else:
            self._routes[start] = [new_flight.flight]

    def flights_for(self, airport: str):
        return list(map(lambda flight_id: self._flights[flight_id], self._routes[airport]))

# Aqui em baixo fica a sua solucao

if __name__ == "__main__":
    main()
