from email.mime import image
from fileinput import close
import time # for file make time and destructing time knowlege gathering.....
# from tkinter import * #Gui for our desktop applic
from PIL import Image,ImageFilter, ImageTk # this is our image library that helps in opening the image..
from tkinter import BooleanVar, filedialog,messagebox,Toplevel,Entry,Menu,Label,Button,Tk,Canvas,Radiobutton,BooleanVar # extra things..
from pickle import dump, load # file handling done by this guy...
# Python Program to Get IP Address
import uuid

from pyparsing import col
# class to create the .skr extension which is mapped to file 
class secureimg:
    def __init__(self, Rasta, samay, gopniyata, kavach,MacPriority) -> None:
        self.Img = Image.open(str(Rasta)) # the actual image file for which this all thing is done ...
        self.MakeTime  = time.time() # this will store at what time .skr file and object for it is made..
        self.Duration  = samay # dUration after making which the file is nul and void..
        self.DestructTime = self.MakeTime + self.Duration # the time at which file will be corruoted or say not good to see..
        self.ThereIsPaswword = gopniyata # password proctection is give or not ..
        self.Password = kavach # password proctection is give then what is it actually..
        self.forPersonalUse=MacPriority
        self.allowed_machines={}
        self.allowed_machines[ uuid.getnode()]= 'allowed'
        self.corrupted=False
        # MAC Addresses are unique to the computer generating them.
        # By including a MAC address in the UUID
        # you can be sure that two different computers will never generate the same UUID.
        # Because MAC addresses are globally unique,
        # But can be changed by user to a certain value.
        # version-1 UUIDs can be traced back to the computer that generated them

    # you want to see the file this is the function for it..
    def dikado(image):
        def CorruptFile(ImageFile):
            ImageFile = ImageFile.crop((0,0,ImageFile.width/2,ImageFile.height/5))
            ImageFile = ImageFile.filter(ImageFilter.BoxBlur(7))
            return ImageFile
        def showImage(imageFile):
            imageFile.show()
            return
        def dr():
            entered_password = e3.get()
            if(entered_password == image.Password):
                showImage(image.Img)
            else:
                messagebox.showerror(title="Fas gaye ap to", message="BHAI PASSWORD SAHI DALO time NIKAL JA RAHA HAI")
            return
        thisMachine = uuid.getnode()
        # have time.....
        # machinesAllowed = image.allowed_machines.keys()
        # print(machinesAllowed)
        # print(uuid.getnode())
        if image.DestructTime>time.time():#Time bacha hai....
            if(image.forPersonalUse == True):#Only to be opened on single device..
                if(thisMachine in image.allowed_machines):#check if this machine is the machine that was allowed by the user..
                    print("You are right to open the file ")
                    if(image.ThereIsPaswword):#Check if there is password...
                        print("rafter password only you can open the file")
                        open_window = Toplevel()
                        label3 = Label(open_window, text="Enter the encrypted key")
                        e3 = Entry(open_window)
                        label3.grid(row=1,column=0,padx=20,pady=10)
                        e3.grid(row=2,column=2)
                        Submit_btn = Button(open_window, text="submit",command=dr)
                        Submit_btn.grid(row=3,column=0,padx=20, pady=10)
                        return 
                    else:#no password 
                        showImage(image.Img)
                        return
                elif(thisMachine not in image.allowed_machines):
                    image.Img=CorruptFile(image.Img)
                    image.corrupted=True
                    dump(image, open(str(root.filename2), "wb"))
                    showImage(image.Img)
            elif(image.forPersonalUse == False):# no personal Use
                if(image.ThereIsPaswword):
                    open_window = Toplevel()
                    label3 = Label(open_window, text="Enter the encrypted key")
                    e3 = Entry(open_window)
                    label3.grid(row=1,column=0,padx=20,pady=10)
                    e3.grid(row=2,column=2)
                    Submit_btn = Button(open_window, text="submit",command=dr)
                    Submit_btn.grid(row=3,column=0,padx=20, pady=10)
                else:#no password either 
                    showImage(image.Img)
                    return
        # dont have time         
        else:
            #already corrupted
            if (image.corrupted==True):
                showImage(image.Img)
            #not yet corrupted
            else:
                image.Img = CorruptFile(image.Img)
                image.corrupted=True
                dump(image , open(str(root.filename2), "wb"))
                showImage(image.Img)

def opener():
    root.filename2 = filedialog.askopenfilename(initialdir="/", title="Select A File",  filetypes=(("secure files","*.skr"),("all files", "*.*")))
    file_to_object = load(open(root.filename2, "rb"))
    secureimg.dikado(file_to_object)

def insert_file():
    def fr():
        p1=e1.get()#p1 = time in seconds after which file must be corrupted.........
        p2=e2.get() # p2 = password carrting variable 
        p3=bool(hasPersonalProtection.get())# p3 = bool->can open in others 
        #get the details ...
        time_file=0 # in seconds 
        opensInNativeDeviceOnly=p3 
        if p1.isnumeric:
            time_file = int(p1)
        else:
            time_file = 60 #file default time is 60 seconds i.e it will be corrupted in 60 seconds if user dont give the time details
        givenPassword = False  # setting the password or not
        passkey = "" # The actual password
        if p2!="":
            passkey = p2
            givenPassword = True
        # print(time_file,givenPassword,passkey,opensInNativeDeviceOnly)
        tmp = secureimg(root.filename, time_file, givenPassword, passkey,p3)
        root.filename1 = filedialog.asksaveasfile(initialdir="/", title = "Select file",filetypes = (("all files","*.*"),))
        dump(tmp , open(str(root.filename1.name), "wb"))
        return
    def sel():
        pass
    inerter = Toplevel()
    #file to be converted to .skr is asked by the code here from this line of code
    root.filename = str(filedialog.askopenfilename(initialdir="/", title="Select A File", filetypes=(("all files", "*.*"), ("jpg files", "*.jpg"),)))

    label1 = Label(inerter, text="Enter the time period in seconds after which the file must be destroyed/corruped in seconds")
    e1 = Entry(inerter)
    label1.grid(row=1,column=0,padx=20,pady=10)
    e1.grid(row=1,column=2)
    

    label2 = Label(inerter, text="Enter the encrypted key Leave it you dont want encryption..")
    e2 = Entry(inerter)
    label2.grid(row=2,column=0,padx=20,pady=10)
    e2.grid(row=2,column=2)
    
    
    label3 = Label(inerter, text="Enter the encrypted key Leave it you dont want encryption..")
    label3.grid(row=3,column=0,padx=20,pady=10)
    
    hasPersonalProtection = BooleanVar()
    R1 = Radiobutton(inerter, text="All can open the file ", variable=hasPersonalProtection, value=False,command=sel)
    R1.grid(row=4,column=0,padx=20,pady=10)

    R2 = Radiobutton(inerter, text="Only available for this device ", variable=hasPersonalProtection, value=True,command=sel)
    R2.grid(row=5,column=0,padx=20,pady=10)

    Submit_btn = Button(inerter, text="submit",command=fr)
    Submit_btn.grid(row=6,column=0,padx=20,pady=10)

root = Tk()
# root = Tk()#main Window
root.title('secura') # application is SECURA becuase why not does it not secure your image.
root.geometry("1000x900") #lambai motai avam golai


my_menu = Menu(root) # menu uapar ka jo hota hai na file new edit ms word me ek liine me hita hai jo
root.config(menu=my_menu)# configuration of menu

Create_a_file = Menu(my_menu)# islke liye kya comment karu lol samjh jao
my_menu.add_cascade(label="Create a File", menu=Create_a_file)# adding the Create the file menu item in the menu
Create_a_file.add_command(label="insert a file to make it secure", command=insert_file)

View_a_file = Menu(my_menu)
my_menu.add_cascade(label= "View the File", menu=View_a_file)# adding the View the file menu item in the menu
View_a_file.add_command(label="View the file", command=opener)# view the file...

my_menu.add_command(label="Exit",command=root.quit)# this will theow you out actually.. i am not joking

root.mainloop()#loop me gane sunte jao