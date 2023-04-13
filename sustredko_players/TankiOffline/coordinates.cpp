#include "coordinates.h"

long double squared_distance(Coordinates &lhs, const Coordinates &rhs) {
    return abs(lhs - rhs);
}

long double distance(Coordinates &lhs, const Coordinates &rhs) {
    return std::sqrt(squared_distance(lhs, rhs));
}

std::istream &operator>>(std::istream &in, Coordinates &rhs) {
    long double a, b;
    in >> a >> b;
    rhs = Coordinates{a,b};
    return in;
}

std::ostream &operator<<(std::ostream &out, const Coordinates &rhs) {
    out << rhs.x << ' ' << rhs.y;
    return out;
}

long double angle_to(Coordinates &lhs, Coordinates &rhs){
    Coordinates v = rhs - lhs;
    return atan2(v.y,v.x);
}
