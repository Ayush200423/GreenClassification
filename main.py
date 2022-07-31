from cv2_object_detection import ObjectDetection
from database import Database
from tkinter import *

class Controller:
    def __init__(self):
        self.db = Database()

        self.window = Tk()
        self.window.geometry('340x440') 
        self.window.title("Login")

        self.auth = StringVar()
        self.auth.set("")

        self.count_recyclable = StringVar()
        self.count_recyclable.set(0)

        self.window.configure(background = "black")

        Label (self.window, text = "Username", bg="black", fg="white", font="Arial 13 bold") .grid(row = 1, column = 0, sticky = W)
        self.username_entry = Entry(self.window, width = 20, bg = "white", fg = "black")
        self.username_entry.grid(row = 2, column = 0, sticky = W)

        Label (self.window, text = "Password", bg="black", fg="white", font="Arial 13 bold") .grid(row = 3, column = 0, sticky = W)
        self.password_entry = Entry(self.window, width = 20, bg = "white", fg = "black")
        self.password_entry.grid(row = 4, column = 0, sticky = W)

        Button(self.window, text = "Start WebCam", width = 12, command = self.submit) .grid(row = 5, column = 0, sticky = W)

        self.window.mainloop()
            
    def submit(self):
        self.username = self.username_entry.get()
        self.password = self.password_entry.get()
        if self.username == "" or self.password == "":
            return
        try:
            self.db.add_user(self.username, self.password)
        except:
            if self.db.authenticate_user(self.username, self.password):
                self.video()
            else:
                print("Error: Wrong Password.")
                quit()
        else:
            self.video()

    def video(self):
        model_path = "dnn_model/yolov4-tiny.weights"
        config_path = "dnn_model/yolov4-tiny.cfg"
        detection = ObjectDetection(model_path, config_path)
        detection.detect_items(self.username)

Controller()