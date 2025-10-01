#ifndef STRUCTS_H
#define STRUCTS_H
#include <iostream>
#include <cmath>
using namespace std;

struct Point{
    double x, y; 
};

struct Circle{
    Point center;
    double radius;
};

struct Square{
    Point top_left_p;
    double side;
};
#endif