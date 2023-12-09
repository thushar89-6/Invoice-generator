import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
import database
import datetime
import generate_bill
from tkinter import filedialog
import shutil
from tkinter import messagebox
import datetime


def ent(event):
    addentry()
            

def addentry():
    sno=database.rowcount()+1
    date=datetime.date.today().strftime("%d/%m/%Y")
    consignee=entry1.get()
    destination=entry2.get()
    weight=entry3.get()
    amount=entry4.get()
    entry1.delete(0, tk.END)
    entry2.delete(0, tk.END)
    entry3.delete(0, tk.END)
    entry4.delete(0, tk.END)
    try:
        if not amount=="":
                float(amount)
        database.add_row(sno,date,consignee,destination,weight,amount)
        populatetable()
    except:
        messagebox.showinfo("Error","Amount must be number")
    entry1.focus()

        

def deleteentry():
        database.deleterow()
        populatetable()

def download():
       billno=database.getbno()
       generate_bill.generatepdf(str(billno))
       file_path = filedialog.asksaveasfilename(initialfile="Bill_No_"+str(billno)+".pdf",defaultextension=".pdf")
       shutil.copy2("bills\Bill_No_"+str(billno)+".pdf",file_path)
       database.deleteall()
       populatetable()
       label_1.configure(text="Bill No: "+str(database.getbnowithoutincrement()))
         
       
def editentry():
    window = ctk.CTkToplevel(root)
    window.attributes("-topmost",True)
    window.geometry("200x300")
    window.title("Edit entry")
    window.grid_columnconfigure(0,weight=1)
    def fn1(choice):
        d1,d2,d3,d4=database.getcontent(choice)
        e1.insert(tk.END,str(d1))
        e2.insert(tk.END,str(d2))
        e3.insert(tk.END,str(d3))
        e4.insert(tk.END,str(d4))

    cbox=ctk.CTkComboBox(window, values=[str(x) for x in range(1,database.rowcount()+1)],command=fn1)
    cbox.set("Sr.No.")
    cbox.grid(row=0,column=0,padx=30,pady=(20,5))
    e1=ctk.CTkEntry(window,placeholder_text="Consignee")
    e2=ctk.CTkEntry(window,placeholder_text="Destination")
    e3=ctk.CTkEntry(window,placeholder_text="Weight")
    e4=ctk.CTkEntry(window,placeholder_text="Amount")
    e1.grid(row=2,column=0,padx=30,pady=5)
    e2.grid(row=3,column=0,padx=30,pady=5)
    e3.grid(row=4,column=0,padx=30,pady=5)
    e4.grid(row=5,column=0,padx=30,pady=(5,20))
    def ffn1():
        d1=e1.get()
        d2=e2.get()
        d3=e3.get()
        d4=e4.get()
        try:
            if not d4=="":
                float(d4)
                id=cbox.get()
                database.setcontent(id,d1,d2,d3,d4)
                window.destroy()
                populatetable()
            else:
                id=cbox.get()
                database.setcontent(id,d1,d2,d3,0)
                window.destroy()
                populatetable()
        except:
            messagebox.showinfo("Error","Amount must be number")
        
    bb = ctk.CTkButton(window,text="Save",command=ffn1)
    bb.grid(row=6,column=0)
    window.mainloop()

def populatetable():
        mydict=database.allrows()
        table.delete(*table.get_children())
        for row in mydict:
                table.insert('', tk.END, values=row)
        table.grid(row=0,column=0,sticky='nsew',padx=10,pady=10,columnspan=5)
        total=database.totalamount()
        lastrow=("","","","","Total:",total)
        table.insert('',tk.END,values=lastrow)
    
root = ctk.CTk()
style = ttk.Style()
style.theme_use("default")
if root._get_appearance_mode()=="dark":
        style.configure("Treeview",
                                background="#2a2d2e",
                                foreground="white",
                                rowheight=30,
                                fieldbackground="#343638",
                                bordercolor="#343638",
                                borderwidth=0,
                                font=('Arial', 16),
                                )
        style.map('Treeview', background=[('selected', '#22559b')])
        
        style.configure("Treeview.Heading",
                                background="#343638",
                                foreground="white",
                                relief="flat",
                                font=('Arial', 16))
        style.map("Treeview.Heading",
                        background=[('active', '#3484F0')])
else:
        style.configure("Treeview",
                                background="#ebebeb",
                                foreground="black",
                                rowheight=30,
                                fieldbackground="white",
                                bordercolor="#343638",
                                borderwidth=0,
                                font=('Arial', 16),
                                )
        style.map('Treeview', background=[('selected', '#22559b')])
        
        style.configure("Treeview.Heading",
                                background="#dbdbdb",
                                foreground="black",
                                relief="flat",
                                font=('Arial', 16))
        style.map("Treeview.Heading",
                        background=[('active', '#3484F0')])
root.title("Invoice Generator")
root.iconbitmap('bills\icon.ico')
root.geometry("780x520")

root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(0, weight=1)

f1=ctk.CTkFrame(root,
                width=200,
                corner_radius=0)
f1.grid(row=0, column=0, sticky="nswe")

f2 = ctk.CTkFrame(master=root)
f2.grid(row=0, column=1, sticky="nswe", padx=15, pady=15)

f2.grid_rowconfigure(0,weight=1)
f2.grid_columnconfigure(0,weight=1)

column=["Sr.No.","Date","Consignee","Destination","Weight","Amount"]
table = ttk.Treeview(f2, columns=column,show='headings')
for col in column:
        table.heading(col, text=col)
        table.column(col,anchor="center",width=100)
populatetable()

label_1 = ctk.CTkLabel(master=f1,
                        text="Bill No: "+str(database.getbnowithoutincrement()),
                        font=("Roboto Medium", -16))
label_1.grid(row=1, column=0, pady=(10,0), padx=38, sticky='w')
label_2 = ctk.CTkLabel(master=f1,
                        text="Date: "+str(datetime.date.today().strftime("%d/%m/%Y")),
                        font=("Roboto Medium", -16))
label_2.grid(row=2, column=0, pady=5, padx=30)

entry1=ctk.CTkEntry(f1,placeholder_text="Consignee")
entry2=ctk.CTkEntry(f1,placeholder_text="Destination")
entry3=ctk.CTkEntry(f1,placeholder_text="Weight")
entry4=ctk.CTkEntry(f1,placeholder_text="Amount")
entry1.grid(row=3,column=0,padx=30,pady=(10,5))
entry2.grid(row=4,column=0,padx=30,pady=5)
entry3.grid(row=5,column=0,padx=30,pady=5)
entry4.grid(row=6,column=0,padx=30,pady=5)

root.bind("<Return>",ent)

entry1.bind('<Down>', lambda event:entry2.focus())
entry1.bind('<Up>', lambda event:entry4.focus())
entry1.bind('<Return>', lambda event:entry2.focus())

entry2.bind('<Down>', lambda event:entry3.focus())
entry2.bind('<Up>', lambda event:entry1.focus())
entry2.bind('<Return>', lambda event:entry3.focus())

entry3.bind('<Down>', lambda event:entry4.focus())
entry3.bind('<Up>', lambda event:entry2.focus())
entry3.bind('<Return>', lambda event:entry4.focus())

entry4.bind('<Down>', lambda event:entry1.focus())
entry4.bind('<Up>', lambda event:entry3.focus())
entry4.bind('<Return>', ent)





btn1=ctk.CTkButton(f1,text="Add Entry",command=addentry)
btn1.grid(row=7,column=0,padx=30,pady=20)



btn4=ctk.CTkButton(f2,text="Edit entry",command=editentry)
btn4.grid(row=1,column=3,sticky='e',padx=5,pady=5)

btn2=ctk.CTkButton(f2,text="Delete last entry",command=deleteentry)
btn2.grid(row=1,column=2,sticky='e',padx=5,pady=5)

btn3=ctk.CTkButton(f2,text="Download",command=download)


btn3.grid(row=1,column=4,sticky='e',padx=5,pady=5)
def about():
    window = ctk.CTkToplevel(root)
    window.attributes("-topmost",True)
    window.geometry("400x420")
    window.title("About")
    window.grid_columnconfigure(0,weight=1)
    l1=ctk.CTkLabel(window,text="This project was made by,",font=("Roboto Medium", -14))
    l1.grid(row=0,column=0,sticky='w',padx=10,pady=10)
    l2=ctk.CTkLabel(window,text="Sriram Kini (4NM21CS170)",font=("Roboto Medium", -14))
    l2.grid(row=1,column=0,sticky='w',padx=30,pady=0)
    l3=ctk.CTkLabel(window,text="Sudesh Nayak (4NM21CS175)",font=("Roboto Medium", -14))
    l3.grid(row=2,column=0,sticky='w',padx=30,pady=0)
    l4=ctk.CTkLabel(window,text="Thushar (4NM21CS193)",font=("Roboto Medium", -14))
    l4.grid(row=3,column=0,sticky='w',padx=30,pady=0)
    l5=ctk.CTkLabel(window,text="Yasir Manzoor Sheikh (4NM21CS215)",font=("Roboto Medium", -14))
    l5.grid(row=4,column=0,sticky='w',padx=30,pady=(0,20))
    l6=ctk.CTkLabel(window,text="Under the guidance of,",font=("Roboto Medium", -14))
    l6.grid(row=5,column=0,sticky='w',padx=10,pady=0)
    l7=ctk.CTkLabel(window,text="Dr. Radhakrishna",font=("Roboto Medium", -14))
    l7.grid(row=6,column=0,sticky='w',padx=30,pady=0)
    l8=ctk.CTkLabel(window,text="Associate Professor,",font=("Roboto Medium", -14))
    l8.grid(row=7,column=0,sticky='w',padx=30,pady=0)
    l9=ctk.CTkLabel(window,text="Dept. of Comp. Science & Eng.",font=("Roboto Medium", -14))
    l9.grid(row=8,column=0,sticky='w',padx=30,pady=0)
    l10=ctk.CTkLabel(window,text="NMAM Inst. of Technology, Nitte.",font=("Roboto Medium", -14))
    l10.grid(row=8,column=0,sticky='w',padx=30,pady=0)
    l11=ctk.CTkLabel(window,text="As part of internship - II activity (April 2023).",font=("Roboto Medium", -14))
    l11.grid(row=9,column=0,sticky='w',padx=10,pady=(20,0))
    l12=ctk.CTkLabel(window,text="It involves a GUI where user can make/edit entries and",font=("Roboto Medium", -14))
    l12.grid(row=10,column=0,sticky='w',padx=10,pady=0)
    l13=ctk.CTkLabel(window,text="generate the invoice in pdf format.",font=("Roboto Medium", -14))
    l13.grid(row=11,column=0,sticky='w',padx=10,pady=0)
   
btn5=ctk.CTkButton(f1,text="""Invoice Generator
Project""",font=("Roboto Medium", -16),fg_color='#2b2b2b',border_color='#343638',border_width=1,border_spacing=8,command=about)
btn5.grid(row=0,column=0,padx=30,pady=20)

root.mainloop()

