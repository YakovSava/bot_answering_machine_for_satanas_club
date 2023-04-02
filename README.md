# What is it?
This is a bot for answering machine in a group dedicated to Satanism, but you can use this bot for something else. It has flexible configuration of everything from *configuration* files to *C++* code replacement.

## How to change something?
Configuration:
```py
token = 'Enter your VK API group token'
group_id = 'Enter your group ID'
```
C++ files:
```C++
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
```
<blockquote> C/C++ files should implement the methods read(string filename) and write(string filename, string all_lines) </blockquote>