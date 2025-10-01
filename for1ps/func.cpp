#include "func.h"
#include <cmath>
using std::max;
using std::min;

const double eps = 0.00001;

void read_point(Point& p) {
    cin >> p.x >> p.y;
}
void print_point(const Point& p) {
    cout << "(" << p.x << ", " << p.y << ")";
}

void read_circle(Circle& c) {
    read_point(c.center);
    cin >> c.radius;
}
void print_circle(const Circle& c) {
    print_point(c.center);
    cout << " ;radius: " << c.radius << "; ";
}
double circle_circuit(const Circle& c) {
    return 2 * 3.14159265 * c.radius;
}
double circle_area(const Circle& c) {
    return 3.14159265 * c.radius * c.radius;
}

void read_square(Square& s) {
    read_point(s.top_left_p);
    cin >> s.side;
}
void print_square(const Square& s) {
    print_point(s.top_left_p);
    cout << " ;side: " << s.side << "; ";
}
double square_perimeter(const Square& s) {
    return 4 * s.side;
}
double square_area(const Square& s) {
    return s.side * s.side;
}


bool are_points_intersecting(const Point& p1, const Point& p2){
    return fabs(p1.x - p2.x) < eps && fabs(p1.y - p2.y) < eps;
}


bool point_in_circle(const Point& p, const Circle& c){
    double vec_x = p.x - c.center.x;
    double vec_y = p.y - c.center.y;
    double rad = c.radius;
    return vec_x * vec_x + vec_y * vec_y < rad * rad - eps;
}
bool point_in_square(const Point& p, const Square& s){
    return p.x > s.top_left_p.x + eps &&
           p.x < s.top_left_p.x + s.side - eps &&
           p.y < s.top_left_p.y - eps && 
           p.y > s.top_left_p.y - s.side + eps;
}


bool point_on_circle(const Point& p, const Circle& c){
    double vec_x = p.x - c.center.x;
    double vec_y = p.y - c.center.y;
    return fabs(sqrt(vec_x*vec_x + vec_y*vec_y) - c.radius) < eps;
}
bool point_on_square(const Point& p, const Square& s){
    //left
    if (fabs(p.x - s.top_left_p.x) < eps && 
        p.y <= s.top_left_p.y + eps && p.y >= s.top_left_p.y - s.side - eps){
    return true;
    }
    //right
    if (fabs(p.x - (s.top_left_p.x + s.side)) < eps && 
        p.y <= s.top_left_p.y + eps && p.y >= s.top_left_p.y - s.side - eps){
    return true;
    }
    //upper
    if (fabs(p.y - s.top_left_p.y) < eps && 
        p.x >= s.top_left_p.x - eps && p.x <= s.top_left_p.x + s.side + eps){
    return true;
    }
    //under
    if (fabs(p.y - (s.top_left_p.y - s.side)) < eps && 
        p.x >= s.top_left_p.x - eps && p.x <= s.top_left_p.x + s.side + eps){
    return true;
    }

    return false;
}


bool circles_intersect(const Circle& c1, const Circle& c2){
    double vec_x = c1.center.x - c2.center.x;
    double vec_y = c1.center.y - c2.center.y;
    return sqrt(vec_x * vec_x + vec_y * vec_y) < c1.radius + c2.radius + eps &&
           sqrt(vec_x * vec_x + vec_y * vec_y) > fabs(c1.radius - c2.radius) - eps;
}
bool squares_intersect(const Square& s1, const Square& s2){
    double x1 = s1.top_left_p.x;
    double y1 = s1.top_left_p.y;
    double x2 = s2.top_left_p.x;
    double y2 = s2.top_left_p.y;
    return x1 < x2 + s2.side + eps &&
           x1 + s1.side + eps > x2 &&
           y1 + eps > y2 - s2.side &&
           y1 - s1.side < y2 + eps; 
}
bool circleSquare_intersect(const Circle& c, const Square& s){
    double close_x = max(s.top_left_p.x, min(c.center.x, s.top_left_p.x + s.side));
    double close_y = min(s.top_left_p.y, max(c.center.y, s.top_left_p.y - s.side));
    double vec_x = c.center.x - close_x;
    double vec_y = c.center.y - close_y;
    return vec_x * vec_x + vec_y * vec_y < c.radius * c.radius +eps;
}


bool circle_in_circle(const Circle& small_c, const Circle& big_c){
    double vec_x = small_c.center.x - big_c.center.x;
    double vec_y = small_c.center.y - big_c.center.y;
    return sqrt(vec_x * vec_x + vec_y * vec_y) + small_c.radius < big_c.radius + eps;
}
bool square_in_square(const Square& small_s, const Square& big_s){
    double s_x = small_s.top_left_p.x;
    double s_y = small_s.top_left_p.y;
    double b_x = big_s.top_left_p.x;
    double b_y = big_s.top_left_p.y;
    return s_x > b_x - eps &&
           s_x + small_s.side < b_x + big_s.side + eps &&
           s_y < b_y + eps &&
           s_y - small_s.side > b_y - big_s.side - eps;
}
bool square_in_circle(const Square& s, const Circle& c){
    double c_x = c.center.x;
    double c_y = c.center.y;
    double x_1 = s.top_left_p.x;
    double x_2 = s.top_left_p.x + s.side;
    double y_1 = s.top_left_p.y;
    double y_3 = s.top_left_p.y - s.side;
    double f1 = sqrt((c_x - x_1)*(c_x - x_1) + (c_y - y_1)*(c_y - y_1));
    double f2 = sqrt((c_x - x_2)*(c_x - x_2) + (c_y - y_1)*(c_y - y_1));
    double f3 = sqrt((c_x - x_2)*(c_x - x_2) + (c_y - y_3)*(c_y - y_3));
    double f4 = sqrt((c_x - x_1)*(c_x - x_1) + (c_y - y_3)*(c_y - y_3));

    double dist = max(max(f1, f2), max(f3, f4));
    return dist < c.radius - eps;
}

bool circle_in_square(const Circle& c, const Square& s){    
    double dist_to_left = c.center.x - s.top_left_p.x;
    double dist_to_right = (s.top_left_p.x + s.side) - c.center.x;
    double dist_to_top = s.top_left_p.y - c.center.y;
    double dist_to_bottom = c.center.y - (s.top_left_p.y - s.side);
    
    // Все расстояния должны быть БОЛЬШЕ радиуса круга
    return (dist_to_left > c.radius - eps) &&
           (dist_to_right > c.radius - eps) &&
           (dist_to_top > c.radius - eps) &&
           (dist_to_bottom > c.radius - eps);
}



