/******************************************************************************
 * Name: main.cpp
 * Purpose: Refactored version of Koname player from Python to C++
 * Author(s): Nolan Schlacht
 * Last Modified: 28/03/26
 */

// Standard libraries
#include <iostream>
#include <string>
#include <fstream>
#include <vector>
#include <set>
#include <utility>
#include <typeinfo>

using namespace std;

// Global variables
char BLACK = 'B';
char WHITE = 'W';
char EMPTY = 'O'; // use whatever matches the board/checker
int SIZE = 8;
set<pair<int, int>> VALID_POSITIONS;
string PLAYER = "B";
string BE = "board_early.txt";
string BL = "board_late.txt";
string BM = "board_mid.txt";
string NONE = "None";

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

/*
 * Checks every position on board to check that there are no empty pieces
 * Param: board - A 2D vector of characters representing board pieces
 * Return: True is board is full, false if at least one piece is missing
 */
bool is_board_full(vector<vector<char>> board){
	for(const auto& row : board){
		for(const auto& col : row){
			if(col == EMPTY){
				return false;
			}
		}
	}
	return true;
}

/*
 * Selects an opening move for black or white player given a full board
 * Params: board - A 2D vector of characters representing board pieces
 *         player - String representing the color of player pieces
 * Return: String representing opening move position for black or white
 */
string find_opening_move(vector<vector<char>> board, string player){
	vector<string> center_stones = {"D5", "E5", "D4", "E4"};

	// First move: full board
	if(is_board_full(board)){
		if(player == "BLACK"){
			return "D5";
		} else {
			return "E5";
		}
	}
	return NONE;
}
/*
string find_best_move(vector<vector<char>> board, string player){

}
*/
/*
 * Calls functions to pick a move depending if board is empty or not
 * Params: board - A 2D vector of characters representing board pieces
 *         player - String representing the color of player pieces
 * Return: String representing coordinate of piece to move
 */
string choose_move(vector<vector<char>> board, string player){
	string opening_move = find_opening_move(board, player);
	// Not returning one of the opening moves returns a mangled string
	if(opening_move != NONE){
		return opening_move;
	}

	PLAYER = player;
	return "TBA";
	//return find_best_move(board, player);
}	

int main(int argc, char* argv[]) {
	// Quick population of VALID_POSITIONS
	for(int r = 0; r < SIZE; ++r){
		for(int c = 0; c < SIZE; ++c){
			VALID_POSITIONS.insert({r, c});
		}
	}

	if(argc != 3){
		cerr << "Invalid argument count. argc = " << argc << "." << endl; 
	}

	string board_file = argv[1];
	string player = argv[2];

	PLAYER = player;

	vector<vector<char>>board = load_board(board_file);

	// Test loading board
	for(const auto& row : board){
		for(char c : row){
			cout << c;
		}
		cout << endl;
	}

	/*
	// Testing for is_board_full
	bool isFull = is_board_full(board);
	cout << "Is the board full? " << isFull << endl; 

	// Testing opening move
	string o = find_opening_move(board, player);
	cout << "Opening move: " << o << endl;
	cout << "Type of move: " << typeid(o).name() << endl;
	*/
	string my_move = choose_move(board, player);
	cout << "Move: " << my_move << endl;

	return 0;	
}
