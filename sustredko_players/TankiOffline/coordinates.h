#ifndef CPP_COORDINATES
#define CPP_COORDINATES
#include "common.h"




long double squared_distance(Coordinates &lhs, const Coordinates &rhs) ;

long double distance(Coordinates &lhs, const Coordinates &rhs) ;

std::istream &operator>>(std::istream &in, Coordinates &rhs) ;

std::ostream &operator<<(std::ostream &out, const Coordinates &rhs) ;

long double angle_to(Coordinates &lhs, Coordinates &rhs);

struct line{
    Coordinates A,B;
    long double cross(const Coordinates &lhs,const Coordinates &rhs){
        return lhs.x*rhs.y - lhs.y*lhs.y;
    }

    Coordinates intersect(line a,line b){
        long double t = (a.A.x - b.A.x)*(b.A.y - b.B.y) - (a.A.y - b.A.y)*(b.A.x - b.B.x);
        t /= (a.A.x - a.B.x)*(b.A.y - b.B.y) - (a.A.y - a.B.y)*(b.A.x - b.B.x);
        Coordinates ret(a.A.x + t*(a.B.x - a.A.x),a.A.y + t*(a.B.y - a.A.y));
        return ret;
    }
};


#endif //CPP_COORDINATES
