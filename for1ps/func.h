#ifndef FUNC_H
#define FUNC_H
#include "structs.h"

//функции ввода-вывода для точек
void read_point(Point& p);
void print_point(const Point& p);

//функции ввода-вывода и вычислений для кругов
void read_circle(Circle& c);
void print_circle(const Circle& c);
double circle_circuit(const Circle& c);
double circle_area(const Circle& c);

//функции ввода-вывода и вычислений для квадратов
void read_square(Square& s);
void print_square(const Square& s);
double square_perimeter(const Square& s);
double square_area(const Square& s);

//проверка точек на пересечение
bool are_points_intersecting(const Point& p1, const Point& p2); //ссылку на переменные p1 и p2 из структуры Point с припиской const, чтобы не изменить передаваемые данные

//принадлежность точки к фигуре
bool point_in_circle(const Point& p, const Circle& c);
bool point_in_square(const Point& p, const Square& s);

//точка на контуре
bool point_on_circle(const Point& p, const Circle& c);
bool point_on_square(const Point& p, const Square& s);

//пересецение фигур
bool circles_intersect(const Circle& c1, const Circle& c2);
bool squares_intersect(const Square& s1, const Square& s2);
bool circleSquare_intersect(const Circle& c, const Square& s);

//принадлежность фигур
bool circle_in_circle(const Circle& small_c, const Circle& big_c);
bool square_in_square(const Square& small_s, const Square& big_s);
bool square_in_circle(const Square& s, const Circle& c);
bool circle_in_square(const Circle& c, const Square& s);

#endif

