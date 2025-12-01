#imported modules
import tkinter as tk
from tkinter import messagebox
from tkinter import Frame, BOTTOM, TOP, LEFT, RIGHT
import pandas as pd
from tkinter import ttk

#主要的視窗
window = tk.Tk()
window.title("酒吧管理系统")

#read data from CSV
file_path= "程式設計期末專題-酒譜 - 工作表1.csv"
df_1 = pd.read_csv(file_path)

#options
type = df_1["Type"].drop_duplicates().tolist()
sweetness = df_1["sweetness"].drop_duplicates().tolist()
sourness = df_1["sourness"].drop_duplicates().tolist()
alcohol_feeling = df_1["alcohol_feeling"].drop_duplicates().tolist()
flavors = df_1["flavor_tags"].drop_duplicates().tolist() #not sure yet if this is the best method
mouthfeel = df_1["mouthfeel"].drop_duplicates().tolist()
ingredients = df_1["ingredients"].drop_duplicates().tolist()
time = df_1["time"].drop_duplicates().tolist()
glassware = df_1["glassware"].drop_duplicates().tolist()

selected_options = {} #提出結果以後，需要刪除所有選項

#functions
def exit_app():
    window.destroy()
    messagebox.showinfo("退出", "已退出酒吧管理系统")

# 框架設置：頂部標題、內容（左右兩欄）、底部按鈕
topFrame = Frame(window)
topFrame.pack(side=TOP, fill='x')

contentFrame = Frame(window)
contentFrame.pack(fill='both', expand=True)

leftFrame = Frame(contentFrame)
leftFrame.pack(side=LEFT, fill='both', expand=True, padx=10, pady=10)

rightFrame = Frame(contentFrame)
rightFrame.pack(side=LEFT, fill='both', expand=True, padx=10, pady=10)

bottomFrame = Frame(window)
bottomFrame.pack(side=BOTTOM, fill='x')

# 自動讓視窗最大化
window.geometry("{0}x{1}+0+0".format(window.winfo_screenwidth() -100, window.winfo_screenheight() -100))

# 標題放在頂部
title_label = tk.Label(topFrame, text="酒吧管理系统", font=(None, 18))
title_label.pack(pady=12)

# 右側顯示區（例如：材料清單與時間管理占位）
materials_label = tk.Label(rightFrame, text="材料清單")
materials_label.pack(anchor='n', pady=10)

time_label = tk.Label(rightFrame, text="時間管理")
time_label.pack(anchor='n', pady=10)

# options 按鈕 - 使用正確的 IntVar / StringVar 變量
# mouthfeel checkbuttons
mouthfeel_vars = {}
mouthfeel_label = tk.Label(leftFrame, text="Mouthfeel Options:")
mouthfeel_label.pack(anchor='w', pady=(0,6))
for option in mouthfeel:
    var = tk.IntVar()
    mouthfeel_vars[option] = var
    cb = tk.Checkbutton(leftFrame, text=option, variable=var)
    cb.pack(anchor='w')

# radio button groups
sweetness_var = tk.StringVar()
sweetness_label = tk.Label(leftFrame, text="Sweetness Options:")
sweetness_label.pack(anchor='w', pady=(8,6))
for option in sweetness:
    rb = tk.Radiobutton(leftFrame, text=option, variable=sweetness_var, value=option)
    rb.pack(anchor='w')

sourness_var = tk.StringVar()
sourness_label = tk.Label(leftFrame, text="Sourness Options:")
sourness_label.pack(anchor='w', pady=(8,6))
for option in sourness:
    rb = tk.Radiobutton(leftFrame, text=option, variable=sourness_var, value=option)
    rb.pack(anchor='w')

alcohol_var = tk.StringVar()
alcohol_label = tk.Label(leftFrame, text="Alcohol Feeling Options:")
alcohol_label.pack(anchor='w', pady=(8,6))
for option in alcohol_feeling:
    rb = tk.Radiobutton(leftFrame, text=option, variable=alcohol_var, value=option)
    rb.pack(anchor='w')

# Comboboxes
type_label = tk.Label(leftFrame, text="Type Options:")
type_label.pack(anchor='w', pady=(8,6))
type_var = tk.StringVar()
type_combobox = ttk.Combobox(leftFrame, textvariable=type_var, values=type)
type_combobox.pack(anchor='w', pady=4)

#積累用戶選擇的選項
def accumulate_choices():
    #檢查是否所有選項均已選擇
    if not sweetness_var.get() or not sourness_var.get() or not alcohol_var.get() or not type_var.get() or all(var.get() == 0 for var in mouthfeel_vars.values()):
        messagebox.showwarning("警告", "請確保所有選項均已選擇")
        return
    else:
        selected_options['mouthfeel'] = [option for option, var in mouthfeel_vars.items() if var.get() == 1]
        selected_options['sweetness'] = sweetness_var.get()
        selected_options['sourness'] = sourness_var.get()
        selected_options['alcohol_feeling'] = alcohol_var.get()
        selected_options['type'] = type_var.get()
        messagebox.showinfo("選擇已儲存", f"已儲存的選擇: {selected_options}")

#確認按鈕
button = tk.Button(bottomFrame, text="確認", command=accumulate_choices) 
button.pack(pady=10)

#離開按鈕
exit_button = tk.Button(bottomFrame, text="離開", command=exit_app)
exit_button.pack(pady=10) 

#如果我們有時間，可以讓用戶儲存他們最喜歡的飲料配方

window.mainloop()