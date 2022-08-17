import time
from tkinter import *
ind = -1
def start():
    import tkinter 
    from tkinter import BOTTOM
    
    window = tkinter.Tk()
    window.title("Car-Facial-recognition-system")
    window.geometry("1000x650")
    window.iconbitmap("icon.ico")
    window.configure(bg="green")
    
    photo = tkinter.PhotoImage(file='logo.gif')
    w = tkinter.Label(window, image=photo)
    w.pack(side="top",expand='no')
   
    """
    image1 = tkinter.PhotoImage(file="lg.gif")
    w = image1.width()
    h = image1.height()
    #window.geometry("%dx%d+0+0" % (w, h))
    panel1 = tkinter.Label(window, image=image1)
    panel1.pack(side='right', fill='both', expand='no')
    """
    image2 = tkinter.PhotoImage(file="background.gif")
    w = image2.width()
    h = image2.height()
    #window.geometry("%dx%d+0+0" % (w, h))
    panel2 = tkinter.Canvas(window,bg="black")
    panel2.pack(side='top', fill='both',expand='yes')
    panel2.create_image(530,70,anchor='nw', image=image2, tag='image2')

    
    def update(delay=1):
        global ind      
        ind += 1
        if ind == 160: ind = 0
        #print (ind)
        image2.configure(format="gif -index " + str(ind))
        window.after(delay, update)
 
    update()
####################################################################################################################################
#                                                                                                                                  #
#                                                               DATASET                                                            #                                                         
####################################################################################################################################
    def data():
        import tkinter as tk

        import tkinter.messagebox as tm
        import numpy as np
        import cv2
        import sys
        class LoginPage():
            def __init__(self):
                self.root=tk.Tk()
                label = tk.Label(self.root, text="Welcome Back Admin",fg="blue")
                label.grid(row=0)
                label_1 = tk.Label(self.root, text="Username")
                label_2 = tk.Label(self.root, text="Password")
                self.entry_1 = tk.Entry(self.root)
                self.entry_2 = tk.Entry(self.root, show="*")
                label_1.grid(row=1, sticky="e")
                label_2.grid(row=2, sticky="e")
                self.entry_1.grid(row=1, column=1)
                self.entry_2.grid(row=2, column=1)

                ## doesn't do anything at this time
                ##checkbox = tk.Checkbutton(self.root, text="Keep me logged in")
                ##checkbox.grid(row=3, columnspan=2)

                logbtn = tk.Button(self.root, text="Login",bg='black',fg='green', command = self._login_btn_clickked)
                logbtn.grid(row=10)
                myButton = tk.Button(self.root, text="Exit",bg='black',fg='red',command = self.buttonPushed)
                myButton.grid(row=10,columnspan=3)

                self.root.mainloop()

            def buttonPushed(self):
                self.root.destroy()


            def _login_btn_clickked(self):
                #print("Clicked")
                username = self.entry_1.get()
                password = self.entry_2.get()

                #print(username, password)

                if username == "admin" and password == "1234":
                    #tm.showinfo("Login info", "Welcome ")
                    class adduser():
                        def __init__(self):
                            self.root1=tk.Tk()
                            label_11 = tk.Label(self.root1, text="User ID")
                            label_12 = tk.Label(self.root1, text="UserName")
                            self.entry_11 = tk.Entry(self.root1)
                            self.entry_12 = tk.Entry(self.root1)
                            label_11.grid(row=1, sticky="e")
                            label_12.grid(row=2, sticky="e")
                            self.entry_11.grid(row=1, column=1)
                            self.entry_12.grid(row=2, column=1)
                            okbtn = tk.Button(self.root1, text="OK",bg='black',fg='green', command = self._OK_btn_clickked)
                            okbtn.grid(row=10)
                            exitButton = tk.Button(self.root1, text="Exit",bg='black',fg='red',command = self.button_exit)
                            exitButton.grid(row=10,columnspan=3)
                            self.root1.mainloop()

                        def button_exit(self):
                            self.root1.destroy()
                        def _OK_btn_clickked(self):
                            #print("Clicked")
                            userid = self.entry_11.get()
                            username = self.entry_12.get()
                            print(userid+"\n", username)

                            id=(userid)
                            name=(username)
                            detector = cv2.CascadeClassifier('/Users/BX1090/Desktop/carsys/haarcascade_frontalface_default.xml')
                            cam=cv2.VideoCapture(0); 
                            samplenumber=0;
                            while(True):
                                ret, img = cam.read()
                                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                                faces = detector.detectMultiScale(gray, 1.3, 5);
                                for (x,y,w,h) in faces:
                                    samplenumber=samplenumber+1;
                        
                                    cv2.imwrite("/Users/BX1090/Desktop/carsys/dataset/"+str(name)+"."+str(id)+"."+str(samplenumber)+".jpg",gray[y:y+h,x:x+w])
                                    cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)
                                    cv2.waitKey(100);

                                cv2.imshow('face',img)
                                cv2.waitKey(1);
                                if(samplenumber>50):
                                    break
                            cam.release()
                            cv2.destroyAllWindows()
                 
                    au=adduser()    

                else:
                    #box.showerror("Login failed", "Incorrect username")
                    tm.showerror("Login error", "Incorrect username or password")

        LP=LoginPage()
#####################################################################################################################################    
#                                                                                                                                   #
#                                                               DATA TRAINING                                                       #
#####################################################################################################################################
    def train():
        import os
        import cv2
        import numpy as np
        from PIL import Image

        recognizer = cv2.face.LBPHFaceRecognizer_create()
        path='/Users/BX1090/Desktop/carsys/dataset'

        def getimagesid(path):
            imagePaths=[os.path.join(path,f) for f in os.listdir(path)]
            faces=[]
            IDs=[]
            for imagePath in imagePaths:
                faceImg=Image.open(imagePath).convert('L');
                faceNp=np.array(faceImg,'uint8')
                ID=int(os.path.split(imagePath)[-1].split('.')[1])
                faces.append(faceNp)
                print(ID)
                IDs.append(ID)
                cv2.imshow("training",faceNp)
                cv2.waitKey(10)
            return IDs,faces

        Ids,faces=getimagesid(path)
        recognizer.train(faces,np.array(Ids))
        recognizer.save('/Users/BX1090/Desktop/carsys/trainer.yml')
        cv2.destroyAllWindows()
#######################################################################################################################################
#                                                                                                                                     #
#                                                                 FACE RECOGNITION                                                    #
#######################################################################################################################################
    def detect():
        import cv2
        import numpy as np

        recognizer = cv2.face.LBPHFaceRecognizer_create()
        recognizer.read('/Users/BX1090/Desktop/carsys/trainer.yml')
        cascadePath = "/Users/BX1090/Desktop/carsys/haarcascade_frontalface_default.xml"
        faceCascade = cv2.CascadeClassifier(cascadePath);


        cam = cv2.VideoCapture(0)
        font = cv2.FONT_HERSHEY_SIMPLEX
        while True:
            ret, im =cam.read()
            gray=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
            faces=faceCascade.detectMultiScale(gray, 1.2,5)
            for(x,y,w,h) in faces:
                cv2.rectangle(im,(x,y),(x+w,y+h),(225,0,0),2)
                Id, conf = recognizer.predict(gray[y:y+h,x:x+w])
                print('face matched',Id)
                if(conf<45):
                    if(Id==1):
                        Id="Mohamed"    
                    elif(Id==2):
                        Id="x"
                    elif(Id==3):
                        Id="y"
                    elif(Id==5):
                        Id="z"
                else:
                    Id="Unknown"
                #cv2.cv.PutText(cv2.cv.fromarray(img),str(id),(x,y+h),font,255)
                cv2.putText(im, str(Id), (x,y-40),font, 1, (255,255,255), 3)
            cv2.imshow('im',im) 
            if cv2.waitKey(10) & 0xFF==ord('q'):
                break
        cam.release()
        cv2.destroyAllWindows()



    #button2 = tkinter.Button(panel1, text='button2')
    #button2.pack(side='right')

    detect = tkinter.Button(window, text = "Detection",bg='#383a39',fg='#a1dbcd' , command =detect)
    detect.pack(padx=5, pady=10, side=BOTTOM)

    tra = tkinter.Button(window, text = "Data Training",bg='#383a39',fg='#a1dbcd' , command =train)
    tra.pack(padx=5, pady=10, side=BOTTOM)
    
    data = tkinter.Button(window, text = "Add New Member",bg='#383a39',fg='#a1dbcd' , command =data)
    data.pack(padx=5, pady=10, side=BOTTOM)
    
    window.mainloop()


if __name__ == "__main__":
    start()
