from tkinter import *
from pytube import YouTube




def Downloader():     
    url =YouTube(str(link.get()))
    video = url.streams.first()
    video.download()
    Label(root, text = 'DOWNLOADED', font = 'arial 15').place(x= 180 , y = 210)  






# create window
root = Tk()
root.geometry('500x300')
root.resizable(0,0)
root.title("Trapistan Zindabad")


# header
Label(root,text = 'Piracy', font ='arial 20 bold').pack()


# search bar field
link = StringVar()

Label(root, text = 'Paste Link Here:', font = 'arial 15 bold').place(x= 160 , y = 60)
link_enter = Entry(root, width = 70,textvariable = link).place(x = 32, y = 90)


# download button
Button(root,text = 'DOWNLOAD', font = 'arial 15 bold' ,bg = 'pale violet red', padx = 2, command = Downloader).place(x=180 ,y = 150)




root.mainloop()