import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk, Image
import maze_solver
from copy import deepcopy
import numpy as np

debug = 0

class gui:
    image_scale = 1

    def __init__(self) -> None:
        self.imageObservers = []

        self.root = tk.Tk()
        self.root.title("Maze Solver")
        # self.root.state('zoomed')#maximize the window
        return

    def add_function_buttons(self,row=0,column=1):
        #setup the base frame for the buttons
        self.buttonFrame = tk.Frame(self.root, background="Blue")
        self.buttonFrame.grid(row=row,column=column,sticky="NSEW")
        self.root.columnconfigure(1,weight=1)
        self.buttonFrame.columnconfigure(0,weight=1)
        #make gray
        makeGrayButton = tk.Button(self.buttonFrame, text='Turn Image Grayscale', command = lambda: self.update_image(maze_solver.makeGrayImage(self.get_PIL_image())))
        makeGrayButton.grid(row=0,column=0,sticky="EW") 
        #binarize
        binarizeButton = tk.Button(self.buttonFrame, text='Binarize Image', command = lambda: self.save_np_image(maze_solver.binarizeImage(self.get_PIL_image())))
        binarizeButton.grid(row=1,column=0,sticky="EW") 
        #crop
        autoCropButton = tk.Button(self.buttonFrame, text='Auto Crop Image', command = lambda: self.save_np_image(maze_solver.cropImage(self.get_np_image())) )
        autoCropButton.grid(row=2,column=0,sticky="EW") 
        #expand Walls
        expandWallsbutton = tk.Button(self.buttonFrame, text='Expand Black Area', command = lambda: self.save_np_image(maze_solver.expand_black_area(self.get_np_image(),1)) )
        expandWallsbutton.grid(row=3,column=0,sticky="EW") 
        #get start/end
        lastClickLabel = tk.Label(self.buttonFrame, text="Last Clicked Image Coordinates (X, Y)")
        lastClickLabel.grid(row=4,column=0,sticky="EW") 
        self.clickCoordantes = tk.Label(self.buttonFrame,text="(XXX, YYY)")
        self.clickCoordantes.grid(row=5,column=0,sticky="EW") 
        expandSetStartButton = tk.Button(self.buttonFrame, text='Save as Start Location', command = lambda: self.set_start_coords())
        expandSetStartButton.grid(row=6,column=0,sticky="EW") 
        expandSetEndButton = tk.Button(self.buttonFrame, text='Save as End Location', command = lambda: self.set_end_coords())
        expandSetEndButton.grid(row=7,column=0,sticky="EW") 
        #run astar
        runAstarButton = tk.Button(self.buttonFrame, text='Run A-Star', command = lambda: self.save_np_image(maze_solver.runAStar(self.get_np_image(),self.start,self.end)) )
        runAstarButton.grid(row=8,column=0,sticky="EW") 
        
    def add_image_frame(self,row=0,column=0):
        #setup the base frame for the image
        self.imageFrame = tk.Frame(self.root, background="Red")
        self.imageFrame.grid(row=row,column=column,sticky="NSEW")
        self.root.columnconfigure(0,weight=3)
        self.root.rowconfigure(0,weight=1)

        #image ui setup
        uploadImageButton = tk.Button(self.imageFrame, text='Upload Image', command = lambda:self.upload_image())
        uploadImageButton.grid(row=0,column=0,sticky="EW") 
        self.imageFrame.columnconfigure(0,weight=1)
        self.mazeImage = tk.Canvas(self.imageFrame)
        self.mazeImage.grid(row=1,column=0,columnspan=3,sticky="NSEW")
        self.imageFrame.rowconfigure(1,weight=3)
        self.mazeImageContainer = self.mazeImage.create_image(0, 0, anchor="nw", tags="IMG")
        self.bind_image_observer(self.render_image)

        # resize, you need to resize the image
        self.root_width = 0
        self.root_hight =0
        self.root.bind("<Configure>", self.resize_maze)
        self.mazeImage.bind('<1>', self.click_canvas_callback)

    def set_start_coords(self):
        self.start = (self.clicked_image_x,self.clicked_image_y)

    def set_end_coords(self):
        self.end = (self.clicked_image_x,self.clicked_image_y)

    def get_PIL_image(self):
        return self.sourceImage

    def get_np_image(self):
        np_array = np.array(self.get_PIL_image())
        if len(np_array.shape) == 3:
            return np_array[:,:,0]
        return np_array

    def save_np_image(self, np_image):
        image = Image.fromarray(np.uint8(np_image))
        self.sourceImage = image
        self.update_image(self.sourceImage)

    def click_canvas_callback(self, e):
        print("Detected Click")
            
        x,y = self.canvas_to_image_cords(canvas=self.mazeImage, x=e.x, y=e.y, image=self.img, tagOrId='IMG') # Can also pass img_tag as tagOrId
        self.undo_image_scaling()
        self.clickCoordantes.configure(text=f"({x}, {y})")
        self.clicked_image_x = x
        self.clicked_image_y = y

    def undo_image_scaling(self):
        source_x = self.sourceImage.width
        source_y = self.sourceImage.height

        display_x = self.img.width()
        display_y = self.img.height()

        if source_x > display_x or source_y > display_y:
            print("NEED RESIZE")

    def canvas_to_image_cords(self, canvas: tk.Canvas, x: int, y: int, image: ImageTk.PhotoImage, tagOrId=''):
        anchor = 'center'
        if tagOrId:
            anchor = canvas.itemcget(tagOrId, 'anchor')
        
        w, h = canvas.winfo_reqwidth(), canvas.winfo_reqheight()
        
        if anchor == 'center':
            img_xpos, img_ypos = image.width()/2, image.height()/2
            start_x, start_y = img_xpos-w/2, img_ypos-h/2
        elif anchor == 'nw':
            start_x, start_y = 0, 0
        # And so on for different anchor positions if you want to make this more modular
        
        req_x, req_y = start_x+x, start_y+y

        return req_x, req_y

    # check to see if the whole maze image is scaled to fit int  the gui
    # true if it fits false if it dont
    def check_image_scale(self):
        canvas_width = self.mazeImage.winfo_width()
        canvas_height = self.mazeImage.winfo_height()

        source_width = self.sourceImage.width
        source_height = self.sourceImage.height

        rendered_width = self.img.width()
        rendered_height = self.img.height()
        if canvas_width < rendered_width or canvas_height < rendered_height:
            PIL_image = ImageTk.getimage(self.img)
            PIL_image.thumbnail((canvas_width,canvas_height))
            self.update_image(PIL_image)
            return False
        elif (source_width > canvas_width > rendered_width and 
                source_height > canvas_height > rendered_height):
            self.update_image(self.sourceImage)
        return True

    def render_image(self):
        if self.check_image_scale():
            self.mazeImage.itemconfig(self.mazeImageContainer, image=self.img)

    def upload_image(self):
        f_types = [('Jpg Files', '*.jpg'), ('Any File', '*')]
        filename = filedialog.askopenfilename(filetypes=f_types)
        self.sourceImage = Image.open(filename)
        image = ImageTk.PhotoImage(self.sourceImage)
        self.update_image(image)
    
    # bind image observer functions
    def bind_image_observer(self, function):
        if function in self.imageObservers:
            print("Function already an observer")
            return
        self.imageObservers.append(function)

    #update image and call observing functions
    def update_image(self, newImage):
        if not type(newImage) is ImageTk.PhotoImage: # if the image is the wrong type try and fix it
            if type(newImage) is Image.Image:
                try:
                    newImage = ImageTk.PhotoImage(newImage)
                except:
                    print("Error Occurred when converting from PIL.Image to an PhotoImage")
            else:
                try:
                    newImage = ImageTk.PhotoImage(newImage)
                except:
                    print(f"Cant convert from {type(newImage)} to required format")
        print("updating image")
        self.img = newImage
        
        for callback in self.imageObservers: #call image update functions
            callback()
    
    def resize_maze(self, event: tk.Event):
        if event.widget.master == None:
            if (self.root_width != event.width) and (self.root_hight != event.height):
                self.root_width, self.root_hight = event.width,event.height
                print(f"window hight now {self.root_hight}, and the width is {self.root_width}")
                self.render_image()

    # Start
    def run(self):
        self.add_image_frame()
        self.add_function_buttons()
        self.root.mainloop()


if __name__ == "__main__":
    mazeGui = gui()
    mazeGui.run()