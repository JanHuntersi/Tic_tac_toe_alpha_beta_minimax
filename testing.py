

from typing import NamedTuple
import copy


def hevristika(state):   
 # H = (col + row + diag) for MAX  - (col + row + diag) for MIN
    # Max is AI Min is user
    # MAX val=2
    # MIN val=1  

    maxRes=0
    minRes=0

    for i in range(3):
        #Checks rows for Max
        if state[i][0] in[2,0] and state[i][1] in[2,0] and state[i][2] in[2,0]:
            minRes+=1    
        #Checks rows for Min
        if state[i][0] in[1,0] and state[i][1] in[1,0] and state[i][2] in[1,0]:
            maxRes+=1    

        #Checks columns for Max
        if state[0][i] in[2,0] and state[1][i] in[2,0] and state[2][i] in[2,0]:
            minRes+=1    
        #Checks columns for Min
        if state[0][i] in[1,0] and state[1][i] in[1,0] and state[2][i] in[1,0]:
            maxRes+=1   

        #CHECK IF MAX WON----------
            # ROW    
        if state[i][0] == 2 and state[i][1] == 2 and state[i][2] ==2:
            return -100
            #COLUMN
        if state[0][i] == 2 and state[1][i] == 2 and state[2][i] == 2:
            return -100
        
        #CHECK IF MIN WON----------
            # ROW    
        if state[i][0] == 1 and state[i][1] == 1 and state[i][2] ==1:
            return 100
            #COLUMN
        if state[0][i] == 1 and state[1][i] == 1 and state[2][i] == 1:
            return 100

    #CHECK if MAX WON DIAGONAL
    if state[0][0] == 2 and state[1][1] == 2 and state[2][2] == 2:
        return -100
    if state[0][2]== 2  and state[1][1]== 2  and state[2][0]== 2:
        return -100

    #CHECK if MIN WON DIAGONAL
    if state[0][0] == 1 and state[1][1] == 1 and state[2][2] == 1:
        return 100
    if state[0][2]== 1  and state[1][1]== 1  and state[2][0]== 1:
        return 100


    #check diagonals for Max
    if state[0][0]in[2,0] and state[1][1]in[2,0] and state[2][2] in[2,0]:
        minRes+=1 
    if state[0][2]in[2,0] and state[1][1]in[2,0] and state[2][0] in[2,0]:
        minRes+=1 

    #check diagonals for Min
    if state[0][0] in [1,0] and state[1][1] in [1,0] and state[2][2] in [1,0]:
        maxRes+=1 
    if state[0][2] in [1,0] and state[1][1] in [1,0] and state[2][0] in [1,0]:
        maxRes+=1 

    return  maxRes - minRes



def isStateFinished(state):
    for x in range(3):
        for y in range(3):
            if state[x][y] == 0:
                return False

            if state[x][0] == 2 and state[x][1] == 2 and state[x][2] ==2:
                return True
            if state[x][0] == 1 and state[x][1] == 1 and state[x][2] ==1:
                return True
    
            if state[0][y] == 2 and state[1][y] == 2 and state[2][y] == 2:
                return True
            if state[0][y] == 1 and state[1][y] == 1 and state[2][y] == 1:
                return True

    #CHECK if MAX WON DIAGONAL
    if state[0][0] == 2 and state[1][1] == 2 and state[2][2] == 2:
        return True
    if state[0][2]== 2  and state[1][1]== 2  and state[2][0]== 2:
        return True

    #CHECK if MIN WON DIAGONAL
    if state[0][0] == 1 and state[1][1] == 1 and state[2][2] == 1:
        return True
    if state[0][2]== 1  and state[1][1]== 1  and state[2][0]== 1:
        return True            

    return True


def minmax(s,d,player,alpha,beta):

    newState=copy.deepcopy(s)
    
    if d == 0 or isStateFinished(newState)==True:   
        return hevristika(newState),10,10
   
   
    if player==True: # PLAYER MAX uporabnik
        ocena =-100
    else:
        ocena =100   

    x = 10
    y = 10


    for i in range(3):
        for j in range(3): #try all options

            if newState[i][j] == 0: 
                

                tmpState = copy.deepcopy(newState) #deep copy so original isnt changed 

                if player==True: #MAX
                    tmpState[i][j] = 1
                else:            #MIN   
                    tmpState[i][j] = 2
   
                outOcena,outX,outY = minmax(tmpState,d-1,not player,alpha,beta)

                if(player ==True and outOcena > ocena) :
                
                    ocena=outOcena
                    x=i
                    y=j

                    if ocena > alpha:
                        alpha = ocena

                elif  (player == False and outOcena < ocena):
                    ocena=outOcena
                    x=i
                    y=j    

                    if ocena < beta:
                        beta = ocena

                if alpha >= beta:
                    return ocena,x,y

    return ocena,x,y


def get_position_ai(state,d):    
    state_copy= copy.deepcopy(state)
    ocena,x,y = minmax(state_copy,d,False,-100,100)   
    return x,y


def main():
    state=[[0,0,0],
           [0,0,0],
           [0,0,0]]
    
    print(hevristika(state))


    print("Starting")
   
    state_copy= copy.deepcopy(state)

    ocena,x,y = minmax(state_copy,2,True,-100,100)
    print("Dobili smo " + str(ocena) + " " + str(x) + " " + str(y))
    #print(output)
   

if __name__ == "__main__":
    main()