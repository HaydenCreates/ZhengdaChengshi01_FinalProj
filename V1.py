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

#積累用戶選擇的選項
def accumulate_choices():
    # 檢查是否所有選項均已選擇
    if not sweetness_var.get() or not sourness_var.get() or not alcohol_var.get() or not type_var.get() or not any(var.get() for var in mouthfeel_vars.values()):
        messagebox.showwarning("警告", "請確保所有選項均已選擇")
        return

    # 儲存使用者選擇
    #selected_options['mouthfeel'] = [option for option, var in mouthfeel_vars.items() if var.get() == 1]
    #selected_options['sweetness'] = sweetness_var.get()
    #selected_options['sourness'] = sourness_var.get()
    #selected_options['alcohol_feeling'] = alcohol_var.get()
    #selected_options['type'] = type_var.get()

    selections = {
        'type': type_var.get(),
        'sweetness': sweetness_var.get(),
        'sourness': sourness_var.get(),
        'alcohol_feeling': alcohol_var.get(),
        'mouthfeel': [k for k, v in mouthfeel_vars.items() if v.get() == 1],
    }
    
    #call find best matches function
    matches = find_best_matches(df_1, selections, top_n=5)
    if matches:
        best = matches[0]
        open_secondary_window(best)
    else:
         messagebox.showinfo("推薦結果", "找不到符合條件的調酒，請重新選擇條件。")

    '''
    # === 真正從 CSV 篩選推薦調酒 ===
    filtered_df = df_1.copy()
    print(filtered_df)

    filtered_df = filtered_df[filtered_df["sweetness"] == selected_options["sweetness"]]
    filtered_df = filtered_df[filtered_df["sourness"] == selected_options["sourness"]]
    filtered_df = filtered_df[filtered_df["alcohol_feeling"] == selected_options["alcohol_feeling"]]
    filtered_df = filtered_df[filtered_df['Type'] == selected_options['type']]

    # mouthfeel 是多選 → 用 isin 篩選
    filtered_df = filtered_df[filtered_df["mouthfeel"].isin(selected_options["mouthfeel"])]

    # === 顯示推薦結果 ===
    if filtered_df.empty:
        messagebox.showinfo("推薦結果", "找不到符合條件的調酒，請重新選擇條件。")
        return
    recommendation_text = ""
    for idx, row in filtered_df.head(5).iterrows():
        recommendation_text += f" {row['drink_name']}｜杯型：{row['glassware']}\n"

    messagebox.showinfo("推薦結果", recommendation_text)
    '''

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

    final_steps = str(result_text['row']['steps']).split("\\n")
    print(final_steps)
    for i in range(len(final_steps)):
        step_label = tk.Label(secondary_window, text=f"Step {i+1}: {final_steps[i]}")
        step_label.place(x=50, y=100 + i*30)

    mouthfeel = tk.Label(secondary_window, text="Mouthfeel: " + str(result_text['row']['mouthfeel']))
    mouthfeel.place(x=50, y=140)

    flavor_tags = tk.Label(secondary_window, text="Flavor Tags: " + str(result_text['row']['flavor_tags']))
    flavor_tags.place(x=50, y=180)

    alcohol_feeling = tk.Label(secondary_window, text="Alcohol Feeling: " + str(result_text['row']['alcohol_feeling']))
    alcohol_feeling.place(x=50, y=220)

    time_label = tk.Label(secondary_window, text="Time: " + str(result_text['row']['time']))
    time_label.place(x=50, y=260)

    type_label = tk.Label(secondary_window, text="Type: " + str(result_text['row']['Type']))
    type_label.place(x=50, y=300)

    glassware_label = tk.Label(secondary_window, text="Glassware: " + str(result_text['row']['glassware']))
    glassware_label.place(x=50, y=340)

    abv_label = tk.Label(secondary_window, text="ABV: " + str(result_text['row']['abv']))
    abv_label.place(x=50, y=380)

    sourness_label = tk.Label(secondary_window, text="Sourness: " + str(result_text['row']['sourness']))
    sourness_label.place(x=50, y=420)

    sweetness_label = tk.Label(secondary_window, text="Sweetness: " + str(result_text['row']['sweetness']))
    sweetness_label.place(x=50, y=460)

    #離開按鈕
    button_close = ttk.Button(
        secondary_window,
        text="Close window",
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