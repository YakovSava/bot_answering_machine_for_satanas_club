# include <fstream>
# include <string>
# include <iostream>
using namespace std;

string read(string filename) {
    string line, lines = "", endline = "\n";
    ifstream file;
    file.open(filename.c_str());
    if (file.is_open()) {
        while (getline(line, file)) lines = lines + line + endline;
    }
    return lines;
}

void write(string filename, string all_lines) {
    ofstream file;
    file.open(filename.c_str());
    if (file.is_open()) {
        file << all_lines.c_str() << endl;
    }
}