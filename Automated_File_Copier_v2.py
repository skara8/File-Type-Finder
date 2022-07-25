import tkinter as tk
from tkinter import *
from tkinter import filedialog
import sys
from os import *
import os
import shutil
from datetime import datetime

root = tk.Tk()
root.title("Auto File Copier")
root.iconbitmap(f"{getcwd()}\\FolderIcon.ico")

main_frame = Frame(root, bg='#2a2a3c')
main_frame.pack(fill="both", expand=True)

# widgets in the main frame
main_title = Label(main_frame, text='Automated File and Folder Copier', bg='#c3c3d5', fg='#14141f', font =12, relief=RIDGE)
frame1 = LabelFrame(main_frame, text="Copy files containing specified extension", bg='#e1e1ea', labelanchor='n', highlightcolor='white', highlightthickness=2)
frame2 = LabelFrame(main_frame, text="Copy files or folders containing specified text in the name", bg='#e1e1ea',labelanchor='n', highlightcolor='white', highlightthickness=2)
frame3 = LabelFrame(main_frame, text = 'Move files into separate folders using the files date-modified', bg='#e1e1ea',labelanchor='n', highlightcolor='white', highlightthickness=2)
frame4 = LabelFrame(main_frame, text = 'Move files into separate folders using first (n) characters in the file name', bg='#e1e1ea',labelanchor='n', highlightcolor='white', highlightthickness=2)
# laying out the main frame
main_frame.grid_rowconfigure(1, weight=1)
main_frame.grid_rowconfigure(2, weight=1)
main_frame.grid_columnconfigure(0, weight=1)
main_frame.grid_columnconfigure(1, weight=1)

main_title.grid(row=0, column=0, padx=5, pady=5, sticky="nsew", columnspan=2)
frame1.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
frame2.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")
frame3.grid(row=2, column=0, padx=5, pady=5, sticky="nsew")
frame4.grid(row=2, column=1, padx=5, pady=5, sticky="nsew")

label_source = Label(frame1, text='Enter Source Folder Path')
label_source.grid(row = 0, column = 0, padx = 10, pady = 10)
label_destination = Label(frame1, text='Enter Destination Folder Path')
label_destination.grid(row=2, column= 0, padx = 10, pady = 10)
label_extension = Label(frame1, text='Enter Required Extensions e.g. .jpg .png .mp4')
label_extension.grid(row=4, column= 0, padx = 10, pady = 10)
EntryBoxSource = Entry(frame1, width = 60)
EntryBoxDestination = Entry(frame1, width = 60)
EntryBoxExtension = Entry(frame1, width = 60)
EntryBoxSource.grid(row=1, column=0, padx = 10, pady = 10)
EntryBoxDestination.grid(row=3, column=0, padx = 10, pady = 10)
EntryBoxExtension.grid(row=5, column=0, padx = 10, pady = 10)

label_source_substring = Label(frame2, text='Enter Source Folder Path').grid(row = 0, column = 0, padx = 10, pady = 10)
label_destination_substring = Label(frame2, text='Enter Destination Folder Path').grid(row = 2, column = 0, padx = 10, pady = 10)
label_substring = Label(frame2, text='Enter Required Alphanumeric String').grid(row = 4, column = 0, padx = 10, pady = 10)
EntryBoxSource_substring = Entry(frame2, width = 60)
EntryBoxDestination_substring = Entry(frame2, width = 60)
EntryBox_substring = Entry(frame2, width = 60)
EntryBoxSource_substring.grid(row = 1, column = 0, padx = 10, pady = 10)
EntryBoxDestination_substring.grid(row = 3, column = 0, padx = 10, pady = 10)
EntryBox_substring.grid(row = 5, column = 0, padx = 10, pady = 10)

label_move_source_date = Label(frame3,text='Path containing files for moving into folders').grid(row = 0, column=0, padx = 10, pady = 10)
EntryBoxMoveSource_date = Entry(frame3, width = 60)
EntryBoxMoveSource_date.grid(row=1, column=0, padx = 10, pady = 10)

label_move_source = Label(frame4, text='Path containing files for moving into folders').grid(row = 0, column=0, padx = 10, pady = 10)
label_sort_file_length = Label(frame4, text = 'Number of characters from left to right \nto use for moving files into folders.\ne.g. 01-01-2001 = 10').grid(row = 2, column=0, padx=10,pady=10)
EntryBoxMoveSource = Entry(frame4, width = 60)
EntryBoxMoveSource.grid(row=1, column=0, padx=10, pady = 10)
EntryBoxFileLength = Entry(frame4, width = 20)
EntryBoxFileLength.grid(row=3, column=0, padx=10, pady = 10)

var1 = IntVar()
var2 = IntVar()
Checkbutton(frame1, text="Include subfolders", variable=var1).grid(row=6, sticky=W, padx = 10, pady = 10)
Checkbutton(frame2, text="Include subfolders", variable=var2).grid(row=6, sticky=W, padx = 10, pady = 10)

def browse_button1():
    EntryBoxSource.delete(0, END)
    EntryBoxSource.insert(END, filedialog.askdirectory())
def browse_button2():
    EntryBoxDestination.delete(0, END)
    EntryBoxDestination.insert(END, (filedialog.askdirectory()))
def browse_button3():
    EntryBoxSource_substring.delete(0, END)
    EntryBoxSource_substring.insert(END, (filedialog.askdirectory()))
def browse_button4():
    EntryBoxDestination_substring.delete(0, END)
    EntryBoxDestination_substring.insert(END, (filedialog.askdirectory()))
def browse_button5():
    EntryBoxMoveSource_date.delete(0, END)
    EntryBoxMoveSource_date.insert(END, (filedialog.askdirectory()))
def browse_button6():
    EntryBoxMoveSource.delete(0, END)
    EntryBoxMoveSource.insert(END, (filedialog.askdirectory()))

#checks for duplicate files. If true, creates a new name for the file and copies it.
def file_exist_and_rename_check(dst, file_path): 
    if not os.path.exists(os.path.join(dst, (os.path.basename(file_path)))):
        shutil.copy2(file_path, dst)
    else:
        base, extension = os.path.splitext(os.path.basename(file_path))
        i = 1
        while os.path.exists(os.path.join(dst, '{}_{}{}'.format(base, i, extension))):
            i += 1
        shutil.copy2(file_path, os.path.join(dst, '{}_{}{}'.format(base, i, extension)))

#copies all files with a specificed extension from a directory including subfolders.
def copy_all_files(src, dst, req_ext): 
    for folder, sub_folder, files in os.walk(src):
        for name in files:
            file_path = (os.path.join(folder, name))
            file_main, file_extension = os.path.splitext(file_path)
            if file_extension in req_ext:
                file_exist_and_rename_check(dst, file_path)

#copies all files with a specificed extension within a directory excluding subfolders.
def copy_no_subfolder(src, dst, req_ext):
    for file in os.listdir(src):
        if os.path.isfile(os.path.join(src, file)):
            file_path = os.path.join(src, file)
            file_main, file_extension = os.path.splitext(file_path)
            if file_extension in req_ext:
                file_exist_and_rename_check(dst, file_path)

#moves files into new folders named according to the first n characters in the file name.
def move_dated_files(src, n):
    for file in os.listdir(src):
        if os.path.isfile(os.path.join(src, file)):
            folder = os.path.join(src, file[:n])
            try:
                os.mkdir(folder)
            except FileExistsError:
                pass
            if file[:n] == os.path.basename(folder):
                if not os.path.exists(os.path.join(folder, (os.path.basename(file)))):
                    shutil.move(os.path.join(src, file), folder)
                else:
                    base, extension = os.path.splitext(os.path.basename(os.path.join(src, file)))
                    i = 1
                    while os.path.exists(os.path.join(folder, '{}_{}{}'.format(base, i, extension))):
                        i += 1
                    shutil.move(os.path.join(src, file), os.path.join(folder, '{}_{}{}'.format(base, i, extension)))          

#gets the date modified time of a file.
def get_mtime(src, file):
    return datetime.fromtimestamp(os.path.getmtime(os.path.join(src, file))).strftime('%Y-%m-%d')

#moves files into new folders named according to the file's date modified 
def mod_date_files(src):
    for file in os.listdir(src):
        if os.path.isfile(os.path.join(src, file)):
            try:
                os.mkdir(os.path.join(src, get_mtime(src, file)))
            except FileExistsError:
                pass
            folder = os.path.join(src, get_mtime(src, file))
            if get_mtime(src, file) == os.path.basename(folder):
                if not os.path.exists(os.path.join(folder, (os.path.basename(file)))):
                    shutil.move(os.path.join(src, file), (os.path.join(src, get_mtime(src, file))))
                else:
                    base, extension = os.path.splitext(os.path.basename(os.path.join(src, file)))
                    i = 1
                    while os.path.exists(os.path.join(folder, '{}_{}{}'.format(base, i, extension))):
                        i += 1
                    shutil.move(os.path.join(src, file), os.path.join(folder, '{}_{}{}'.format(base, i, extension)))    

#searches directory including subfolders for files with specificed substring in the file name and copies them
def file_search(src, dst, substring):
    for folder, sub_folders, files in os.walk(src):
        for name in files:
            if substring in name:
                file_path = (os.path.join(folder, name))
                file_exist_and_rename_check(dst, file_path)

#searches a folder for files with specificed substring in the file name and copies them
def file_search_folder(src, dst, substring):
    for file in os.listdir(src):
        if os.path.isfile(os.path.join(src, file)):
            if substring in file:
                file_path = os.path.join(src, (os.path.basename(file)))
                file_exist_and_rename_check(dst, file_path)

#copies folders containing a substring in folder name.
def folder_copy(src, dst, substring):
    for folder, sub_folders, files in os.walk(src):
        for name in sub_folders:
            if substring in name:
                folder = os.path.join(src, name)
                if not os.path.exists(os.path.join(dst, name)):
                    shutil.copytree(folder, os.path.join(dst, name))

def run_copy_all():
    req_ext = ''
    req_ext += str(EntryBoxExtension.get())
    src = r'{}'.format(str(EntryBoxSource.get()))
    dst = r'{}'.format(str(EntryBoxDestination.get()))
    copy_all_files(src, dst, req_ext)

def run_copy_no_subfolder():
    req_ext = ''
    req_ext += str(EntryBoxExtension.get())
    src = r'{}'.format(str(EntryBoxSource.get()))
    dst = r'{}'.format(str(EntryBoxDestination.get()))
    copy_no_subfolder(src, dst, req_ext)

def run_move_n():
    src = r'{}'.format(str(EntryBoxMoveSource.get()))
    n = abs(int(EntryBoxFileLength.get()))
    move_dated_files(src, n)   

def run_move_date():
    src = r'{}'.format(str(EntryBoxMoveSource_date.get()))
    mod_date_files(src)

def run_file_search():
    substring = ''
    substring += str(EntryBox_substring.get())
    src = r'{}'.format(str(EntryBoxSource_substring.get()))
    dst = r'{}'.format(str(EntryBoxDestination_substring.get()))
    file_search(src, dst, substring)

def run_file_search_folder():
    substring = ''
    substring += str(EntryBox_substring.get())
    src = r'{}'.format(str(EntryBoxSource_substring.get()))
    dst = r'{}'.format(str(EntryBoxDestination_substring.get()))
    file_search_folder(src, dst, substring)

def run_folder_copy():
    substring = ''
    substring += str(EntryBox_substring.get())
    src = r'{}'.format(str(EntryBoxSource_substring.get()))
    dst = r'{}'.format(str(EntryBoxDestination_substring.get()))
    folder_copy(src, dst, substring)

def checkbox_copy_all():
    if var1.get() == 1:
         run_copy_all()
    if var1.get() == 0:
        run_copy_no_subfolder()

def checkbox_file_search():
     if var2.get() == 1:
         run_file_search()
     if var2.get() == 0:
         run_file_search_folder()

copy_button = Button(frame1, text = "Copy Files", command=checkbox_copy_all).grid(row = 6, column = 0, padx = 10, pady = 10)
file_search_button= Button(frame2,text = "Copy Files",command=checkbox_file_search).grid(row = 6, column = 0, padx = 10, pady = 10)
folder_search_button= Button(frame2,text = "Copy Folder", command=run_folder_copy).grid(row = 7, column = 0, padx = 10, pady = 10)
move_button_date = Button(frame3, text = "Move Files", command=run_move_date).grid(row = 2, column=0, padx = 10, pady = 10)
move_button_n = Button(frame4, text = "Move Files", command=run_move_n).grid(row = 4, column=0, padx = 10, pady = 10)
browse_button_1 = Button(frame1, text = '...', command=browse_button1).grid(row = 1, column = 1, padx = 10, pady = 10)
browse_button_2 = Button(frame1, text = '...', command=browse_button2).grid(row = 3, column = 1, padx = 10, pady = 10)
browse_button_3 = Button(frame2, text = '...', command=browse_button3).grid(row = 1, column = 1, padx = 10, pady = 10)
browse_button_4 = Button(frame2, text = '...', command=browse_button4).grid(row = 3, column = 1, padx = 10, pady = 10)
browse_button_5 = Button(frame3, text = '...', command=browse_button5).grid(row = 1, column = 1, padx = 10, pady = 10)
browse_button_6 = Button(frame4, text = '...', command=browse_button6).grid(row = 1, column = 1, padx = 10, pady = 10)

root.mainloop()