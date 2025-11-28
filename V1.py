#imported modules
import tkinter as tk

#主要的視窗
window = tk.Tk()
window.title("酒吧管理系统")

#自動讓視窗最大化
window.geometry("{0}x{1}+0+0".format(window.winfo_screenwidth(), window.winfo_screenheight()))
label = tk.Label(window, text="酒吧管理系统")
label.pack(pady=20)

#如果我們有時間，可以讓用戶儲存他們最喜歡的飲料配方

window.mainloop()