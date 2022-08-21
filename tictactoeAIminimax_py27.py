import sys, os, math, datetime
import numpy as np
import Tkinter as Tk
import random as rd

BEGINNING = True;
GAMEMODE = 0;
TURNLIST = np.zeros(9);
POLIST = np.zeros((3, 3));
PXLIST = np.zeros((3, 3));
GAMEDONE = False;



def AIMove(buttons, label):
    index = minimaxIdx();
    markBox(buttons, index, label);
def simpleIdx():
    global TURNLIST;
    index = 0;
    zeroFound = False; 
    while zeroFound == False: 
        if TURNLIST[index] == 0:
            zeroFound = True;
        else:
            index += 1;
    return index;
#minimax##########################
def minimaxIdx():
    global GAMEMODE;
    global TURNLIST;
    optIdx = -1;
    if GAMEMODE == 1:
        bestScore = -1000;
        for i in range(9):
            if TURNLIST[i] == 0:
                setVal(i, 1, "X");
                score = minimax(False);
                if score > bestScore:
                    bestScore = np.copy(score);
                    optIdx = np.copy(i);
                print PXLIST - POLIST, "<-----";
                print "score = " + str(score);
                print "bestScore = " + str(bestScore);
                print "optIdx = " + str(optIdx);
                print "";
                setVal(i, 0, "X");
    elif GAMEMODE == -1:
        if np.sum(TURNLIST) == 0:
            return rd.randrange(9);
        bestScore = 1000;
        for i in range(9):
            if TURNLIST[i] == 0:
                setVal(i, 1, "O");
                score = minimax(True);
                if score < bestScore:
                    bestScore = np.copy(score);
                    optIdx = np.copy(i);
                print PXLIST - POLIST, "<-----";
                print "score = " + str(score);
                print "optIdx = " + str(optIdx);
                print "";
                setVal(i, 0, "O");
    print "###################################" + str(np.sum(TURNLIST));
    return optIdx;
def minimax(maximizing):
    global TURNLIST;
    global POLIST;
    global PXLIST;
    if checkWin(POLIST) == True:
        return -1*(len(TURNLIST) - np.sum(TURNLIST) + 1);
    elif checkWin(PXLIST) == True:
        return  1*(len(TURNLIST) - np.sum(TURNLIST) + 1);
    elif np.sum(TURNLIST) == 9:
        return 0;

    if maximizing == True:
        bestScore = -1000;
        for i in range(9):
            if TURNLIST[i] == 0:
                setVal(i, 1, "X");
                score = minimax(False);
                bestScore = max(bestScore, score);
                #print PXLIST - POLIST, maximizing, bestScore, "\n";
                setVal(i, 0, "X");
        return bestScore;
    elif maximizing == False:
        bestScore = 1000;
        for i in range(9):
            if TURNLIST[i] == 0:
                setVal(i, 1, "O");
                score = minimax(True);
                bestScore = min(bestScore, score);
                #print PXLIST - POLIST, maximizing, bestScore, "\n";
                setVal(i, 0, "O");
        return bestScore;
def setVal(idx, val, OXid):
    if val not in [0, 1]:
        print "ERROR: setVal(): invalid input";
        exit(0);
    global GAMEMODE;
    global TURNLIST;
    global POLIST; 
    global PXLIST; 
    TURNLIST[idx] = np.copy(val);
    if OXid == "O":
        POLIST[idx/3, idx%3] = np.copy(val);
    elif OXid == "X":
        PXLIST[idx/3, idx%3] = np.copy(val);
    else:
        print "ERROR: setVal(): invalid input";
        exit(0);
def checkWin(PLIST):
    if np.sum(PLIST) >= 3:
        for i in range(3):
            if np.sum(PLIST[i]) == 3:
                return True;
            if np.sum(PLIST[:, i]) == 3:
                return True;
        if (PLIST[0,0]+PLIST[1,1]+PLIST[2,2]) == 3:
            return True;
        if (PLIST[0,2]+PLIST[1,1]+PLIST[2,0]) == 3:
            return True;
    return False; 
##################################



def playerMove(buttons, idx, label):
    global BEGINNING;
    global GAMEMODE;
    global TURNLIST;
    global GAMEDONE;
    if BEGINNING == True:
        if idx == 3 or idx == 4 or idx == 5:
            BEGINNING = False;
            GAMEMODE = np.copy(idx - 4);
            setGame(buttons, label);
            if GAMEMODE == -1:
                AIMove(buttons, label);
    else:
        if TURNLIST[idx] == 0 and GAMEDONE == False:
            markBox(buttons, idx, label);
            if GAMEMODE != 0 and GAMEDONE == False and np.sum(TURNLIST) != 9:
                AIMove(buttons, label);
        elif GAMEDONE == True:
            reset(buttons, label);
def markBox(buttons, idx, label):
    global BEGINNING;
    global GAMEMODE;
    global TURNLIST;
    global POLIST;
    global PXLIST;
    global GAMEDONE;
    imageOpath = os.getcwd() + "/figures/o.png";
    imageXpath = os.getcwd() + "/figures/x.png";
    imageO = Tk.PhotoImage(file=imageOpath);
    imageX = Tk.PhotoImage(file=imageXpath);
    if np.sum(TURNLIST)%2 == 0:
        buttons[idx].config(image=imageO);
        buttons[idx].photo = imageO;
        POLIST[idx/3, idx%3] = 1;
        if checkWinButton(buttons, POLIST) == True:
            if GAMEMODE == -1:
                label.config(text="AI O won!!!\nPress any box to reset");
            else:
                label.config(text="Player O won!!!\nPress any box to reset");
            GAMEDONE = True;
        else:
            label.config(text="Player X");
    else:
        buttons[idx].config(image=imageX);
        buttons[idx].photo = imageX;
        PXLIST[idx/3, idx%3] = 1;
        if checkWinButton(buttons, PXLIST) == True:
            if GAMEMODE == 1:
                label.config(text="AI X won!!!\nPress any box to reset");
            else:
                label.config(text="Player X won!!!\nPress any box to reset");
            GAMEDONE = True;
        else:
            label.config(text="Player O");
    TURNLIST[idx] = 1;
    if np.sum(TURNLIST) == 9 and GAMEDONE == False:
        label.config(text="Nobody won\nPress any box to reset");
        GAMEDONE = True;
def checkWinButton(buttons, PLIST):
    if np.sum(PLIST) >= 3:
        for i in range(3):
            if np.sum(PLIST[i]) == 3:
                buttons[3*i+0].config(background="red", activebackground="red");
                buttons[3*i+1].config(background="red", activebackground="red");
                buttons[3*i+2].config(background="red", activebackground="red");
                return True;
            if np.sum(PLIST[:, i]) == 3:
                buttons[0+i].config(background="red", activebackground="red");
                buttons[3+i].config(background="red", activebackground="red");
                buttons[6+i].config(background="red", activebackground="red");
                return True;
        if (PLIST[0,0]+PLIST[1,1]+PLIST[2,2]) == 3:
            buttons[0].config(background="red", activebackground="red");
            buttons[4].config(background="red", activebackground="red");
            buttons[8].config(background="red", activebackground="red");
            return True;
        if (PLIST[0,2]+PLIST[1,1]+PLIST[2,0]) == 3:
            buttons[2].config(background="red", activebackground="red");
            buttons[4].config(background="red", activebackground="red");
            buttons[6].config(background="red", activebackground="red");
            return True;
    return False;

def reset(buttons, label):
    global BEGINNING;
    global GAMEMODE;
    global TURNLIST;
    global POLIST;
    global PXLIST;
    global GAMEDONE;
    BEGINNING = True;
    GAMEMODE = 0;
    TURNLIST = np.zeros(9);
    POLIST = np.zeros((3, 3));
    PXLIST = np.zeros((3, 3));
    GAMEDONE = False;
    setBeginning(buttons, label);
def setBeginning(buttons, label):
    for i in range(9):
        initButton(buttons[i]);
    label.config(text="");
    imageAIOpath  = os.getcwd() + "/figures/ai_o.png";
    imageNoAIpath = os.getcwd() + "/figures/no_ai.png";
    imageAIXpath  = os.getcwd() + "/figures/ai_x.png";
    imageAIO  = Tk.PhotoImage(file=imageAIOpath);
    imageNoAI = Tk.PhotoImage(file=imageNoAIpath);
    imageAIX  = Tk.PhotoImage(file=imageAIXpath);
    buttons[3].config(image=imageAIO);
    buttons[4].config(image=imageNoAI);
    buttons[5].config(image=imageAIX);
    buttons[3].photo = imageAIO;
    buttons[4].photo = imageNoAI;
    buttons[5].photo = imageAIX;
    label.config(text="Choose a mode");
def setGame(buttons, label):
    for i in range(9):
        initButton(buttons[i]);
    label.config(text="Player O");
def initButton(button):
    imageEpath = os.getcwd() + "/figures/e.png";
    imageE = Tk.PhotoImage(file = imageEpath);
    button.config(image=imageE, borderwidth=2, height=120, width=120,\
                  background="white", activebackground="light grey",\
                  highlightbackground="black");
    button.photo = imageE;

if __name__ == "__main__":
    root = Tk.Tk();   
    root.title("Tic Tac Toe");
    root.configure(background="white");
    
    label = Tk.Label(root, height=2, font="times 24", bg="white");
    label.grid(row=0, column=0, columnspan=3);
 
    b0=Tk.Button(root, bg="white");
    b1=Tk.Button(root, bg="white");
    b2=Tk.Button(root, bg="white");
    b3=Tk.Button(root, bg="white");
    b4=Tk.Button(root, bg="white");
    b5=Tk.Button(root, bg="white");
    b6=Tk.Button(root, bg="white");
    b7=Tk.Button(root, bg="white");
    b8=Tk.Button(root, bg="white");
    buttons = [b0, b1, b2, b3, b4, b5, b6, b7, b8];
    buttons[0].config(command=lambda:playerMove(buttons, 0, label));
    buttons[1].config(command=lambda:playerMove(buttons, 1, label));
    buttons[2].config(command=lambda:playerMove(buttons, 2, label));
    buttons[3].config(command=lambda:playerMove(buttons, 3, label));
    buttons[4].config(command=lambda:playerMove(buttons, 4, label));
    buttons[5].config(command=lambda:playerMove(buttons, 5, label));
    buttons[6].config(command=lambda:playerMove(buttons, 6, label));
    buttons[7].config(command=lambda:playerMove(buttons, 7, label));
    buttons[8].config(command=lambda:playerMove(buttons, 8, label));
    for i in range(9):
        buttons[i].grid(row=(i/3+1), column=i%3);
    reset(buttons, label);

    root.mainloop();











 
