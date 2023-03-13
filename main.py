import tkinter as tk
from tkinter import *
from itertools import cycle
from tkinter import font
from typing import NamedTuple

class Move(NamedTuple):
    row: int
    col: int


def hevristika(state):

    # H = (col + row + diag) for MAX  - (col + row + diag) for MIN
    # Max is AI Min is PC
    # MAX val=2
    # MIN val=1  

    maxRes=0
    minRes=0

    for i in range(3):
            #Checks rows for Max
            if state[i][0] in[2,0] and state[i][1] in[2,0] and state[i][2] in[2,0]:
                maxRes+=1    
            #Checks rows for Min
            if state[i][0] in[1,0] and state[i][1] in[1,0] and state[i][2] in[1,0]:
                minRes+=1    

            #Checks columns for Max
            if state[0][i] in[2,0] and state[1][i] in[2,0] and state[2][i] in[2,0]:
                maxRes+=1    
            #Checks columns for Min
            if state[0][i] in[1,0] and state[1][i] in[1,0] and state[2][i] in[1,0]:
                minRes+=1   

    #check diagonals for Max
    if state[0][0]in[2,0] and state[1][1]in[2,0] and state[2][2] in[2,0]:
        maxRes+=1 
    if state[0][2]in[2,0] and state[1][1]in[2,0] and state[2][0] in[2,0]:
        maxRes+=1 

    #check diagonals for Min
    if state[0][0] in [1,0] and state[1][1] in [1,0] and state[2][2] in [1,0]:
        minRes+=1 
    if state[0][2] in [1,0] and state[1][1] in [1,0] and state[2][0] in [1,0]:
        minRes+=1 

    return  maxRes - minRes

class AIPlayer():
    def __init__(self):
        self._difficulty=1
    
    def move(self,state):

        print("AI MOVE!")

        return 



class Player(NamedTuple):
    icon:str
    color:str
    val: int
    score:int
    
PLAYERS = (
    Player(icon="X", color="green", val=1, score=0),
    Player(icon="O", color="blue", val=2, score=0),
)    


class GameLogic:
    def __init__(self):
        self._players=cycle(PLAYERS)
        self._current_player = next(self._players)
        self._isOver = False
        self._states = [ [0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self._draw_score=0
        self._player_score=0
        self._ai_score=0
    
    def togglePlayer(self):
        self._current_player = next(self._players)

    def checkIfOver(self):
        user_won = False
        player = self._current_player.val

        # check all rows and columns
        for i in range(3):
            if self._states[i][0]==player and self._states[i][1]==player and self._states[i][2] ==player:
                user_won=True
            if self._states[0][i]==player and self._states[1][i]==player and self._states[2][i] ==player:
                user_won=True
        
        #check diagonals
        if self._states[0][0]==player and self._states[1][1]==player and self._states[2][2] ==player:
            user_won=True
        if self._states[0][2]==player and self._states[1][1]==player and self._states[2][0] ==player:
            user_won=True
 
        if user_won:
            print("USER WON :" + str(self._current_player.val))
            self._isOver = True
            if(self._current_player.val==1):
                print("user")
                self._player_score +=1
            else:            
                print("AI")    
                self._ai_score +=1
            return True
        
        isDraw=True #Check if all moves are set
        for i in range(3):
            for j in range(3):
                if self._states[i][j] == 0:
                    isDraw=False
                    break

        if isDraw:  
            print("ITS a DRAW")
            self._isOver = True
            self._draw_score+=1
            return True
        
        return False

    
    def startNextGame(self,widget): 
        #Reset values and start again    
        self._states = [ [0, 0, 0], [0, 0, 0], [0, 0, 0]]

        self._isOver = False #Start again

        self.togglePlayer() #Next player starts
        if self._current_player.val == 2:  #AI STARTS GAME
            print("HERE AI starts")
        #Hide Button
        widget.pack_forget()


    def moveLogic(self,row,col):
        #update state 
        self._states[row][col] = self._current_player.val #Set state!
        #check if over 
        if self.checkIfOver()==False:
            self.togglePlayer()            

    def isValid(self,row,col):
        return self._states[row][col] == 0

        
class TTTBoard(tk.Tk):
    def __init__(self,game_logic,ai):
        super().__init__()
        self.title("Tic tac toe minimax alfa/beta")
        self._game_logic=game_logic
        self._ai=ai
        self._cells={}
        self._label_score={} #label with score
        self._new_game_btn={} #btn for starting new game
        self._create_board()
        self._score()
        self._next_game()
        self._new_game_btn.pack_forget()

    def _score(self):
        frame = tk.Frame(master=self) #games main window will be the frames parent    
        frame.pack(fill=tk.X) #on resize frame fills width
        self._label_score = Label(
            master=frame,
            pady=15,
            padx=5,
            text="User:%d   Tied:%d   Pc:%d" % (self._game_logic._player_score, self._game_logic._draw_score, self._game_logic._ai_score),
            font=font.Font(size=28, weight="bold"),
        )
        self._label_score.pack()

    def _next_game(self):
        frame = tk.Frame(master=self) #games main window will be the frames parent    
        frame.pack()
        self._new_game_btn=Button(frame, fg="white", background="blue", width=10,height=2, text="Next Game", font= ('Helvetica bold', 15),command=lambda:self.reset_values() )  
        self._new_game_btn.pack(pady=10)            

    def _create_board(self):
        frame = tk.Frame(master=self)
        frame.pack()
        for row in range(3):
            self.rowconfigure(row, weight=1,minsize=50)
            self.columnconfigure(row, weight=1, minsize=75)
            for col in range(3):
                button = tk.Button(
                    master=frame,
                    text="",
                    font=font.Font(size=36, weight="bold"),
                    fg="white",
                    width=5,
                    height=2,
                    highlightbackground="darkblue",
                )
                self._cells[button] = (row, col)
                button.grid(row=row,column=col,padx=5,pady=5,sticky="nsew")
                button.bind("<ButtonPress-1>", self._play_click)
    
    def _update_btn(self,btn):
        btn.config(text=self._game_logic._current_player.icon)
        btn.config(fg=self._game_logic._current_player.color)

    def reset_values(self):
        #Reset values
        for btn in self._cells.keys():
            btn.config(text="") 
            
        self._game_logic.startNextGame(self._new_game_btn) #Start new game

    def _play_click(self, event):
        btn = event.widget
        row,col = self._cells[btn]
        print("WE clicked on ",row,col)

        if self._game_logic.isValid(row,col) and  self._game_logic._isOver == False:

            self._update_btn(btn) #update btn look
            self._game_logic.moveLogic(row,col)  #handle game logic of click
            
            #update label
            self._label_score.config(text="User:%d   Tied:%d   Pc:%d" % (self._game_logic._player_score, self._game_logic._draw_score, self._game_logic._ai_score),)

            #Next game button show
            if self._game_logic._isOver: #if GAME FINISHED SHOW NEXT GAME BUTTON
                self._new_game_btn.pack()
            elif self._game_logic_current_player.val == 2:  #AI STARTS GAME
                
                #AI SELECTS MOVE    
                self._ai.move() 


def main():
    game=GameLogic() # Class for game logic
    ai=AIPlayer() #Class for artificial intelligence
    game_board=TTTBoard(game,ai)  #instantiating  GUI class
    game_board.mainloop()   #the tkinter event loop -> listens to events, clicks...

if __name__ == "__main__":
    main()