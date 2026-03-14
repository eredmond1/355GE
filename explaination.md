# Konane Game Functions Explanation

This document provides a quick reference for all functions in the Konane game implementation.

---

## Constants

- **BLACK, WHITE, EMPTY**: Represent piece types ('B', 'W', 'O')
- **SIZE**: Board size (8x8)
- **VALID_POSITIONS**: Set of all valid board coordinates (0-7, 0-7)
- **PLAYER**: Current player color (needs to be updated based on turn)

---

## Board Management

### `load_board(filename)`
Loads a board state from a text file.
- Reads the file line by line
- Converts each line into a list of characters (B, W, or O)
- Automatically removes center piece if board is completely full
- **Returns**: 2D list representing the board

### `remove_center_if_full(board)`
Checks if the board is completely full and removes the center piece if it is.
- Used during board initialization to start the game
- Center position is calculated as (SIZE//2, SIZE//2)
- **Returns**: Modified board

### `print_board(board)`
Displays the board with coordinates for easy reference.
```
   A B C D E F G H
8  B W O O O W B W
7  W O O O B O O B
...
```
- Column letters at top
- Row numbers on left side

---

## Coordinate Conversion

### `coord_to_index(coord)`
Converts chess notation to matrix indices.
- **Input**: "A8", "C6", etc.
- **Output**: (row, col) tuple with 0-based indices
- Example: "A8" → (0, 0), "H1" → (7, 7)

### `index_to_coord(row, col)`
Converts matrix indices back to chess notation.
- **Input**: row and column indices (0-7)
- **Output**: String like "A8" or "C6"
- Example: (0, 0) → "A8", (7, 7) → "H1"

---

## Move String Formatting

### `format_move(start, end)`
Creates a formatted move string from two coordinates.
- **Input**: Two coordinate strings (e.g., "A8", "C8")
- **Output**: Formatted string "A8 -> C8"

### `parse_move(move_string)`
Splits a formatted move string back into start and end coordinates.
- **Input**: Formatted string "A8 -> C8"
- **Output**: Tuple ("A8", "C8")

---

## Move Validation

### `is_valid_move(board, start_row, start_col, end_row, end_col)`
Validates if a move follows Konane rules. Takes indices (not coordinate strings).

**Checks performed:**
1. **Bounds**: Both positions are within board (0-7)
2. **Piece ownership**: Start position has current player's piece
3. **Empty destination**: End position is empty
4. **Direction**: Move is horizontal OR vertical (no diagonals)
5. **Path validation**: 
   - Odd positions (1, 3, 5...) must have opponent pieces
   - Even positions (2, 4, 6...) must be empty
6. **Distance**: Must be even (2, 4, 6 spaces)

**Returns**: True if valid, False otherwise

---

## Move Execution

### `move_piece(board, move)`
Executes a move if valid.

**Process:**
1. Parses move string to get start/end coordinates
2. Converts to indices
3. Validates the move using `is_valid_move()`
4. If invalid → prints "Invalid move" and returns None
5. If valid:
   - Moves piece to destination
   - Clears start position
   - Removes all jumped opponent pieces at odd positions along path
6. **Returns**: Destination coordinate or None if invalid

**Path clearing logic:**
- For vertical moves: removes pieces at intervals of 2 along column
- For horizontal moves: removes pieces at intervals of 2 along row

---

## AI / Move Finding

### `find_valid_move(board)`
Finds the first available valid move for the current player.

**Strategy (simple, not optimal):**
- Iterates through all board positions
- For each player piece found:
  - Tries moves in 4 directions (up, down, left, right)
  - Tries distances 2, 4, 6
  - Returns first valid move found

**Returns**: Formatted move string (e.g., "A8 -> C8") or None if no moves available

⚠️ **Note**: This is a placeholder. Final version will use Alpha-Beta Pruning with Minimax.

---

## How Moves Work

### Example: Moving from A8 to E8 (distance = 4)

```
Before:  B W B W O O O O
         ^ start   ^ end
         
Check:   Position B8 (i=1): Must have opponent (W) ✓
         Position C8 (i=2): Must be empty (O) ✓
         Position D8 (i=3): Must have opponent (W) ✓
         
After:   O O O O B O O O
         ^ cleared  ^ piece moves here
```

The `row_diff` and `col_diff` determine:
- **Which axis** to move along (row_diff=0 means horizontal)
- **Direction** (positive = right/down, negative = left/up)
- **Distance** to validate and clear

---

## Key Logic Points

### Distance Calculation
```python
distance = abs(row_diff)  # or abs(col_diff)
```
This is the number of squares between start and end.

### Direction Determination
```python
direction = 1 if diff > 0 else -1
```
- `+1` means moving right (columns) or down (rows)
- `-1` means moving left (columns) or up (rows)

### Path Validation Loop
```python
for i in range(1, distance):
    if i % 2 == 1:  # odd = opponent pieces
    else:           # even = empty squares
```
Ensures the alternating pattern required by Konane rules.

---

## Testing Functions

### `find_move_test()`
Tests the move finding and execution:
1. Loads early board
2. Prints initial state
3. Finds a valid move
4. Executes the move
5. Prints final state

### `state1()` / `state2()`
Simple board display tests for different board states.
