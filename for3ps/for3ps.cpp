#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <random>
#include <algorithm>
#include <cmath>

using namespace std;

struct PGMImage {
    int width, height, max_value;
    vector<vector<int>> pixel_data;
};

struct ProcessingResult {
    string filename;
    double mean_squared_error;
    double peak_snr;
    double mean_absolute_error;
};

void addRandomNoise(PGMImage* image, int noise_pixels) {
    random_device rd;
    mt19937 gen(rd());
    uniform_int_distribution<> value_dist(0, image->max_value);
    
    for (int i = 0; i < noise_pixels; i++) {
        int random_row = rand() % image->height;
        int random_col = rand() % image->width;
        image->pixel_data[random_row][random_col] = value_dist(gen);
    }
}

void writePGMFile(const PGMImage& image, const string& filepath) {
    ofstream file(filepath);
    if (!file) {
        throw runtime_error("Cannot create file: " + filepath);
    }
    
    file << "P2\n";
    file << image.width << " " << image.height << "\n";
    file << image.max_value << "\n";
    
    for (int row = 0; row < image.height; row++) {
        for (int col = 0; col < image.width; col++) {
            file << image.pixel_data[row][col];
            if (col < image.width - 1) file << " ";
        }
        file << "\n";
    }
    
    file.close();
    cout << "Created: " << filepath << endl;
}

void applyMedianFilter(PGMImage* image, int window_size) {
    if (window_size % 2 == 0) {
        cout << "Filter size must be odd number" << endl;
        return;
    }

    int border = window_size / 2;
    vector<vector<int>> original_data = image->pixel_data;

    for (int y = border; y < image->height - border; y++) {
        for (int x = border; x < image->width - border; x++) {
            vector<int> neighborhood_values;
            
            for (int dy = -border; dy <= border; dy++) {
                for (int dx = -border; dx <= border; dx++) {
                    neighborhood_values.push_back(original_data[y + dy][x + dx]);
                }
            }
            
            sort(neighborhood_values.begin(), neighborhood_values.end());
            image->pixel_data[y][x] = neighborhood_values[neighborhood_values.size() / 2];
        }
    }
}

PGMImage loadPGMFile(const string& filename) {
    ifstream file(filename);
    if (!file) {
        throw runtime_error("Cannot open PGM file: " + filename);
    }
    
    PGMImage image;
    string format_line;
    
    getline(file, format_line);
    if (format_line != "P2") {
        throw runtime_error("Not a P2 PGM file: " + filename);
    }
    
    // Skip comments
    string line;
    while (file.peek() == '#' || file.peek() == '\n') {
        getline(file, line);
    }
    
    file >> image.width >> image.height >> image.max_value;
    
    cout << "Loading PGM: " << image.width << "x" << image.height 
         << ", max=" << image.max_value << endl;
    
    image.pixel_data.resize(image.height, vector<int>(image.width));
    
    for (int i = 0; i < image.height; i++) {
        for (int j = 0; j < image.width; j++) {
            if (!(file >> image.pixel_data[i][j])) {
                throw runtime_error("Error reading PGM pixel data");
            }
        }
    }
    
    file.close();
    return image;
}

ProcessingResult analyzeResults(const PGMImage& original, const PGMImage& processed, const string& name) {
    ProcessingResult result;
    result.filename = name;
    
    double squared_error_sum = 0.0;
    double absolute_error_sum = 0.0;
    int total_pixels = original.width * original.height;
    
    for (int i = 0; i < original.height; i++) {
        for (int j = 0; j < original.width; j++) {
            int difference = original.pixel_data[i][j] - processed.pixel_data[i][j];
            squared_error_sum += difference * difference;
            absolute_error_sum += abs(difference);
        }
    }
    
    result.mean_squared_error = squared_error_sum / total_pixels;
    result.mean_absolute_error = absolute_error_sum / total_pixels;
    
    if (result.mean_squared_error > 0) {
        result.peak_snr = 20 * log10(255.0 / sqrt(result.mean_squared_error));
    } else {
        result.peak_snr = 100.0; // Perfect match
    }
    
    return result;
}

void generateReport(const vector<ProcessingResult>& results, const string& report_filename) {
    ofstream file(report_filename);
    file << "Image,MSE,PSNR,MAE\n";
    for (const auto& result : results) {
        file << result.filename << "," 
             << result.mean_squared_error << "," 
             << result.peak_snr << "," 
             << result.mean_absolute_error << "\n";
    }
    file.close();
    cout << "Report saved: " << report_filename << endl;
}

int main() {
    vector<string> pgm_files = {"image1.pgm", "image2.pgm", "image3.pgm", "image4.pgm", "image5.pgm"};
    vector<ProcessingResult> all_results;
    
    cout << "=== PGM Image Noise Filtering ===" << endl;
    
    for (const auto& filename : pgm_files) {
        cout << "\nProcessing: " << filename << endl;
        
        try {
            string input_path = "input/" + filename;
            PGMImage original_image = loadPGMFile(input_path);
            
            // Create noisy version
            PGMImage noisy_image = original_image;
            int noise_count = (original_image.width * original_image.height) * 0.05;
            addRandomNoise(&noisy_image, noise_count);
            writePGMFile(noisy_image, "output/noisy_" + filename);
            
            // Test different filter sizes
            vector<int> filter_sizes = {3, 5, 7};
            
            for (int filter_size : filter_sizes) {
                PGMImage filtered_image = noisy_image;
                applyMedianFilter(&filtered_image, filter_size);
                
                string output_name = "filtered_" + to_string(filter_size) + "_" + filename;
                writePGMFile(filtered_image, "output/" + output_name);
                
                ProcessingResult metrics = analyzeResults(original_image, filtered_image, output_name);
                all_results.push_back(metrics);
                
                cout << "  Filter " << filter_size << "x" << filter_size 
                     << " - PSNR: " << metrics.peak_snr << " dB" << endl;
            }
            
            cout << "Completed: " << filename << endl;
            
        } catch (const exception& e) {
            cout << "ERROR with " << filename << ": " << e.what() << endl;
        }
    }
    
    if (!all_results.empty()) {
        generateReport(all_results, "pgm_analysis_report.csv");
        cout << "\n=== Processing Complete ===" << endl;
        cout << "Check 'output' folder for processed PGM files" << endl;
        cout << "Check 'pgm_analysis_report.csv' for results" << endl;
    } else {
        cout << "\nNo PGM files were processed successfully" << endl;
    }
    
    return 0;
}
