/******************************************************************************
 * Name: main.cpp
 * Purpose: Refactored version of Koname player from Python to C++
 * Author(s): Nolan Schlacht
 * Last Modified: 29/03/26
 *#############################################################################
 * IMPORTANT: IF THIS MESSAGE IS PRESENT, THEN THE CODE HAS NOT BEEN FULLY
 * ERROR CHECKED AFTER REFACTOR. CURRENT VERSION IS NOT VIABLE YET.
 *#############################################################################
 *****************************************************************************/

// Standard libraries
#include <iostream>
#include <string>
#include <fstream>
#include <vector>
#include <set>
#include <utility>
#include <cctype>
#include <cstdlib>
#include <unorder_map>
#include <algorithm>
#include <chrono>
#include <limits>
#include <typeinfo> // Remove at end

// Nmaespace and type aliases
using namespace std;
// Will use this once code working to simplify
//using Board = std::vector<std::vector<char>>;

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
string NONE_STR = "None";
chrono::steady_clock::time_point _ALPHABETA_START_TIME;
double _ALPHABETA_TIME_LIMIT = 10.0;
bool _ALPHABETA_TIMEOUT = false;

struct Replies {
	string move;
	pair<int, int> start;
	pair<int, int> end;
}

struct Move{
	string move;
	pair<int, int> start;
	pair<int, int> end;
	double eval_sum;
	Replies replies;
}

/*
 * Start alphabeta timer
 */
void start_alphabeta_timer(){
	_ALPHABETA_START_TIMER = chrono::steady_clock::now();
	_ALPHABETA_TIMEOUT = false;
}

/*
 * Checker if timer exceeded
 */
bool check_alphabeta_timeout() {
	auto now = chrono::steady_clock::now();
	chrono::duration<double> elapsed = now - _ALPHABETA_START_TIME;
	if(elapsed.count() >= _ALPHABETA_TIME_LIMIT){
		_ALPHABETA_TIMEOUT = true;
	}
	return _ALPHABETA_TIMEOUT;
}

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
 * Acquire row index value from chess coordinates
 * Param: coord - String representing chess coordinates
 * Return: Index of row value for 2D vector
 */
int coord_to_index_row(string coord){
	int convert = coord[1];
	convert = convert - 48;
	return SIZE - convert;
}

/*
 * Acquire column index value from chess coordinates
 * Param: coord - String representing chess coordinates
 * Return: Index of col value for 2D vector
 */
int coord_to_index_col(string coord){
	return toupper(coord[0]) - 'A';
}

/*
 * Takes a pair of index values can convert to chess coordinates
 * Params: row, col
 * Return: String representing chess board coordinates
 */
string index_to_coord(int row, int col){
	char letter = 'A' + col;
	string number = to_string(SIZE - row);
	return string(1, letter) + number;
}

/*
 * Formats start and end strings to single move string
 * Params: start - Starting coordinate string
 *         end - Ending coordinate string
 * Return: Concatenate the two strings with a hyphen
 */
string format_move(string start, string end){
	return start + "-" + end;
}

/*
 * Parses first coordinate from move string
 * Param: move_string - String representing movement between two coordinates
 * Return: String representing the first (starting) coordinate
 */
string parse_move_start(string move_string){
	size_t pos = move_string.find('-');

	if(pos == npos){
		return move_string;
	}else{
		return move_string.substr(0, pos);
	}
}

/*
 * Parses second coordinate from move string
 * Param: move_string - String representing movement between two coordinates
 * Return: String representing the second (ending) coordinate
 */
string parse_move_end(string move_string){
	size_t pos = move_string.find('-');

	if(pos == npos){
		return NONE_STR;
	}else{
		return move_string.substr(pos + 1);
	}
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
 * Counts the number of empty positions on the board
 * Param: board - A 2D vector of characters representing board pieces
 * Return: Integer number of 'empty' positions
 */
int count_empty(vector<vector<char>> board){
	int total = 0;

	for(const auto& row : board){
		for(const auto& col : row){
			if(col == EMPTY){
				total++;
			}
		}
	}
	return total;
}

/*
 * Determines if a piece needs to be removed and certain coordinates and does so
 * Params: board - A 2D vector of characters representing the game board
 *         coord - A string representing chess coordinates
 * Return: False if coordinates is already empty. Otherwise, remove the piece
 *         and return true
 */
bool apply_removal_move(vector<vector<char>> board, string coord){
	int row = coord_to_index_row(coord);
	int col = coord_to_index_col(coord);
	if(board[row][col] == EMPTY){
		return false
	}
	board[row][col] = EMPTY;
	return true;
}

/*
 * Determines if a certain move is valid
 * Params: board - A 2D vector of characters representing board
 *         start_row - Starting row value of piece to move
 *         start_col - Starting column value of piece to move
 *         end_row - Row value to move piece to
 *         end_col - Column value to move piece to
 *         player - String representing player color
 */
bool is_valid_move(vector<vecor<char>> board, int start_row, int start_col, int end_row, int end_col, string player){
	// Check if coordinates within bounds
	pair<int, int> start_coords = <start_row, start_col>;
	pair<int, int> end_coords = <end_row, end_col>;
	bool valid = false;

	for(const auto& p : v){
		if(p == start_coords){
			valid = true;
			break;
		}
	}

	for(const auto& p : v){
		if(p == end_coords){
			valid = true;
			break;
		}
	}

	if(!valid){
		return false;
	}

	// Check if start has a piece and end is empty
	char piece = board[start_row][start_col];

	if(piece != player[0]){
		return false;
	}
	if(piece == EMPTY){
		return false;
	}
	if(board[end_row][end_col] != EMPTY){
		return false;
	}

	// Must move in a straight line (horizontal or vertical)
	int row_diff = end_row - start_row;
	int col_diff = end_col - start_col;

	if(row_diff != 0 && col_diff != 0){
		return false; // diagonal move not allowed
	}
	if(row_diff == 0 && col_diff == 0){
		return false; // no movement
	}

	int distance;
	int direction;
	// Determine direction and distance
	if(row_diff != 0){
		// Vertical move
		distance = abs(row_diff);
		direction = (row_diff > 0) ? 1 : -1;
		// Check all positions between start and end
		int check_row;
		for(int i = 1; i < distance; ++i){
			check_row = start_row + (i * direction);
			if((i % 2) == 1){ // odd positions should have opponent pieces
				if(board[check_row][start_col] == EMPTY || board[check_row][start_col] == piece){
					return false;
				}
			}else{ // even positions should be empty
				if(board[check_row][start_col] != EMPTY){
					return false;
				}
			}	
		}
	}else{
		// Horizontal move
		distance = abs(col_diff);
		direction = (col_diff > 0) ? 1 : -1;
		// Check all positions between start and end
		int check_col;
		for(int i = 1; i < distance; ++i){
			check_col = start_col + (i * direction);
			if((i % 2) == 1){ // odd positions should have opponent pieces
				if(board[start_row][check_col] == EMPTY || board[start_row][check_col] == piece){
					return false;
				}
			}else{ // even positions should be empty
				if(board[start_row][check_col] != EMPTY){
					return false;
				}
			}	
		}	
	}
	// Distance must be even (jump is 2, 4, 6, etc.)
	if((distance % 2) != 0){
		return false;
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
	// Second move: exactly one empty square
	
	int count = count_empty(board);

	if(count == 1){
		string empty_coord = NONE_STR;

		for(int row = 0; row < SIZE; ++row){
			for(int col = 0; col < SIZE; ++col){
				if(board[row][col] == EMPTY){
					empty_coord = index_to_coord(row, col);
				}
			}
		}
		// Allowed responses based on which center stone was removed first
		string candidates[2];
		int candid_count = 0;

		if(empty_coord == "D5" || empty_coord == "E4"){
			candidates[0] = "E5";	
			candidates[1] = "D4";	
			candid_count = 2;
		} else if(empty_coord == "E5" || empty_coord == "D4"){
			candidates[0] = "D5";	
			candidates[1] = "E4";	
			candid_count = 2;
		}
		if(candid_count != 0){
			for(int i = 0; i < candid_count; ++i){
				int r = coord_to_index_row(candidates[i]);
				int c = coord_to_index_col(candidates[i]);
				if(board[r][c] == player[0]){
					return candidates[i];
				}
				
			}
		}
	}
	
	return NONE_STR;
}

/*
 * Moves a board piece and removes and captured pieces
 * Params: board - A 2D vector of characters representing the board
 *                 and must be passed by reference to modify
 *         move - A string containing the start and end positions of a piece in
 *                motion
 *         player - String representing the player color
 * Return: Returns a string representing the new coordinates of the moved piece
 */
string move_piece(vector<vector<char>& board, string move, string player){
	string start = parse_move_start(move);
	string end = parse_move_end(move);
	
	// Opening removal move support
	if(end == NONE_STR){
		if(apply_removal_move(board, start)){
			return start
		}
		return NONE_STR;	
	}	
	int start_row = coord_to_index_row(start);
	int start_col = coord_to_index_col(start);
	int end_row = coord_to_index_row(end);
	int end_col = coord_to_index_col(end);

	// Validate the first move
	if(!is_valid_move(board, start_row, start_col, end_row, end_col, player)){
		cout << "Invalid move" << endl;
		return NONE_STR
	}
	char piece = board[start_row][start_col];

	// Move the piece
	board[end_row][end_col] = piece;
	board[start_row][start_col] = 'O';

	// Remove jumped pieces
	int row_diff = end_row - start_row;
	int col_diff = end_col - start_col;
	int direction;
	int distance

	if(row_diff != 0){
		// Vertical jumps
		direction = (row_diff > 0) ? 1 : -1;
		distance = abs(row_diff);
		for(int i = 1; i < distance; i += 2){
			board[start_row + (i * direction)][start_col] = 'O';
		}
	} else {
		// Horizontal distance
		direction = (col_diff > 0) ? 1 : -1;
		distance = abs(col_diff);
		for(int i = 1; i < distance; i += 2){
			board[start_row][start_col + (i * direction)] = 'O';
		}
	}
	
	return index_to_coord(end_row, end_col);
}

/*
 * Generate a matrix representing mobility of a pieces on the board
 * Params: board - A 2D vector of characters representing board pieces
 *         player - String representing the color of player pieces
 * Return: A 2D vector of integers representing available hops to pieces
 */
vector<vector<int>> evaluate_tile_mobility_signed(vector<vector<char>> board, string player){
	/*
	 * Returns an 8x8 matrix:
	 * - Your pieces: positive move count
	 * - Opponent pieces: negative move count
	 * - Empty: 0
	 */
	vector<vector<int>> mobility_matrix(SIZE, vector<int>(SIZE, 0));
	char opponent = (player[0] == BLACK) ? WHITE : BLACK;

	vector<pair<int, int>> directions = {
		{-2, 0}, {-4, 0}, {-6, 0},
		{2, 0}, {4, 0}, {6, 0},
		{0, -2}, {0, -4}, {0, -6},
		{0, 2}, {0, 4}, {0, 6}
	};

	char piece;
	int move_count;
	int end_row;
	int end_col;

	for(int row = 0; row < SIZE; ++row){
		for(int col = 0; col < SIZE; ++col){
			piece = board[row][col];
			if(piece == EMPTY){
				mobility_matrix[row][col] = 0;
			} else if(piece == player || piece == opponent){
				move_count = 0;	
				for(const auto& [row_offset, col_offset] : directions){
					end_row = row + row_offset;
					end_col = col + col_offset;
					if(is_valid_move(board, row, col, end_row, end_col, piece)){
						move_count += 1;
					}
				}
				if(piece == player[0]){
					mobility_matrix[row][col] = move_count;
				} else {
					mobility_matrix[row][col] = (-1 * move_count);
				}
			}	
		}
	}
	return mobility_matrix;
}

/*
 * Gather a collection of structs holding all possible on the board
 * Params: board - A 2D vector of characters representing board pieces
 *         player - String representing the color of player pieces
 * Return: A vector of Move structs representing data on all possible moves
 */
vector<Moves> get_all_move_evaluations(vector<vector<char>> board, string player){
	/*
	 * For each possible move for the player, generate a resulting board,
	 * call evaluate_tile_mobility_signed, and store:
	 *   - 'move': move string
	 *   - 'start': (row, col)
	 *   - 'end': (row, col)
	 *   'eval_sum': sum of evaluation matrix after move
	 * Returns a list of dicts, one per possible move.
	 */
	
	vector<Moves> moves;
	vector<pair<int, int>> directions = {
		{-2, 0}, {-4, 0}, {-6, 0},
		{2, 0}, {4, 0}, {6, 0},
		{0, -2}, {0, -4}, {0, -6},
		{0, 2}, {0, 4}, {0, 6}
	};
	char opponent = (player[0] == BLACK) ? WHITE : BLACK;

	string start_coord = index_to_coord(row, col);
	int row_offset;
	int col_offset;
	int end_row;
	int end_col;
	int throwaway;
	int eval_sum;
	string end_coord;
	string move_str;
	string old_player;
	vector<vector<char>> board_copy;
	double eval_sum;
	string opp_start;
	int opp_end_row;
	int opp_end_col;
	string opp_end;
	string opp_move_str;

	for(int row = 0; row < SIZE; ++row){
		for(int col = 0; col < SIZE; ++col){
			if(board[row][col] == player[0]){
				start_coord = index_to_coord(row, col);
				for(const auto& direction : directions) {
					row_offset = direction.first;
					col_offset = direction.second;
					end_row = row + row_offset;
					end_col = col + col_offset;
					old_player = PLAYER;
					PLAYER = player;
					if(is_valid_move(board, row, col, end_row, end_col, player)){
						end_coord = index_to_coord(end_row, end_col);
						move_str = format_move(start_coord, end_coord);
						board_copy = board;
						throwaway = move_piece(board_copy, move_str, player);
						// Evaluate the resulting board
						eval_sum = evaluate_board_weighted(board_copy, player);
						// Now, generate all possible opponent replies from current board state
						vector<Replies> replies;
						for(int opp_row = 0; opp_row < SIZE; ++opp_row){
							for(int opp_col = 0; opp_col < SIZE; ++opp_col){
								if(board_copy[opp_row][opp_col] == opponent){
									opp_start = index_to_coord(opp_row, opp_col);
									for(const auto& [opp_row_offset, opp_col_offset] : directions){
										opp_end_row = opp_row + opp_row_offset;
										opp_end_col = opp_col + opp_col_offset;
										if(is_valid_move(board_copy, opp_row, opp_col, opp_end_row, opp_end_col, opponent)){
											opp_end = index_to_coord(opp_end_row, opp_end_col);
											opp_move_str = format_move(opp_start, opp_end);
											replies.push_back({opp_move_str, <opp_row, opp_col>, <opp_end_row, opp_end_col>});
										}
									}
								}
							}
						}
						moves.push_back({move_str, <row, col>, <end_row, end_col>, eval_sum, replies});
					}
				}
			}
		}
	}
	return moves;
	
}

/*
 *
 */
string find_best_move(vector<vector<char>> board, string player){
	vector<Moves> moves = get_all_move_evaluations(board, player);
	if(moves.empty()){
		return NONE_STR;
	}
	sort(moves.begin(), moves.end(), [](const Move &a, const Move &b){
		return a.eval_sum > b.eval_sum;
	});
	// Note: setup for timing moved
	string best_move = NONE_STR;
	double best_val = -numeric_limits<<double>::infinity();
	// Current position
}


/*
 * Gets the number of player pieces in the center minus number of opponent pieces
 * Params: board - A 2D vector of characters representing board pieces
 *         player - String representing the color of player pieces
 * Return: Integer representing diff of player and opponent pieces in the center
 */
int evaluate_center_control(vector<vector<char>> board, string player){
	vector<pair<int, int>> center_coords = {
		{3, 3}, {3, 4}, {4, 3}, {4, 4}
	}; // D4, D5, E4, E5
	int player_count = 0;
	char opponent = (player[0] == BLACK) ? WHITE : BLACK;
	int opponent_count = 0;
	for(const auto& [row, col] : center_coords){
		if(board[row][col] == player[0]){
			player_count += 1;
		} else if(board[row][col] == opponent){
			opponent_count += 1;
		}
	}
	return (player_count - opponent_count);
}

/*
 * Provides a weight for the board based off of evaluation functions
 * Params: board - A 2D vector of characters representing board pieces
 *         player - String representing the color of player pieces
 *         w_mob - Tailored weight value for mobility eval
 *         w_safe - Tailored weight value for piece safety
 *         w_center - Tailored weight value for center control
 * Return Double representing evaluation score
 */
double evaluate_board_weighted(vector<vector<char>> board, string player, double w_mob = 0.4, double w_safe = 0.4, double w_center = 0.2){
	char opponent = (player[0] == BLACK) ? WHITE : BLACK;
	vector<pair<int, int>> directions = {
		{-2, 0}, {-4, 0}, {-6, 0},
		{2, 0}, {4, 0}, {6, 0},
		{0, -2}, {0, -4}, {0, -6},
		{0, 2}, {0, 4}, {0, 6}
	};
	int mobility = 0;
	char piece;

	for(int row = 0; row < SIZE; ++row){
		for(int col = 0; col < SIZE; ++col){
			piece = board[row][col];
			if(piece == EMPTY){
				continue;
			}
			for(const auto& [dr, dc] : directions){
				if(is_valid_move(board, row, col, (row + dr), (col + dc), piece)){
					mobility += (piece == player[0]) ? 1 : -1;
				}
			}
		}
	}
	
	vector<vector<int>> mobility_matrix = evaluate_tile_mobility_signed(board, player);
	int safety_score;
	for(const auto& r : safety_matrix){
		for(int v : r){
			safety_score += v;
		}
	}
	center_score = evaluate_center_control(board, player);
	return (w_mob * mobility + w_safe * safety_score + w_center * center_score);
}

/*
 * Calls functions to pick a move depending if board is empty or not
 * Params: board - A 2D vector of characters representing board pieces
 *         player - String representing the color of player pieces
 * Return: String representing coordinate of piece to move
 */
string choose_move(vector<vector<char>> board, string player){
	string opening_move = find_opening_move(board, player);
	// Not returning one of the opening moves returns a mangled string
	if(opening_move != NONE_STR){
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
	*/
	// Testing opening move
	string o = find_opening_move(board, player);
	cout << "Opening move: " << o << endl;
	//cout << "Type of move: " << typeid(o).name() << endl;
	/*
	string my_move = choose_move(board, player);
	cout << "Move: " << my_move << endl;
	
	//Testing count_empty
	int count = count_empty(board);
	cout << "Count: " << count << endl;
	
	// Testing coord conversion
	string coord;
	for(int row = 0; row < SIZE; ++row){
		for(int col = 0; col < SIZE; ++col){
			coord = index_to_coord(row, col);
			cout << coord << " ";
		}
		cout << endl;
	}
	*/
	return 0;	
}
