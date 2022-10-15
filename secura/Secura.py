import time # for file make time and destructing time knowlege gathering.....
# from tkinter import * #Gui for our desktop applic
from PIL import Image,ImageFilter # this is our image library that helps in opening the image..
from tkinter import filedialog,messagebox,Toplevel,Entry,Menu,Label,Button,Tk # extra things..
from pickle import dump, load # file handling done by this guy...
# class to create the .skr extension which is mapped to file 
class secureimg:
    def __init__(self, Rasta, samay, gopniyata, kavach) -> None:
        self.Img = Image.open(str(Rasta)) # the actual image file for which this all thing is done ...
        self.MakeTime  = time.time() # this will store at what time .skr file and object for it is made..
        self.Duration  = samay # dUration after making which the file is nul and void..
        self.DestructTime = self.MakeTime + self.Duration # the time at which file will be corruoted or say not good to see..
        self.ThereIsPaswword = gopniyata # password proctection is give or not ..
        self.Password = kavach # password proctection is give then what is it actually..

    # you want to see the file this is the function for it..
    def dikado(image):
        def dr():
            entered_password = e3.get()
            if(entered_password == image.Password):
                image.Img.show()
            else:
                messagebox.showerror(title="Fas gaye ap to", message="BHAI PASSWORD SAHI DALO time NIKAL JA RAHA HAI")
                dr()
            return

        # there is apassword and file is not corrupted yet...
        if (image.DestructTime > time.time() and image.ThereIsPaswword==True):
            open_window = Toplevel()
            label3 = Label(open_window, text="Enter the encrypted key")
            e3 = Entry(open_window)
            label3.grid(row=1,column=0,padx=20,pady=10)
            e3.grid(row=2,column=2)
            Submit_btn = Button(open_window, text="submit",command=dr)
            Submit_btn.grid(row=3,column=0,padx=20, pady=10)

        # File has not been corupted by the program  and has no password
        elif(image.DestructTime > time.time()):
            image.Img.show()

        else:
            if(image.ThereIsPaswword==False):# No password on the file but file is corrupted
                t=image.Img
                t=t.crop((0,0,t.width/2,t.height/5))# showing the corrupted file...
                t=t.filter(ImageFilter.BoxBlur(7))
                t.show()
            else:
                # file is corrupt and due to fact it was encrypted it was deleted from the System or corrupted badly.
                image.Img = image.Img.crop( (0,0,image.Img.width/2,image.Img.height/3) )
                dump(image , open(str(root.filename2), "wb"))
                image.Img.show()

def opener():
    root.filename2 = filedialog.askopenfilename(initialdir="/", title="Select A File",  filetypes=(("secure files","*.skr"),("all files", "*.*")))
    file_to_object = load(open(root.filename2, "rb"))
    secureimg.dikado(file_to_object)

def insert_file():
    def fr():
        p1=e1.get()#p1 = time in seconds after which file must be corrupted.........
        p2=e2.get() # p2 = password carrting variable 

        #get the details ...
        time_file=0 # in seconds 
        if p1.isnumeric:
            time_file = int(p1)
        else:
            time_file = 60

        givenPassword = False  # setting the password or not
        passkey = "" # The actual password

        if p2=="":
            givenPassword = False
            passkey=""
        else:
            passkey = p2
            givenPassword = True

        tmp = secureimg(root.filename, time_file, givenPassword, passkey)
        root.filename1 = filedialog.asksaveasfile(initialdir="/", title = "Select file",filetypes = (("all files","*.*"),))
        dump(tmp , open(str(root.filename1.name), "wb"))

        return 

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

    Submit_btn = Button(inerter, text="submit",command=fr)
    Submit_btn.grid(row=4,column=0,padx=20,pady=10)

root = Tk()
# root = Tk()#main Window
root.title('secura') # application is SECURA becuase why not does it not secure your image.
root.geometry("800x600") #lambai motai avam golai

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