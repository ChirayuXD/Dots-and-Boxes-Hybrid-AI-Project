import tkinter as tk
from tkinter import messagebox
import random
import math
import time
from copy import deepcopy

class MCTSNode:
    def __init__(self, state, parent=None, move=None):
        self.state = state
        self.parent = parent
        self.move = move
        self.children = []
        self.wins = 0
        self.visits = 0
        self.untried_moves = state.get_possible_moves()
    
    def select_child(self):
        exploration = 1.41
        return max(self.children, key=lambda c: c.wins/c.visits + 
                  exploration * math.sqrt(math.log(self.visits)/c.visits))
    
    def expand(self):
        move = self.untried_moves.pop()
        new_state = deepcopy(self.state)
        new_state.make_move(move)
        child = MCTSNode(new_state, self, move)
        self.children.append(child)
        return child
    
    def backpropagate(self, result):
        self.visits += 1
        self.wins += result
        if self.parent:
            self.parent.backpropagate(1 - result)

class GameState:
    def __init__(self, size=4):
        self.size = size
        self.lines = set()
        self.boxes = {}
        self.scores = {1: 0, 2: 0}
        self.current_player = 1
    
    def get_possible_moves(self):
        moves = []
        # Horizontal lines
        for row in range(self.size):
            for col in range(self.size - 1):
                line = frozenset([(row, col), (row, col + 1)])
                if line not in self.lines:
                    moves.append(line)
        
        # Vertical lines
        for row in range(self.size - 1):
            for col in range(self.size):
                line = frozenset([(row, col), (row + 1, col)])
                if line not in self.lines:
                    moves.append(line)
        
        return moves
    
    def make_move(self, line):
        self.lines.add(line)
        completed = self.check_box_completion(line)
        if not completed:
            self.current_player = 3 - self.current_player
        return completed
    
    def check_box_completion(self, line):
        dot1, dot2 = tuple(line)
        completed_boxes = 0
        
        # Check if line is horizontal
        if dot1[0] == dot2[0]:
            row = dot1[0]
            col = min(dot1[1], dot2[1])
            
            # Check box above
            if row > 0:
                box_lines = {
                    frozenset([(row-1, col), (row-1, col+1)]),
                    frozenset([(row-1, col), (row, col)]),
                    frozenset([(row-1, col+1), (row, col+1)]),
                    line
                }
                if all(l in self.lines for l in box_lines):
                    self.boxes[(row-1, col)] = self.current_player
                    self.scores[self.current_player] += 1
                    completed_boxes += 1
            
            # Check box below
            if row < self.size - 1:
                box_lines = {
                    frozenset([(row, col), (row, col+1)]),
                    frozenset([(row, col), (row+1, col)]),
                    frozenset([(row, col+1), (row+1, col+1)]),
                    frozenset([(row+1, col), (row+1, col+1)])
                }
                if all(l in self.lines for l in box_lines):
                    self.boxes[(row, col)] = self.current_player
                    self.scores[self.current_player] += 1
                    completed_boxes += 1
        
        # Check if line is vertical
        else:
            col = dot1[1]
            row = min(dot1[0], dot2[0])
            
            # Check box to the left
            if col > 0:
                box_lines = {
                    frozenset([(row, col-1), (row+1, col-1)]),
                    frozenset([(row, col-1), (row, col)]),
                    frozenset([(row+1, col-1), (row+1, col)]),
                    line
                }
                if all(l in self.lines for l in box_lines):
                    self.boxes[(row, col-1)] = self.current_player
                    self.scores[self.current_player] += 1
                    completed_boxes += 1
            
            # Check box to the right
            if col < self.size - 1:
                box_lines = {
                    frozenset([(row, col), (row+1, col)]),
                    frozenset([(row, col), (row, col+1)]),
                    frozenset([(row+1, col), (row+1, col+1)]),
                    frozenset([(row, col+1), (row+1, col+1)])
                }
                if all(l in self.lines for l in box_lines):
                    self.boxes[(row, col)] = self.current_player
                    self.scores[self.current_player] += 1
                    completed_boxes += 1
        
        return completed_boxes > 0
    
    def is_terminal(self):
        return len(self.boxes) == (self.size - 1) ** 2
    
    def get_winner(self):
        if not self.is_terminal():
            return None
        if self.scores[1] > self.scores[2]:
            return 1
        elif self.scores[2] > self.scores[1]:
            return 2
        return 0  # Draw
    
    def evaluate(self):
        """Evaluation function for Alpha-Beta pruning"""
        return self.scores[2] - self.scores[1]  # Positive is good for AI (player 2)

class AlphaBetaSearch:
    def __init__(self, state):
        self.state = state
    
    def get_move(self):
        _, best_move = self.alpha_beta(self.state, 8, float('-inf'), float('inf'), True)
        return best_move
    
    def alpha_beta(self, state, depth, alpha, beta, maximizing_player):
        if depth == 0 or state.is_terminal():
            return state.evaluate(), None
        
        possible_moves = state.get_possible_moves()
        if not possible_moves:
            return state.evaluate(), None
        
        best_move = possible_moves[0]
        if maximizing_player:
            max_eval = float('-inf')
            for move in possible_moves:
                new_state = deepcopy(state)
                completed = new_state.make_move(move)
                # If box completed, keep same player's turn
                next_maximizing = maximizing_player if completed else not maximizing_player
                eval_score, _ = self.alpha_beta(new_state, depth - 1, alpha, beta, next_maximizing)
                
                if eval_score > max_eval:
                    max_eval = eval_score
                    best_move = move
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break
            return max_eval, best_move
        else:
            min_eval = float('inf')
            for move in possible_moves:
                new_state = deepcopy(state)
                completed = new_state.make_move(move)
                # If box completed, keep same player's turn
                next_maximizing = maximizing_player if completed else not maximizing_player
                eval_score, _ = self.alpha_beta(new_state, depth - 1, alpha, beta, next_maximizing)
                
                if eval_score < min_eval:
                    min_eval = eval_score
                    best_move = move
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break
            return min_eval, best_move

class MCTS:
    def __init__(self, state, time_limit=1):
        self.root = MCTSNode(state)
        self.time_limit = time_limit
    
    def get_move(self):
        end_time = time.time() + self.time_limit
        
        while time.time() < end_time:
            node = self.select_node()
            if not node.state.is_terminal():
                node = node.expand()
                result = self.simulate(node.state)
                node.backpropagate(result)
        
        return max(self.root.children, key=lambda c: c.visits).move
    
    def select_node(self):
        node = self.root
        while node.untried_moves == [] and node.children != []:
            node = node.select_child()
        return node
    
    def simulate(self, state):
        state = deepcopy(state)
        while not state.is_terminal():
            moves = state.get_possible_moves()
            move = random.choice(moves)
            state.make_move(move)
        winner = state.get_winner()
        return 1 if winner == state.current_player else 0 if winner == 0 else -1

class DotsAndBoxes:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Dots and Boxes vs Hybrid AI")
        
        self.grid_size = 4
        self.dot_size = 8
        self.spacing = 60
        self.line_click_distance = 15
        
        self.game_state = GameState(self.grid_size)
        self.ai_player = 2
        
        # Define when to switch to Alpha-Beta (e.g., when 75% of possible boxes are completed)
        self.endgame_threshold = ((self.grid_size - 1) ** 2) * 0.75
        
        self.player_colors = {
            1: '#3498db',  # Blue (Human)
            2: '#e74c3c'   # Red (AI)
        }
        
        canvas_size = (self.grid_size * self.spacing) + 100
        self.canvas = tk.Canvas(
            self.window, 
            width=canvas_size, 
            height=canvas_size,
            bg='white'
        )
        self.canvas.pack(pady=20)
        
        self.score_frame = tk.Frame(self.window)
        self.score_frame.pack(pady=10)
        
        self.player1_label = tk.Label(
            self.score_frame,
            text="Human: 0",
            fg=self.player_colors[1],
            font=('Arial', 12, 'bold')
        )
        self.player1_label.pack(side=tk.LEFT, padx=20)
        
        self.player2_label = tk.Label(
            self.score_frame,
            text="AI: 0",
            fg=self.player_colors[2],
            font=('Arial', 12, 'bold')
        )
        self.player2_label.pack(side=tk.LEFT, padx=20)
        
        self.dots = self.initialize_board()
        self.canvas.bind('<Button-1>', self.handle_click)
        self.window.mainloop()
    
    def is_endgame(self):
        """Check if we should switch to Alpha-Beta search"""
        return len(self.game_state.boxes) >= self.endgame_threshold
    
    def make_ai_move(self):
        """Make AI move using either MCTS or Alpha-Beta based on game phase"""
        if self.is_endgame():
            # Use Alpha-Beta search in endgame
            alpha_beta = AlphaBetaSearch(deepcopy(self.game_state))
            move = alpha_beta.get_move()
        else:
            # Use MCTS in early/mid game
            mcts = MCTS(deepcopy(self.game_state), time_limit=1)
            move = mcts.get_move()
        
        # Make the move
        self.game_state.make_move(move)
        self.update_display()
        
        # Check for game over
        if self.game_state.is_terminal():
            self.game_over()
        elif self.game_state.current_player == self.ai_player:
            # AI gets another turn if it completed a box
            self.window.after(500, self.make_ai_move)
    
    # [Rest of the methods remain the same as in the original code]
    def initialize_board(self):
        dots = {}
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                x = col * self.spacing + 50
                y = row * self.spacing + 50
                dots[(row, col)] = (x, y)
                self.canvas.create_oval(
                    x - self.dot_size/2,
                    y - self.dot_size/2,
                    x + self.dot_size/2,
                    y + self.dot_size/2,
                    fill='black'
                )
        return dots
    
    def find_closest_line(self, click_x, click_y):
        min_distance = float('inf')
        closest_line = None
        
        # Check horizontal lines
        for row in range(self.grid_size):
            for col in range(self.grid_size - 1):
                x1 = self.dots[(row, col)][0]
                y1 = self.dots[(row, col)][1]
                x2 = self.dots[(row, col + 1)][0]
                y2 = self.dots[(row, col + 1)][1]
                
                if x1 <= click_x <= x2:
                    distance = abs(y1 - click_y)
                    if distance < min_distance and distance < self.line_click_distance:
                        min_distance = distance
                        closest_line = frozenset([(row, col), (row, col + 1)])
        
        # Check vertical lines
        for row in range(self.grid_size - 1):
            for col in range(self.grid_size):
                x1 = self.dots[(row, col)][0]
                y1 = self.dots[(row, col)][1]
                x2 = self.dots[(row + 1, col)][0]
                y2 = self.dots[(row + 1, col)][1]
                
                if y1 <= click_y <= y2:
                    distance = abs(x1 - click_x)
                    if distance < min_distance and distance < self.line_click_distance:
                        min_distance = distance
                        closest_line = frozenset([(row, col), (row + 1, col)])
        
        return closest_line
    
    def draw_line(self, line):
        dot1, dot2 = tuple(line)
        x1, y1 = self.dots[dot1]
        x2, y2 = self.dots[dot2]
        self.canvas.create_line(
            x1, y1, x2, y2,
            fill=self.player_colors[self.game_state.current_player],
            width=3
        )
    
    def complete_box(self, row, col, player):
        """Fill a completed box"""
        x1 = self.dots[(row, col)][0]
        y1 = self.dots[(row, col)][1]
        x2 = self.dots[(row + 1, col + 1)][0]
        y2 = self.dots[(row + 1, col + 1)][1]
        
        self.canvas.create_rectangle(
            x1, y1, x2, y2,
            fill=self.player_colors[player],
            stipple='gray50'
        )
    
    def update_display(self):
        """Update the game display"""
        self.player1_label.config(text=f"Human: {self.game_state.scores[1]}")
        self.player2_label.config(text=f"AI: {self.game_state.scores[2]}")
        
        # Draw all lines
        for line in self.game_state.lines:
            self.draw_line(line)
        
        # Fill all completed boxes
        for (row, col), player in self.game_state.boxes.items():
            self.complete_box(row, col, player)
    
    def handle_click(self, event):
        """Handle human player moves"""
        if self.game_state.current_player != self.ai_player:
            line = self.find_closest_line(event.x, event.y)
            if line and line not in self.game_state.lines:
                # Make human move
                self.game_state.make_move(line)
                self.update_display()
                
                # Check for game over
                if self.game_state.is_terminal():
                    self.game_over()
                elif self.game_state.current_player == self.ai_player:
                    # AI's turn
                    self.window.after(500, self.make_ai_move)
    
    def game_over(self):
        """Handle game over state"""
        winner = self.game_state.get_winner()
        message = "It's a tie!" if winner == 0 else \
                  "You win!" if winner == 1 else \
                  "AI wins!"
        
        # Show which strategy was used in the endgame
        messagebox.showinfo(
            "Game Over",
            f"{message}\nYour score: {self.game_state.scores[1]}\n"
            f"AI score: {self.game_state.scores[2]}\n"

        )
        self.window.quit()

if __name__ == "__main__":
    DotsAndBoxes()