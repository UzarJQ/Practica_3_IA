from Tkinter import *
import tkMessageBox
from agents import *

class TreasureWorld:
    
    def __init__(self, agent, rows=4, cols=6):
        
        self.agent = agent
        
        self.board = [['safe' for i in range(cols)] for j in range(rows)]
        self.visible = [[False for i in range(cols)] for j in range(rows)]
        self.visible[0][0] = True
        
        self.treasure_position = [0, 5]
        
        self.board[0][4] = 'hole'
        self.board[2][1] = 'hole'
        self.board[3][5] = 'hole'
        
        self.rows = rows
        self.cols = cols
        self.width = 250 + 152 * cols
        self.height = 40 + 152 * rows
        
        self.window = Tk()
        self.window.resizable(False, False)
        self.window.title("Find the Treasure!")
        self.canvas = Canvas(self.window, width=self.width, height=self.height, bg='#ffffcc')
        explorer_image = PhotoImage(file="img/explorer.gif")
        treasure_image = PhotoImage(file="img/treasure.gif")
        hole_image = PhotoImage(file="img/hole.gif")
        safe_image = PhotoImage(file="img/safe.gif")
        breeze_image = PhotoImage(file="img/breeze.gif")
        darkness_image = PhotoImage(file="img/darkness.gif")
        self.images = {'explorer': explorer_image, 'treasure': treasure_image, 
                       'hole': hole_image, 'safe': safe_image, 
                       'breeze': breeze_image, 'darkness': darkness_image}
        
        self.b_next = Button(self.window, text="Next Step", command=self.next_step, font=("Helvetica", 20))
        self.b_next.place(x=(20 + 152 * cols + 115), y=200, anchor=CENTER)
        self.l_player = Label(self.window, text="", font=("Helvetica", 20), bg='#ffffcc', fg="blue")
        self.l_player.place(x=(20 + 152 * cols + 115), y=280, anchor=CENTER)
        
        self.canvas.pack()
        self.draw()
        self.window.mainloop()


    def next_step(self):
        breeze = self.near_pit(self.agent.x, self.agent.y)
        glitter = [self.agent.x, self.agent.y] == self.treasure_position
        percept = (breeze, glitter)
        
        self.l_player.config(text='...')
        self.canvas.update()
        action = self.agent.program(percept)
        self.l_player.config(text=action)
        self.canvas.update()

        self.explorer_position = [self.agent.x, self.agent.y]
        self.visible[self.agent.x][self.agent.y] = True
        self.draw()
        
        if self.board[self.agent.x][self.agent.y] == 'hole':
            self.b_next.config(state=DISABLED)
            self.canvas.update()
            self.canvas.after(500)
            self.agent.x, self.agent.y = -1, -1
            for i in range(self.rows):
                for j in range(self.cols):
                    if self.board[i][j] == 'hole':
                        self.visible[i][j] = True
            self.visible[self.treasure_position[0]][self.treasure_position[1]] = True
            self.draw()
            tkMessageBox.showerror("GAME OVER", "The explorer is falling through the hole...")
            return
        elif ([self.agent.x, self.agent.y] == self.treasure_position) and action == 'Grab':
            self.b_next.config(state=DISABLED)
            for i in range(self.rows):
                for j in range(self.cols):
                    if self.board[i][j] == 'hole':
                        self.visible[i][j] = True
            self.draw()
            tkMessageBox.showinfo("YOU WON!", "You found the treasure!!")
            return
        elif action == 'GetOut':
            self.b_next.config(state=DISABLED)
            for i in range(self.rows):
                for j in range(self.cols):
                    if self.board[i][j] == 'hole':
                        self.visible[i][j] = True
            self.visible[self.treasure_position[0]][self.treasure_position[1]] = True
            self.draw()
            tkMessageBox.showinfo("YOU QUIT!", "The explorer could not find the treasure!!")
            return

    def draw(self):
        
        self.canvas.delete(ALL)
        
        for i in range(self.rows):
            for j in range(self.cols):
                x = 20 + 152 * j
                y = 20 + 152 * i 
                if self.visible[i][j]:
                    img = self.images[self.board[i][j]]
                    self.canvas.create_image(x, y, image=img, anchor=NW)
                    if [i, j] == [self.agent.x, self.agent.y]:
                        self.canvas.create_image(x, y, image=self.images['explorer'], anchor=NW)
                    if self.near_pit(i, j) and self.board[i][j] != 'hole':
                        self.canvas.create_image(x, y, image=self.images['breeze'], anchor=NW)
                    if [i, j] == self.treasure_position:
                        self.canvas.create_image(x, y, image=self.images['treasure'], anchor=NW)
                else:
                    img = self.images['darkness']
                    self.canvas.create_image(x, y, image=img, anchor=NW)
        self.canvas.update()

    def near_pit(self, x, y):
        for (i, j) in [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]:
            if 0 <= i < self.rows and 0 <= j < self.cols:
                if self.board[i][j] == 'hole':
                    return True
        return False




if __name__ == "__main__":
    rows = 4
    cols = 6
    agent = RandomTreasureAgent(rows, cols)
    #agent = PLTreasureAgent(rows, cols)
    world = TreasureWorld(agent, rows, cols)
    