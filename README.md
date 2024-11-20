## Dots and Boxes: Hybrid AI Project

### **Overview**
This project implements a hybrid AI to play the strategic two-player game *Dots and Boxes*. The AI combines **Monte Carlo Tree Search (MCTS)** and **Alpha-Beta Pruning** to adapt to different stages of the game:
- **Early/Mid-game**: MCTS is used for exploratory and probabilistic decision-making.
- **Endgame**: Alpha-Beta Pruning ensures precise and optimal moves.

The AI competes against human players via a responsive graphical interface built using Python's Tkinter library.

---

### **Features**
1. **Hybrid AI Approach**:
   - MCTS for exploration during early/mid-game.
   - Alpha-Beta Pruning for precise decision-making in the endgame.

2. **Dynamic Strategy Transition**:
   - Automatically switches between MCTS and Alpha-Beta Pruning when 60% of the boxes are completed.

3. **Interactive Gameplay**:
   - Real-time human-AI interaction with a Tkinter-based graphical interface.
   - Visual representation of moves, scores, and completed boxes.

4. **Efficient Algorithms**:
   - MCTS balances exploration and exploitation with randomized simulations.
   - Alpha-Beta Pruning optimizes computation by pruning irrelevant game tree branches.

5. **Game State Management**:
   - Tracks moves, scores, and player turns.
   - Automatically detects game completion and declares the winner.

---

### **Technologies Used**
- **Python**: Core language for game logic and AI algorithms.
- **Tkinter**: Used for building the graphical user interface.
- **MCTS**: For decision-making in early and mid-game.
- **Alpha-Beta Pruning**: For precise evaluations in the endgame.

---

### **Setup and Usage**
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/<username>/dots-and-boxes-ai.git
   cd dots-and-boxes-ai
   ```

2. **Install Dependencies**:
   Ensure you have Python installed. No external dependencies are required beyond the standard library.

3. **Run the Game**:
   ```bash
   python ai_project_final.py
   ```

4. **Play Against the AI**:
   - The game starts with a 4x4 grid of dots.
   - Take turns drawing lines to complete boxes.
   - The player with the most completed boxes wins.

---

### **How It Works**
1. **Early/Mid-game**:
   - MCTS evaluates potential moves by running randomized simulations to estimate outcomes.
   - Balances trying new strategies (exploration) with refining effective ones (exploitation).

2. **Endgame**:
   - Alpha-Beta Pruning efficiently evaluates the remaining possibilities, pruning irrelevant branches.

3. **Dynamic Transition**:
   - The AI transitions from MCTS to Alpha-Beta Pruning once 60% of boxes are completed.

4. **Graphical Interface**:
   - Intuitive interface for human-AI interaction.
   - Displays moves, scores, and game outcomes dynamically.

---

### **Future Enhancements**
- **Reinforcement Learning**: Train the AI to improve strategies through self-play.
- **Dynamic Strategy Adjustment**: Improve transitions based on game state and opponent behavior.
- **Parallelization**: Speed up simulations and pruning with parallel computing.
- **Opponent Modeling**: Predict and counter human strategies effectively.

---

### **Contributors**
- Chirayu Agrawal  
- Aadit Jaisani  
- Ansh Srivastava  
- Diva Pandey  
- Kunal Passan  
- Jayant Kumar  

---

### **License**
This project is licensed under the MIT License. See the `LICENSE` file for more details.