#imported modules
import tkinter as tk
from tkinter import messagebox
from tkinter import Frame, BOTTOM, TOP, LEFT, RIGHT
import pandas as pd
from tkinter import ttk
import os
import shutil

#主要的視窗
window = tk.Tk()
window.title("酒吧管理系统")

#read data from CSV
file_path= "程式設計期末專題-酒譜 - 工作表1.csv"
df_1 = pd.read_csv(file_path)

#options
type = df_1["Type"].drop_duplicates().tolist()
sweetness = df_1["sweetness"].drop_duplicates().tolist()
sweetness.sort()
sourness = df_1["sourness"].drop_duplicates().tolist()
sourness.sort()
alcohol_feeling = df_1["alcohol_feeling"].drop_duplicates().tolist()
alcohol_feeling.sort()
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
# 三個主畫面
frame_filter = Frame(window)
frame_list = Frame(window)
frame_detail = Frame(window)

frame_filter.pack(fill="both", expand=True)

topFrame = Frame(frame_filter)
topFrame.pack(side=TOP, fill='x')

contentFrame = Frame(frame_filter)
contentFrame.pack(fill='both', expand=True)

leftFrame = Frame(contentFrame)
leftFrame.pack(side=LEFT, fill='both', expand=True, padx=10, pady=10)

rightFrame = Frame(contentFrame)
rightFrame.pack(side=LEFT, fill='both', expand=True, padx=10, pady=10)

bottomFrame = Frame(frame_filter)
bottomFrame.pack(side=BOTTOM, fill='x')

# 顯示最喜歡的（前5個）
fav_path = os.path.join(os.path.dirname(__file__), '最喜歡的.csv')  

favorites_frame = tk.Frame(rightFrame)
favorites_frame.pack(anchor='n', pady=6)

fav_title = tk.Label(favorites_frame, text="我的最愛 (前5)", font=(None, 11, 'bold'))
fav_title.pack(anchor='w')

fav_listbox = tk.Listbox(favorites_frame, width=40, height=5)
fav_listbox.pack(anchor='w', pady=(4,0))

def load_favorites(path=fav_path, limit=5):
    fav_listbox.delete(0, 'end')
    if not os.path.exists(path):
        fav_listbox.insert('end', "(最愛清單為空)")
        return
    try:
        df = pd.read_csv(path, encoding='utf-8-sig')
        if df.empty:
            fav_listbox.insert('end', "(最愛清單為空)")
            return
        for i, (_, row) in enumerate(df.head(limit).iterrows()):
            name = None
            if 'drink_name' in df.columns:
                name = row.get('drink_name')
            if not name and 'Type' in df.columns:
                name = row.get('Type')
            if not name:
                name = str(row.to_dict())
            fav_listbox.insert('end', f"{i+1}. {name}")
    except Exception as e:
        fav_listbox.insert('end', f"(讀取最愛失敗: {e})")

load_favorites()

# 雙擊最愛列表項以打開詳細視窗
def on_fav_double_click(event):
    sel = fav_listbox.curselection()
    if not sel:
        return
    idx = sel[0]
    df = pd.read_csv(fav_path, encoding='utf-8-sig')
    if idx < len(df):
        row = df.iloc[idx].to_dict()
        open_secondary_window({'score': 1.0, 'row': row})

fav_listbox.bind('<Double-1>', on_fav_double_click)

# 刪除選定的最愛項目
def remove_selected_favorite(path=fav_path):
    sel = fav_listbox.curselection()
    if not sel:
        messagebox.showwarning("提示", "請先選擇要移除的最愛項目。")
        return
    idx = sel[0]

    if not os.path.exists(path):
        messagebox.showinfo("提示", "最愛清單不存在。")
        return

    try:
        df = pd.read_csv(path, encoding='utf-8-sig')
    except Exception as e:
        messagebox.showerror("錯誤", f"讀取最愛失敗: {e}")
        return

    if idx >= len(df):
        messagebox.showerror("錯誤", "選擇的索引超出範圍。")
        load_favorites()  
        return

    name = df.iloc[idx].get('drink_name') if 'drink_name' in df.columns else None
    display_name = name or df.iloc[idx].get('Type') or f"項目 {idx+1}"

    if not messagebox.askyesno("確認刪除", f"確定要將「{display_name}」從最愛移除嗎？"):
        return
    
    df = df.drop(df.index[idx]).reset_index(drop=True)
    try:
        df.to_csv(fav_path, index=False, encoding='utf-8-sig')
    except Exception as e:
        messagebox.showerror("錯誤", f"寫入最愛失敗: {e}")
        return

    load_favorites()
    messagebox.showinfo("已移除", f"已將「{display_name}」從最愛移除。")

remove_btn = ttk.Button(favorites_frame, text="刪除凸顯的", command=remove_selected_favorite)
remove_btn.pack(anchor='w', pady=(6,0))

# 自動讓視窗最大化
window.geometry("{0}x{1}+0+0".format(window.winfo_screenwidth() -100, window.winfo_screenheight() -100))

# 標題放在頂部
title_label = tk.Label(topFrame, text="酒吧管理系统", font=(None, 18))
title_label.pack(pady=12)

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

# Utility helpers
def normalize_text(s):
    if pd.isna(s) or s is None:
        return ""
    return str(s).lower().strip()

# 從多值字符串計算相似度 i.e. "sweet, sour" vs "sour, bitter" - 多選項的列
def jaccard_from_strings(a, b):
    # a, b: comma-separated strings or lists; returns 0..1
    if a is None:
        a = ""
    if b is None:
        b = ""
    if isinstance(a, str):
        A = {x.strip() for x in a.lower().split(",") if x.strip()}
    else:
        A = {x.strip().lower() for x in a}
    if isinstance(b, str):
        B = {x.strip() for x in b.lower().split(",") if x.strip()}
    else:
        B = {x.strip().lower() for x in b}
    if not A and not B:
        return 0.0
    inter = A & B
    union = A | B
    return len(inter) / len(union) if union else 0.0

#每個列的計算分數
def score_row(row, selections, weights=None, numeric_max=None):
    if weights is None:
        weights = {
            'type': 1.0,
            'sweetness': 1.0,
            'sourness': 1.0,
            'alcohol_feeling': 1.0,
            'mouthfeel': 1.5,
        }
    score = 0.0
    max_score = 0.0

    # 具體值匹配（單值欄位） — 不把多選欄位 (mouthfeel 等) 放在這裡
    for col in ('Type', 'sweetness', 'sourness', 'alcohol_feeling'):
        key = col.lower()  # 每個列都轉成小寫以匹配 selections 的鍵
        w = weights.get(key, 1.0)
        max_score += w
        sel_val = selections.get(key)
        if sel_val:
            if normalize_text(row.get(col, "")) == normalize_text(sel_val):
                score += w

    # 如果一個列有多值匹配（jaccard)
    for col in (('mouthfeel', 'mouthfeel'), ('flavor_tags', 'flavor_tags'), ('ingredients', 'ingredients')):
        col_name, sel_key = (col if isinstance(col, tuple) else (col, col))
        w = weights.get(sel_key, 1.0)
        max_score += w
        sel_list = selections.get(sel_key)

        # 將 selection 轉成可比較的字串：若為 list/tuple，將其 join 成逗號分隔字串；否則使用原始值或空字串
        if isinstance(sel_list, (list, tuple)):
            sel_for_compare = ",".join([str(x) for x in sel_list])
            # 如果只有一個選項，且該選項出現在資料列的標籤集中，視為完整匹配 (sim = 1.0)
            if len(sel_list) == 1:
                single_token = normalize_text(sel_list[0])
                row_tokens = {x.strip() for x in normalize_text(row.get(col_name, "")).split(",") if x.strip()}
                if single_token and single_token in row_tokens:
                    sim = 1.0
                else:
                    sim = jaccard_from_strings(row.get(col_name, ""), sel_for_compare)
            else:
                sim = jaccard_from_strings(row.get(col_name, ""), sel_for_compare)
        else:
            sel_for_compare = sel_list or ""
            sim = jaccard_from_strings(row.get(col_name, ""), sel_for_compare)
        score += sim * w

    #如果是數字列 (time)
    if 'time' in row and selections.get('time') is not None:
        try:
            row_time = float(row['time'])
            sel_time = float(selections['time'])

            numeric_max = max(row_time, sel_time, 1.0)
            diff = abs(row_time - sel_time) / numeric_max
            numeric_sim = max(0.0, 1.0 - diff)  # 1.0 if exact, drops toward 0
            w = weights.get('time', 1.0)
            max_score += w
            score += numeric_sim * w
        except Exception:
            pass

    # Normalize to 0..1
    normalized = (score / max_score) if max_score > 0 else 0.0
    return normalized

def find_best_matches(df, selections, top_n=3):
    scored = []
    #idx是index,row是每一列的資料
    for idx, row in df.iterrows():
        s = score_row(row, selections)
        scored.append((idx, s))

    # 根據分數排序
    scored.sort(key=lambda x: x[1], reverse=True)
    results = []
    for idx, s in scored[:top_n]:
        row = df.loc[idx].to_dict()
        results.append({'score': s, 'row': row})
    return results

# 畫面 2：結果清單
def show_results_list(matches):
    if not matches:
        messagebox.showinfo("推薦結果", "沒有推薦結果可顯示。")
        return
        
    frame_filter.pack_forget()
    frame_detail.pack_forget()
    frame_list.pack(fill="both", expand=True)

    for w in frame_list.winfo_children():
        w.destroy()

    tk.Label(frame_list, text="符合條件的調酒", font=(None, 20)).pack(pady=15)
    for drink in matches:
        row = Frame(frame_list)
        row.pack(pady=5)

        tk.Label(row, text=drink["row"]["drink_name"], width=25).pack(side=LEFT)
        tk.Button(
            row,
            text="選擇",
            command=lambda d=drink: open_secondary_window(d)
        ).pack(side=LEFT)
            # --- 在清單頁底部加入返回上一頁 ---
    tk.Button(
    frame_list,
    text="返回清單",
    command=back_to_filter
    ).pack(pady=20)

# 導航控制
def back_to_filter():
    frame_list.pack_forget()
    frame_filter.pack(fill="both", expand=True)

#積累用戶選擇的選項
def accumulate_choices():
    # 檢查是否所有選項均已選擇
    if not sweetness_var.get() or not sourness_var.get() or not alcohol_var.get() or not type_var.get() or not any(var.get() for var in mouthfeel_vars.values()):
        messagebox.showwarning("警告", "請確保所有選項均已選擇")
        return

    selections = {
        'type': type_var.get(),
        'sweetness': sweetness_var.get(),
        'sourness': sourness_var.get(),
        'alcohol_feeling': alcohol_var.get(),
        'mouthfeel': [k for k, v in mouthfeel_vars.items() if v.get() == 1],
    }
    # call find best matches function
    matches = find_best_matches(df_1, selections, top_n=5)
    if matches:
        # show list so user can pick one
        show_results_list(matches)
    else:
        messagebox.showinfo("推薦結果", "找不到符合條件的調酒，請重新選擇條件。")

#保存到最愛功能 (placeholder)
def save_to_favorites(row, fav_path='最喜歡的.csv', unique_key='drink_name'):    
    try:
        # Dataframe 一個咧
        df_row = pd.DataFrame([row])

        #如果已經存在
        if os.path.exists(fav_path):
            df_exist = pd.read_csv(fav_path, encoding='utf-8-sig')
            # 檢查重複
            if unique_key and unique_key in df_exist.columns and unique_key in df_row.columns:
                val = df_row.iloc[0].get(unique_key)
                if val in df_exist[unique_key].astype(str).values:
                    messagebox.showinfo("已存在", f"「{val}」已在最愛清單中。")
                    return
            df_row.to_csv(fav_path, mode='a', header=False, index=False, encoding='utf-8-sig')
        else:
            df_row.to_csv(fav_path, index=False, encoding='utf-8-sig')

            messagebox.showinfo("已儲存", "已將此飲料加入最愛。")
        
        load_favorites()  # 重新載入最愛清單
    except Exception as e:
        messagebox.showerror("錯誤", f"儲存失敗：{e}")

#結果的視窗
def open_secondary_window(result_text):
    # Create secondary (or popup) window.
    secondary_window = tk.Toplevel()
    secondary_window.title("Secondary Window")
    secondary_window.config(width=600, height=600)
    
    #顯示結果
    drink_name = tk.Label(secondary_window, text=result_text['row']['drink_name'], font=(None, 16))
    drink_name.place(x=50, y=20)

    ingredients = tk.Label(secondary_window, text="Ingredients: " + str(result_text['row']['ingredients']))
    ingredients.place(x=50, y=50)

    final_steps = str(result_text['row']['steps']).split("\\n")
    for i in range(len(final_steps)):
        step_label = tk.Label(secondary_window, text=f"Step {i+1}: {final_steps[i]}")
        step_label.place(x=325, y=50 + i*40)

    mouthfeel = tk.Label(secondary_window, text="Mouthfeel: " + str(result_text['row']['mouthfeel']))
    mouthfeel.place(x=50, y=80)

    flavor_tags = tk.Label(secondary_window, text="Flavor Tags: " + str(result_text['row']['flavor_tags']))
    flavor_tags.place(x=50, y=120)

    alcohol_feeling = tk.Label(secondary_window, text="Alcohol Feeling: " + str(result_text['row']['alcohol_feeling']))
    alcohol_feeling.place(x=50, y= 160)

    time_label = tk.Label(secondary_window, text="Time: " + str(result_text['row']['time']))
    time_label.place(x=50, y=200)

    type_label = tk.Label(secondary_window, text="Type: " + str(result_text['row']['Type']))
    type_label.place(x=50, y=240)

    glassware_label = tk.Label(secondary_window, text="Glassware: " + str(result_text['row']['glassware']))
    glassware_label.place(x=50, y=280)

    abv_label = tk.Label(secondary_window, text="ABV: " + str(result_text['row']['abv']))
    abv_label.place(x=50, y=320)

    sourness_label = tk.Label(secondary_window, text="Sourness: " + str(result_text['row']['sourness']))
    sourness_label.place(x=50, y= 360)
    
    sweetness_label = tk.Label(secondary_window, text="Sweetness: " + str(result_text['row']['sweetness']))
    sweetness_label.place(x=50, y=400)

    notice_label = tk.Label(secondary_window, text="通知: 您尋找的飲料是最相似性的, 不一定會直接配偶您點按的選項", fg="red")
    notice_label.place(x=200, y=500)

    #保存到最愛按鈕 
    button_save = ttk.Button(
        secondary_window,
        text="保存到最愛",
        command=lambda: save_to_favorites(result_text['row'], fav_path='最喜歡的.csv')
    )
    button_save.place(x=200, y=450)

    #離開按鈕
    button_close = ttk.Button(
        secondary_window,
        text="關閉視窗",
        command=secondary_window.destroy
    )
    button_close.place(x=50, y=500)

#確認按鈕
button = tk.Button(bottomFrame, text="確認", command=accumulate_choices) 
button.pack(pady=10)

#離開按鈕
exit_button = tk.Button(bottomFrame, text="離開", command=exit_app)
exit_button.pack(pady=10) 

#如果我們有時間，可以讓用戶儲存他們最喜歡的飲料配方

window.mainloop()