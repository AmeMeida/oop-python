# RA 210000

# Se necessario importe suas bibliotecas aqui
from dataclasses import dataclass
from sys import stdin
from data import Data

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

            if flight in controller:
                controller[flight].price = price
            else:
                print("Voo nao encontrado")
        elif instruction == "cancelar":
            flight = int(input())
            del controller[flight]
        elif instruction == "planejar":
            airport = input()
            date_o, date_f = map(Data, input().split())

            trips = controller.plan_trip(date_o, date_f, airport)

            if len(trips):
                print(*trips[0], sep="\n")
            else:
                print("Voo nao encontrado")

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
    _routes: dict[str, list[Voo]]

    def __init__(self):
        self._flights = {}
        self._routes = {}

    def __getitem__(self, flight: str):
        return self._flights[flight]

    def __delitem__(self, flight: str):
        it = self._flights[flight] # raises
        del self._flights[flight]

        if len(self._routes[it.route[0]]) > 1:
            self._routes[it.route[0]].remove(it)
        else:
            del self._routes[it.route[0]]

    def __contains__(self, flight: str):
        return flight in self._flights

    def add(self, new_flight: Voo):
        self._flights[new_flight.flight] = new_flight

        if (start := new_flight.route[0]) in self._routes:
            self._routes[start].append(new_flight)
            self._routes[start].sort(key=lambda voo: voo.date.days)
        else:
            self._routes[start] = [new_flight]

    def flights_for(self, airport: str):
        if airport in self._routes:
            return self._routes[airport][:]
        else:
            return []

    def plan_trip(self, date_o: Data, date_f: Data, airport: str):
            trips: list[tuple[Voo, Voo]] = []

            for first_flight in self.flights_for(airport):
                if first_flight.date - date_o < 0 or date_f - first_flight.date < 4:
                    continue

                destination = first_flight.route[1]

                for back_flight in self.flights_for(destination):
                    if back_flight.route[1] != airport \
                        or date_f - back_flight.date < 0 \
                        or back_flight.date - first_flight.date < 4:
                        continue

                    trips.append((first_flight, back_flight))

            trips.sort(key=lambda route: route[0].price + route[1].price)
            return trips

# Aqui em baixo fica a sua solucao

if __name__ == "__main__":
    main()
