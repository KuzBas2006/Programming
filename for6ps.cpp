#include <iostream>
#include <stdexcept> 
using namespace std;

class DynamicArray {
    int *parr;
    int size;
    public:
        DynamicArray(int arr_size){
        size = arr_size;
        parr = new int[size];
        }
        ~DynamicArray(){
            delete []parr;
        }

        void print(){
            for (int i = 0; i < size; i++){
                cout << parr[i] << " " << endl;
            }
        }
        
        void set(int value, int index){
            if (index < 0 || index >= size){
                throw out_of_range("Index out of bounds!");
            }
            if (value < -100 || value > 100){
                throw invalid_argument("Value is not in range from -100 to 100!");
            }
            parr[index] = value;
        }
        
        int get(int index){
            if (index < 0 || index >= size){
                throw out_of_range("Index out of bounds!");
            }
            return parr[index];
        }
        //Конструктор копирования
        DynamicArray(const DynamicArray& other){
            size = other.size;
            parr = new int[size];
            for (int i = 0; i < size; i++){
                parr[i] = other.parr[i];
            }
        }
        //Добавление в конец
        void addToEnd(int new_value){
            if (new_value < -100 || new_value > 100){
                throw invalid_argument("Value is not in range from -100 to 100!");
            }
            int *new_parr = new int[size + 1];
            for (int i = 0; i < size; i++){
                new_parr[i] = parr[i];
            }
            new_parr[size] = new_value;
            delete []parr;
            parr = new_parr;
            size = size + 1;
            cout << "Add new value in the end: " << new_value << endl;
        }
        //Сложение и вычитание массивов
        void add(const DynamicArray& other) {
            for (int i = 0; i < size; i++) {
                if (i < other.size) {
                    parr[i] = parr[i] + other.parr[i];
                }
            }
        }
        void subtract(const DynamicArray& other) {
            for (int i = 0; i < size; i++) {
                if (i < other.size) {
                    parr[i] = parr[i] - other.parr[i];
                }
            }
        }
    
};

int main(){
    DynamicArray arr(10);
    
    for (int i = 0; i < 10; i++){
        try {
            arr.set(i+1, i);
        } catch (const exception& e) {
            cerr << e.what() << endl;
        }
    }
    // Проверка работы на примере get и set
    try {
        arr.get(20);
    } catch (const out_of_range& e) {       // Коммент из throw в геттере
        cerr << e.what() << endl;
    }
    
    try {
        arr.set(101, 1);
    } catch (const invalid_argument& e) {   // Коммент из throw в сеттере
        cerr << e.what() << endl;
    }
    return 0;
}