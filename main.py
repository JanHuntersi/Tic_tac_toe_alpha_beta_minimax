import tkinter as tk
from tkinter import *
from itertools import cycle
from tkinter import font
from typing import NamedTuple
import copy
from tkinter import ttk

from testing import get_position_ai  #AI LOGIC

class Player(NamedTuple):
    icon:str
    color:str
    val: int
    score:int
    
PLAYERS = (
    Player(icon="X", color="green", val=1, score=0),#PLAYER
    Player(icon="O", color="blue", val=2, score=0), #AI
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
        self._ai_difficulty=2


    def getAiMove(self): #returns AI's chosen position to move circle to

        newState=copy.deepcopy(self._states)

        print("sending to ai: ")
        for row in self._states:
            for column in row:
                print(column, end=" ")
            print()

        x,y = get_position_ai(newState,self._ai_difficulty)
        
        print("AI wants to play " + str(x) + str(y))
        print("value at position is: " + str(self._states[x][y]) )    

        
        self._states[x][y]=2 #set value in states


        print("After ai changed: ")
        for row in self._states:
            for column in row:
                print(column, end=" ")
            print()
        return x,y #return position
    

    def togglePlayer(self):
        self._current_player = next(self._players)
        print("player " + self._current_player.icon + "   turn")

    #check if game over and if it is se values
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

    #reset values and start game
    def startNextGame(self,widget): 
        #Reset values and start again    
        self._states=[[0, 0, 0], [0, 0, 0], [0, 0, 0]]

        self._isOver = False #Start again

        self.togglePlayer() #Next player starts
       

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
    def __init__(self,game_logic):
        super().__init__()
        self.title("Tic tac toe minimax alfa/beta")
        self._game_logic=game_logic
        self._cells={}
        self._label_score={} #label with score
        self._new_game_btn={} #btn for starting new game
        self._dropdown_var={}
        self._dropdown()
        self._create_board()
        self._score()
        self._next_game()
        self._new_game_btn.pack_forget()

    def get_selected_value(self):
        selected_value = self._dropdown_var.get()
        self._game_logic._ai_difficulty = int(selected_value)  
        print("Set difficulty to " + selected_value)


    def _dropdown(self):
        frame = tk.Frame(master=self)
        frame.pack()

            # create the dropdown menu options
        options = [1,2,3,4,5,6,7,8]

        # create the dropdown menu
        self._dropdown_var = tk.StringVar()
        dropdown = ttk.Combobox(frame, textvariable=self._dropdown_var, values=options)
        dropdown.current(2)
        dropdown.pack()    
        # create the button to get the selected value
        button = tk.Button(frame, text="SET DIFFICULTY", command=lambda:self.get_selected_value())
        button.pack()


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


    def ai_play_game(self):
        #AI STARTS GAME
        if self._game_logic._current_player.val == 2: 
            x,y = self._game_logic.getAiMove()
            
            btn_to_update={}
            #get btn from list
            for btn in self._cells.keys():
                row,col = self._cells[btn]
                if row == x and col == y:
                    btn_to_update = btn
                    break
            if  btn_to_update=={}:
                print("error finding button to update")
            else:
                self._update_btn(btn_to_update) #update btn look

            if self._game_logic.checkIfOver() == True:
                print("Game!")
                self._new_game_btn.pack()
            else:
                self._game_logic.togglePlayer()
            #update label
            self._label_score.config(text="User:%d   Tied:%d   Pc:%d" % (self._game_logic._player_score, self._game_logic._draw_score, self._game_logic._ai_score),)
    


    def reset_values(self):
        #Reset values
        for btn in self._cells.keys():
            btn.config(text="") 
            
        self._game_logic.startNextGame(self._new_game_btn) #Start new game

        #AI STARTS GAME
        if self._game_logic._current_player.val == 2:   #AI STARTS GAME
                #AI SELECTS MOVE    
            self.ai_play_game()
        

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
                print("game over!")
                self._new_game_btn.pack()

            #AI STARTS GAME
            if self._game_logic._current_player.val == 2 and self._game_logic._isOver==False:  
                #AI SELECTS MOVE    
                self.ai_play_game()


def main():
    game=GameLogic() # Class for game logic
    game_board=TTTBoard(game)  #instantiating  GUI class
    game_board.mainloop()   #the tkinter event loop -> listens to events, clicks...

if __name__ == "__main__":
    main()