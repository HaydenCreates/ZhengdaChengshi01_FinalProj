#imported modules
import tkinter as tk
from tkinter import messagebox
from tkinter import Frame, BOTTOM, TOP, LEFT, RIGHT

#主要的視窗
window = tk.Tk()
window.title("酒吧管理系统")

#functions
def exit_app():
    window.destroy()
    messagebox.showinfo("退出", "已退出酒吧管理系统")

#框架設置
topFrame = Frame(window)
topFrame.pack(side=TOP)
bottomFrame = Frame(window)
bottomFrame.pack(side=BOTTOM)
leftFrame = Frame(window)
leftFrame.pack(side=LEFT)
rightFrame = Frame(window)
rightFrame.pack(side=RIGHT)

#自動讓視窗最大化
window.geometry("{0}x{1}+0+0".format(window.winfo_screenwidth() -100, window.winfo_screenheight() -100))
label = tk.Label(window, text="酒吧管理系统")
label.pack(pady=20)

label = tk.Label(leftFrame, text="材料清單")
label.pack(pady=20)

label = tk.Label(rightFrame, text="時間管理")
label.pack(pady=20)

#確認按鈕
button = tk.Button(bottomFrame, text="確認") #加入functionality
button.pack(pady=10)

#離開按鈕
exit_button = tk.Button(bottomFrame, text="離開", command=exit_app)
exit_button.pack(pady=10) 

#如果我們有時間，可以讓用戶儲存他們最喜歡的飲料配方

window.mainloop()