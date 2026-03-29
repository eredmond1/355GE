/******************************************************************************
 * Name: main.cpp
 * Purpose: Refactored version of Koname player from Python to C++
 * Author(s): Nolan Schlacht
 * Last Modified: 28/03/26
 */

// Standard libraries
#include <iostream>
#include<string>
#include<fstream>
#include<vector>

using namespace std;

// Global variables
string player;

/*
 * Loads Koane board from text file into a vector of character vectors.
 * Param: filename - String for filepath to Konane board text file.
 * Return: board - A 2D vector of characters representing board pieces
 */
vector<vector<char>> load_board(string filename){
	vector<vector<char>> board;
	ifstream infile(filename);

	if(!infile){
		cerr << "Failed to open file: " << filename << endl;
		return board;
	}

	string line;
	while(getline(infile, line)){
		if(!line.empty()){
			vector<char> row(line.begin(), line.end());
			board.push_back(row);
		}
	}

	return board;
}

int main(int argc, char* argv[]) {
	if (argc != 3){
		cerr << "Invalid argument count. argc = " << argc << "." << endl; 
	}

	string board_file = argv[1];
	player = argv[2];

	vector<vector<char>>board = load_board(board_file);

	/*
	// Test loading board
	for(const auto& row : board){
		for(char c : row){
			cout << c;
		}
		cout << endl;
	}
	*/

	//Next

	return 0;	
}
