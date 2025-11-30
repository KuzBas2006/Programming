#include <iostream>
#include <chrono>
#include <fstream>
#include <iomanip>
#include <sstream>

using namespace std;

class DynamicArray {
    protected:
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
                cout << "Index out of bounds!" << endl;
                return;
            }
            if (value < -100 || value > 100){
                cout << "Value is not in range from -100 to 100!" << endl;
                return;
            }
            parr[index] = value;
        }
        
        int get(int index){
            if (index < 0 || index >= size){
                cout << "Index out of bounds!" << endl;
                return 0;
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
                cout << "Value is not in range from -100 to 100!" << endl;
                return;
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

// Абстрактный класс для работы с файламим
class FileArray: public DynamicArray {
    protected:
        string last_filename;
    public:
        using DynamicArray::DynamicArray;

        virtual void save_to_file() = 0;  // Виртуальная функция, чтобы вызывать правильную save_to_file
    
        // Метод для получения имени последнего файла
        string get_last_filename() const {
            return last_filename;
        }
    protected:
        string get_current_time(){
            auto now = chrono::system_clock::now();
            auto time_t = chrono::system_clock::to_time_t(now); // Передаем время
            stringstream ss;
            ss << put_time(localtime(&time_t), "%Y-%m-%d_%H-%M-%S");
            return ss.str();
        }
};

// Класс для перевода и сохранения в txt 
class ArrTxt: public FileArray{
    public:
        using FileArray::FileArray;
        
        void save_to_file() override{
            last_filename = get_current_time() + ".txt"; 
            ofstream file(last_filename);
            for (int i = 0; i < size; i++){
                file << parr[i] << endl;
            }
            file.close();
        }
};

// Класс для перевода и сохранения в csv 
class ArrCsv: public FileArray{
    public:
        using FileArray::FileArray;
        
        void save_to_file() override{
            last_filename = get_current_time() + ".csv";  
            ofstream file(last_filename);
            for (int i = 0; i < size; i++){
                file << parr[i];
                if (i < size - 1) {
                    file << ",";
                }
            }
            file.close();
        }
};

// Вывод содержимого файла
void print_file_content(const string& filename) {
    ifstream file(filename);
    if (!file.is_open()) {
        cout << "ERROR: Cannot open file " << filename << endl;
        return;
    }
    string line;
    while (getline(file, line)) {
        cout << line << endl;
    }
    file.close();
}

int main(){
    // DynamicArray arr(3);
    // //Задание 1
    // arr.set(3, 0);
    // arr.set(5, 1);
    // arr.set(7, 2);
    // cout << "First array: " << endl ;
    // arr.print();

    // //Задание 2
    // DynamicArray arr2 = arr;
    // cout << "Copied array: " << endl;
    // arr2.print();
    
    // //Задание 3
    // arr.addToEnd(9);
    // cout << "After adding to end: " << endl;
    // arr.print();
    
    // //Задание 4
    // cout << "===================================================================" << endl;
    // DynamicArray arr3(3);
    // arr3.set(5, 0);
    // arr3.set(7, 1);
    // arr3.set(9, 2);
    
    // DynamicArray arr4 = arr;
    // cout << "First array: " << endl;
    // arr.print();
    // cout << "Second array: " << endl;
    // arr3.print();

    // cout << "===================================================================" << endl;
    // arr.add(arr3);
    // cout << "After addition: " << endl;
    // arr.print();
    
    // cout << "===================================================================" << endl;
    // arr4.subtract(arr3);
    // cout << "After subtraction: " << endl;
    // arr4.print();
    cout << "FILE SAVING TEST:" << endl << endl;
    
    ArrTxt txtArray(3);  
    ArrCsv csvArray(3);  
    txtArray.set(3, 0);
    txtArray.set(5, 1);
    txtArray.set(7, 2);

    csvArray.set(2, 0);
    csvArray.set(4, 1);
    csvArray.set(6, 2);

    // Прямой вызов
    cout << "====== DIRECT CALL ======" << endl << endl;

    txtArray.save_to_file();

    string txt_filename = txtArray.get_last_filename();
    cout << "Checking file: " << txt_filename << ":" << endl;
    print_file_content(txt_filename);

    csvArray.save_to_file();  
    
    string csv_filename = csvArray.get_last_filename();
    cout << "Checking file " << csv_filename << ":" << endl;
    print_file_content(csv_filename);

    
    // Полиморфный вызов
    cout << "\n====== POLYMORPHIC CALL ======" << endl << endl;

    FileArray* arrays[] = {&txtArray, &csvArray}; 
    for (int i = 0; i < 2; i++){
        arrays[i]->save_to_file(); // Полиморфный вызов

        string poly_filename = arrays[i]->get_last_filename();
        cout << "Polymorphic call created: " << poly_filename << endl;
        print_file_content(poly_filename);
    }

    return 0;
}