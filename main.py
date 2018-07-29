
class InvalidRouteConfiguration(Exception):
    pass


class NoSuchRoute(Exception):
    pass


class Stop(object):

    def __init__(self, name):
        self.name = name


class Setup(object):
    def __init__(self, config):
        try:
            paths = [p.strip() for p in config.split(',')]
            self.routes = {p[0]: dict() for p in paths}
            for p in paths:
                self.routes[p[0]][p[1]] = int(p[2:])
        except ValueError:
            raise InvalidRouteConfiguration('')

    def get_distance(self, route):
        stops = route.split('-')
        paths = []
        for i in range(0, len(stops)-1):
            paths.append((stops[i], stops[i+1]))
        try:
            return sum(self.routes[start][end] for start, end in paths)
        except KeyError:
            raise NoSuchRoute

    def __x(self, start, end, visited, stops):
        if stops < 0:
            return []
        stops -= 1
        trips = []
        for x in self.routes.get(start, dict()).keys():
            edge = '{}-{}'.format(start, x)
            if x == end:
                # print visited, edge, stops
                trips += [stops]
            trips += self.__x(x, end, visited + [edge], stops)
        return trips

    def get_number_of_trips_with_max_steps(self, route, max_stops):
        start, end = route.split('-')
        visited = []
        return len([stops for stops in self.__x(start, end, visited, max_stops) if stops >= 0])

    def get_number_of_trips_with_exact_stops(self, route, stops):
        start, end = route.split('-')
        visited = []
        return len([s for s in self.__x(start, end, visited, stops) if s == 0])


def print_distance(route):
    try:
        print setup.get_distance(route)
    except NoSuchRoute:
        print 'NO SUCH ROUTE'


def print_number_of_trips_with_max_stops(route, stops):
    try:
        print setup.get_number_of_trips_with_max_steps(route, stops)
    except NoSuchRoute:
        print 'NO SUCH ROUTE'


def print_number_of_trips_with_exact_stops(route, stops):
    try:
        print setup.get_number_of_trips_with_exact_stops(route, stops)
    except NoSuchRoute:
        print 'NO SUCH ROUTE'


if __name__ == '__main__':
    route = 'AB5, BC4, CD8, DC8, DE6, AD5, CE2, EB3, AE7'
    setup = Setup(route)
    print_distance('A-B-C')
    print_distance('A-D')
    print_distance('A-D-C')
    print_distance('A-E-B-C-D')
    print_distance('A-E-D')
    print_number_of_trips_with_max_stops('C-C', 3)
    print_number_of_trips_with_exact_stops('A-C', 4)
