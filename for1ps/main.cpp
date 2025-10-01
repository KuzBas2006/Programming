#include <iostream>
#include "func.h"
#include "structs.h"
using namespace std;

int main() {
    Point p1, p2, p;
    Circle c1, c2;
    Square s1, s2;

    read_point(p1);
    read_point(p2);
    read_point(p);
    read_circle(c1);
    read_circle(c2);
    read_square(s1);
    read_square(s2);

    cout << " " << endl;
    cout << "1 - belong / yes" << endl;
    cout << "0 - don't belong / no" << endl;
    cout << " " << endl;
 
    cout << "Points intersect: " << are_points_intersecting(p1, p2) << endl;
    
    cout << "Point in circle 1: " << point_in_circle(p, c1) << endl;
    cout << "Point on circle 1: " << point_on_circle(p, c1) << endl;
    
    cout << "Point in square 1: " << point_in_square(p, s1) << endl;
    cout << "Point on square 1: " << point_on_square(p, s1) << endl;
    
    cout << "Circles intersect: " << circles_intersect(c1, c2) << endl;
    cout << "Squares intersect: " << squares_intersect(s1, s2) << endl;
    cout << "Circle and square intersect: " << circleSquare_intersect(c1, s1) << endl;
    
    cout << "Circle in circle: " << circle_in_circle(c1, c2) << endl;
    cout << "Square in square: " << square_in_square(s1, s2) << endl;
    cout << "Square in circle: " << square_in_circle(s1, c1) << endl;
    cout << "Circle in square: " << circle_in_square(c1, s1) << endl;

    return 0;
}


