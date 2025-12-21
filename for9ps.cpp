#include <iostream>
#include <stdexcept>
#include <cmath>
#include <vector>
#include <typeinfo>

using namespace std;

template<typename T>
class Array {
    vector<T> arr;
    
public:
    Array() {}
    Array(int size) : arr(size) {}

    // (1) Сеттер
    void setValue(int index, T value) {
        if (index < 0 || index >= arr.size()) {
            throw out_of_range("Index out of range");
        }
        // Проверка только для числовых типов
        if (typeid(T) == typeid(int) || 
            typeid(T) == typeid(double) || 
            typeid(T) == typeid(float)) {
            if (value < -100 || value > 100) {
                throw invalid_argument("Value must be between -100 and 100");
            }
        }
        arr[index] = value;
    }
    int getSize() const {
        return arr.size();
    }
    // (2) Оператор вывода массива
    friend ostream& operator<<(ostream& os, const Array<T>& obj) {
        os << "[";
        for (int i = 0; i < obj.arr.size(); i++) {
            os << obj.arr[i];
            if (i != obj.arr.size() - 1) os << ", ";
        }
        os << "]";
        return os;
    }
    // (3) Евклидово расстояние
    double distance(const Array<T>& other) const {
        if (arr.size() != other.arr.size()) {
            throw invalid_argument("Arrays must have same size");
        }
        
        // Только для числовых типов
        if (typeid(T) != typeid(int) && 
            typeid(T) != typeid(double) && 
            typeid(T) != typeid(float)) {
            throw bad_typeid();
        }
        double sum = 0;
        for (int i = 0; i < arr.size(); i++) {
            double diff = static_cast<double>(arr[i]) - static_cast<double>(other.arr[i]);
            sum += diff * diff;
        }
        return sqrt(sum);
    }
};
int main() {
    try {
        Array<int> arr1(3);
        arr1.setValue(0, 10);
        arr1.setValue(1, 20);
        arr1.setValue(2, 30);
        
        Array<int> arr2(3);
        arr2.setValue(0, 5);
        arr2.setValue(1, 15);
        arr2.setValue(2, 25);
        
        cout << "Array 1: " << arr1 << endl;
        cout << "Array 2: " << arr2 << endl;
        cout << "Distance: " << arr1.distance(arr2) << endl;
        
    } catch (const bad_typeid&) {
        cerr << "Error: non-numeric type" << endl;
    } catch (const exception& e) {
        cerr << "Error: " << e.what() << endl;
    }
    
    return 0;
}