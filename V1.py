#imported modules
import tkinter as tk
from PIL import Image
from tkinter import messagebox
from tkinter import BOTTOM, TOP, LEFT, RIGHT
import pandas as pd
from tkinter import ttk
import tkinter.font as tkfont
import os
import customtkinter as ctk

ctk.set_appearance_mode("dark") 
ctk.set_default_color_theme("dark-blue") 

#主要的視窗
window = ctk.CTk()
window.title("酒吧管理系统")

try:
    icon_image = tk.PhotoImage(file="icon.png")
    window.iconphoto(False, icon_image)
except Exception:
    pass

bg_image = ctk.CTkImage(
    light_image=Image.open("bar_bg.png"),
    dark_image=Image.open("bar_bg.png"),
    size=(800, 600)
)

# 增加字體大小以提升可讀性
base_font_size = 12
try:
    default_font = tkfont.nametofont("TkDefaultFont")
    default_font.configure(size=base_font_size)
except Exception:
    pass
try:
    text_font = tkfont.nametofont("TkTextFont")
    text_font.configure(size=base_font_size)
except Exception:
    pass

#讀CSV檔案
file_path= "程式設計期末專題-酒譜 - 工作表1.csv"
df_1 = pd.read_csv(file_path)

priority_map = {'重': 3, '中': 2, '低': 1}
selected_options = {}

#函式
def exit_app():
    window.destroy()
    messagebox.showinfo("退出", "已退出酒吧管理系统")

# 框架設置：頂部標題、內容（左右兩欄）、底部按鈕
# 三個主畫面
bg_label = ctk.CTkLabel(window, image=bg_image, text="")
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

frame_filter = ctk.CTkFrame(window, corner_radius=15)
frame_list   = ctk.CTkFrame(window, corner_radius=15)
frame_detail = ctk.CTkFrame(window,corner_radius=15)
frame_admin  = ctk.CTkFrame(window, corner_radius=15)

frame_filter.pack(fill="both", expand=True,padx=10, pady=10)

topFrame = ctk.CTkFrame(frame_filter)
topFrame.pack(side="top", fill='x', pady=(0, 5))

contentFrame = ctk.CTkFrame(frame_filter)
contentFrame.pack(fill='both', expand=True, padx=5, pady=5)

leftFrame = ctk.CTkFrame(contentFrame)
leftFrame.pack(side="left", fill='both', expand=True, padx=10, pady=10)

rightFrame = ctk.CTkFrame(contentFrame)
rightFrame.pack(side="left", fill='both', expand=True, padx=10, pady=10)

bottomFrame = ctk.CTkFrame(frame_filter)
bottomFrame.pack(side="bottom", fill='x', pady=(5, 0))

# 顯示最喜歡的（前5個）
fav_path = os.path.join(os.path.dirname(__file__), '最喜歡的.csv')  

favorites_frame = ctk.CTkFrame(rightFrame, corner_radius=8)
favorites_frame.pack(anchor='w', pady=6, padx=6, fill="x")

fav_title = ctk.CTkLabel(favorites_frame, text="我的最愛 (前5)", text_color="white",  font=(None, 14, 'bold'))
fav_title.pack(anchor='w', padx=8, pady=(8, 6))

fav_list_frame = ctk.CTkFrame(favorites_frame, corner_radius=4)
fav_list_frame.pack(side="left", fill="both", expand=True, padx=8, pady=(0,8))
fav_listbox = tk.Listbox(fav_list_frame, width=38, height=5, font=("Arial", 10), relief="flat", highlightthickness=0)
fav_listbox.pack(side="left", fill="both", expand=True)
fav_scrollbar = ttk.Scrollbar(fav_list_frame, command=fav_listbox.yview)
fav_scrollbar.pack(side="right", fill="y")
fav_listbox.config(yscrollcommand=fav_scrollbar.set)

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

remove_btn = ctk.CTkButton(favorites_frame, text="刪除凸顯的", command=remove_selected_favorite, width=120)
remove_btn.pack(anchor='w', padx=6, pady=(6,6))

# 自動讓視窗最大化
window.geometry("{0}x{1}+0+0".format(window.winfo_screenwidth() -100, window.winfo_screenheight() -100))

def build_filter_ui():
    global mouthfeel_vars, sweetness_var, sourness_var, alcohol_var, type_var, type_combobox
    try:
        types = df_1['Type'].drop_duplicates().tolist()
    except Exception:
        types = []
    try:
        sweets = df_1['sweetness'].drop_duplicates().tolist()
        sweets = sorted(sweets, key=lambda x: priority_map.get(x, 0))
    except Exception:
        sweets = []
    try:
        sourness = df_1['sourness'].drop_duplicates().tolist()
        sours = sorted(sourness, key=lambda x: priority_map.get(x, 0))
    except Exception:
        sours = []
    try:
        alcohols = df_1['alcohol_feeling'].drop_duplicates().tolist()
        alcohols = sorted(alcohols, key=lambda x: priority_map.get(x, 0))
    except Exception:
        alcohols = []
    try:
        mouthfeels = df_1['mouthfeel'].drop_duplicates().tolist()
    except Exception:
        mouthfeels = []

    # clear leftFrame
    for w in leftFrame.winfo_children():
        w.destroy()

    # mouthfeel
    mouthfeel_vars = {}
    mouthfeel_frame = ctk.CTkFrame(leftFrame)
    mouthfeel_frame.pack(fill='x', expand=False, padx=4, pady=(0,8))

    ctk.CTkLabel(mouthfeel_frame, text='Mouthfeel', font=(None, 13, 'bold')).pack(anchor='w', padx=8, pady=(6, 2))

    mf_inner = ctk.CTkFrame(mouthfeel_frame)
    mf_inner.pack(fill='both', expand=True, padx=4, pady=(0,6))

    for option in mouthfeels:
        var = tk.IntVar()
        mouthfeel_vars[option] = var
        cb = ctk.CTkCheckBox(mf_inner, text=option, variable=var)
        cb.pack(anchor='w', padx=8, pady=2)

    # Taste group
    taste_frame = ctk.CTkFrame(leftFrame, fg_color="transparent", corner_radius=6)
    taste_frame.pack(fill='both', expand=False, padx=0, pady=(0,8))
    ctk.CTkLabel(taste_frame, text='Taste / Feeling', font=(None, 13, 'bold')).pack(anchor='w', padx=8, pady=(6, 2))

    #Sweetness
    sweetness_var = tk.StringVar()
    sw_frame = ctk.CTkFrame(taste_frame, fg_color="transparent")
    sw_frame.pack(fill='x', padx=6, pady=(4, 0))
    ctk.CTkLabel(sw_frame, text='Sweetness:', width=80, anchor='w').pack(side="left")
    for option in sweets:
        rb = ctk.CTkRadioButton(sw_frame, text=option, variable=sweetness_var, value=option)
        rb.pack(side="left", padx=4)

    #Sourness
    sourness_var = tk.StringVar()
    so_frame = ctk.CTkFrame(taste_frame, fg_color="transparent")
    so_frame.pack(fill='x', padx=6, pady=(6, 0))
    ctk.CTkLabel(so_frame, text='Sourness:', width=80, anchor='w').pack(side="left")
    for option in sours:
        rb = ctk.CTkRadioButton(so_frame, text=option, variable=sourness_var, value=option)
        rb.pack(side="left", padx=4)

    #Alcohol Feeling
    alcohol_var = tk.StringVar()
    al_frame = ctk.CTkFrame(taste_frame, fg_color="transparent")
    al_frame.pack(fill='x', padx=6, pady=(6, 8))
    ctk.CTkLabel(al_frame, text='Alcohol:', width=80, anchor='w').pack(side="left")
    for option in alcohols:
        rb = ctk.CTkRadioButton(al_frame, text=option, variable=alcohol_var, value=option)
        rb.pack(side="left", padx=4)

    # Type
    type_frame = ctk.CTkFrame(leftFrame)
    type_frame.pack(fill='x', expand=False, padx=4, pady=(0, 8))
    ctk.CTkLabel(type_frame, text='Type', font=(None, 13, 'bold')).pack(anchor='w', padx=8, pady=(6, 2))
    type_var = tk.StringVar()
    type_combobox = ctk.CTkComboBox(type_frame, variable=type_var, values=types, width=220)
    type_combobox.pack(anchor='w', padx=10, pady=6)

# initial build
build_filter_ui()

# 標題放在頂部
title_label = ctk.CTkLabel(topFrame, text="酒吧管理系统", font=(None, 24, 'bold'))
title_label.pack(pady=12, side="left", padx=10)

# 管理酒譜按鈕（切換到 admin 面板）
def show_admin_panel():
    frame_filter.pack_forget()
    frame_list.pack_forget()
    frame_detail.pack_forget()
    frame_admin.pack(fill='both', expand=True, padx=10, pady=10)
    build_admin_ui()

def back_to_home_from_admin():
    frame_admin.pack_forget()
    frame_filter.pack(fill='both', expand=True, padx=10, pady=10)

manage_btn = ctk.CTkButton(topFrame, text='管理酒譜', command=show_admin_panel, width=120)
manage_btn.pack(side="right", padx=10, pady=8)

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
    frame_list.pack(fill="both", expand=True, padx=10, pady=10)

    for w in frame_list.winfo_children():
        w.destroy()

    ctk.CTkLabel(frame_list, text="符合條件的調酒", font=ctk.CTkFont(size=22, weight="bold")).pack(pady=15)

    for drink in matches:
        row = ctk.CTkFrame(frame_list, fg_color="transparent")
        row.pack(pady=5,padx=10, fill="x")

        ctk.CTkLabel(row, text=drink["row"]["drink_name"], width=200, anchor="w").pack(side="left", padx=(0, 10))
        ctk.CTkButton(
            row,
            text="選擇",
            command=lambda d=drink: open_secondary_window(d),
            width=90
        ).pack(side="left")

    ctk.CTkButton(
        frame_list,
        text="返回清單",
        command=back_to_filter,
        width=140
    ).pack(pady=20)


# 導航控制
def back_to_filter():
    frame_list.pack_forget()
    frame_filter.pack(fill="both", expand=True, padx=10, pady=10)

#UI
def build_admin_ui():
    for w in frame_admin.winfo_children():
        w.destroy()

    header = ctk.CTkLabel(frame_admin, text='酒譜管理', font=(None, 18, 'bold'))
    header.pack(pady=8)

    # 列出酒譜的表格
    cols = ('drink_name', 'Type', 'glassware', 'time', 'abv')
    table_frame = ctk.CTkFrame(frame_admin)
    table_frame.pack(fill="both", expand=True, padx=8, pady=8)

    tree = ttk.Treeview(table_frame, columns=cols, show='headings', selectmode='browse')
    for c in cols:
        tree.heading(c, text=c)
        tree.column(c, width=140, anchor='w')

    vsb = ttk.Scrollbar(table_frame, orient='vertical', command=tree.yview)
    tree.configure(yscrollcommand=vsb.set)
    vsb.pack(side="right", fill="y")
    tree.pack(side="left", fill="both", expand=True)

    # 加載資料到表格
    for idx, r in df_1.iterrows():
        vals = [str(r.get(c, '')) for c in cols]
        tree.insert('', 'end', iid=str(idx), values=vals)

    # 按鈕區域
    btn_frame = ctk.CTkFrame(frame_admin)
    btn_frame.pack(fill='x', pady=(0, 8), padx=8)

    def refresh():
        # 
        nonlocal tree
        try:
            global df_1
            df_1 = pd.read_csv(file_path)
        except Exception:
            pass
        for w in tree.get_children():
            tree.delete(w)
        for idx, r in df_1.iterrows():
            vals = [str(r.get(c, '')) for c in cols]
            tree.insert('', 'end', iid=str(idx), values=vals)

    def remove_selected():
        sel = tree.selection()
        if not sel:
            messagebox.showwarning('提示', '請先選擇要移除的項目')
            return
        idx = int(sel[0])
        name = df_1.loc[idx].get('drink_name', '') if 'drink_name' in df_1.columns else ''
        if not messagebox.askyesno('確認', f'確定要刪除「{name}」嗎？'):
            return
        # drop and save
        try:
            df_1.drop(index=idx, inplace=True)
            df_1.reset_index(drop=True, inplace=True)
            df_1.to_csv(file_path, index=False, encoding='utf-8-sig')
            refresh()
            messagebox.showinfo('已刪除', '已從資料庫移除該飲料')
        except Exception as e:
            messagebox.showerror('錯誤', f'刪除失敗：{e}')

    def add_new():
        # open a small form to add new drink
        add_win = ctk.CTkToplevel()
        add_win.title('新增飲料')
        fields = ['drink_name','Type','glassware','time','abv','ingredients','steps (加:\\n)','mouthfeel','flavor_tags','alcohol_feeling','sourness','sweetness']
        entries = {}
        for i, f in enumerate(fields):
            lbl = ctk.CTkLabel(add_win, text=f)
            lbl.grid(row=i, column=0, sticky='e', padx=6, pady=4)
            ent = ctk.CTkEntry(add_win, width=50)
            ent.grid(row=i, column=1, padx=6, pady=4)
            entries[f] = ent

        def save_new():
            new = {f: entries[f].get() for f in fields}
            try:
                global df_1
                for col in new.keys():
                    if col not in df_1.columns:
                        df_1[col] = ''
                row_for_df = {col: new.get(col, '') for col in df_1.columns}
                df_1 = pd.concat([df_1, pd.DataFrame([row_for_df])], ignore_index=True)
                df_1.to_csv(file_path, index=False, encoding='utf-8-sig')
                add_win.destroy()
                refresh()
                messagebox.showinfo('已新增', '已新增飲料到資料庫')
            except Exception as e:
                messagebox.showerror('錯誤', f'新增失敗：{e}')

        save_btn = ctk.CTkButton(add_win, text='儲存', command=save_new, width=120)
        save_btn.grid(row=len(fields), column=0, pady=10)
        cancel_btn = ctk.CTkButton(add_win, text='取消', command=add_win.destroy, width=120)
        cancel_btn.grid(row=len(fields), column=1, pady=10)

    add_btn = ctk.CTkButton(btn_frame, text='新增飲料', command=add_new, width=120)
    add_btn.pack(side="left", padx=6)

    remove_btn = ctk.CTkButton(btn_frame, text='移除選定', command=remove_selected, width=120)
    remove_btn.pack(side="left", padx=6)

    refresh_btn = ctk.CTkButton(btn_frame, text='重新整理', command=refresh, width=120)
    refresh_btn.pack(side="left", padx=6)

    back_btn = ctk.CTkButton(btn_frame, text='返回', command=back_to_home_from_admin, width=120)
    back_btn.pack(side="right", padx=6)

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

    matches = find_best_matches(df_1, selections, top_n=5)
    if matches:
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
    secondary_window = ctk.CTkToplevel()
    secondary_window.title(result_text['row'].get('drink_name', 'Details'))
    secondary_window.minsize(640, 420)

    main_frame = ctk.CTkFrame(secondary_window, corner_radius=0)
    main_frame.pack(fill='both', expand=True, padx=12, pady=12)

    left_col = ctk.CTkFrame(main_frame, width=260)
    left_col.pack(side="left", fill="y", padx=(0,12))

    right_col = ctk.CTkFrame(main_frame)
    right_col.pack(side="left", fill="both", expand=True)


    # =左邊: 基本資訊
    name_text = result_text['row'].get('drink_name') or result_text['row'].get('Type') or 'Unnamed'
    name_lbl = ctk.CTkLabel(left_col, text=name_text, font=(None, 16, 'bold'))
    name_lbl.pack(anchor='nw', pady=(0, 8))

    info_items = [
        ('Type', result_text['row'].get('Type', '')),
        ('Glassware', result_text['row'].get('glassware', '')),
        ('ABV', result_text['row'].get('abv', '')),
        ('Time', result_text['row'].get('time', '')),
        ('Sourness', result_text['row'].get('sourness', '')),
        ('Sweetness', result_text['row'].get('sweetness', '')),
        ('Alcohol Feeling', result_text['row'].get('alcohol_feeling', '')),
        ('Mouthfeel', result_text['row'].get('mouthfeel', '')),
        ('Flavor Tags', result_text['row'].get('flavor_tags', '')),
    ]

    for label, val in info_items:
        row = ctk.CTkFrame(left_col, fg_color="transparent")
        row.pack(anchor='w', pady=2, fill='x')
        ctk.CTkLabel(row, text=f"{label}:", width=110, anchor='w').pack(side="left")
        ctk.CTkLabel(row, text=str(val), anchor='w').pack(side="left")

    # 右邊: 成分和步驟
    ctk.CTkLabel(right_col, text='Ingredients', font=(None, 12, 'bold')).pack(anchor='nw')
    ingredients_text = ctk.CTkTextbox(right_col, height=6, wrap='word')
    ingredients_text.pack(fill='x', pady=(4,8))
    ingredients_text.insert('1.0', str(result_text['row'].get('ingredients', '')))
    ingredients_text.configure(state='disabled')

    ctk.CTkLabel(right_col, text='Steps', font=(None, 12, 'bold')).pack(anchor='nw')
    steps_frame = ctk.CTkFrame(right_col)
    steps_frame.pack(fill='both', expand=True)

    steps_text = ctk.CTkTextbox(steps_frame, wrap='word')
    steps_vsb = ttk.Scrollbar(steps_frame, orient='vertical', command=steps_text.yview)
    
    steps_text.configure(yscrollcommand=steps_vsb.set)
    steps_vsb.pack(side='right', fill='y')
    steps_text.pack(side="left", fill='both', expand=True, pady=(4, 4), padx=(0, 4))

    final_steps = str(result_text['row'].get('steps', '')).split("\\n")
    for i, s in enumerate(final_steps):
        steps_text.insert('end', f"Step {i+1}: {s}\n\n")
    steps_text.configure(state='disabled')

    # 下面的按鈕區域
    footer = ctk.CTkFrame(secondary_window, corner_radius=0)
    footer.pack(fill='x', padx=12, pady=(0, 8))

    notice = ctk.CTkLabel(footer, text="通知: 推薦為相似性最高的選項，可能不完全符合所有選擇", text_color='red')
    notice.pack(side="left")

    btn_frame = ctk.CTkFrame(footer, fg_color="transparent")
    btn_frame.pack(side="right")

    save_btn = ctk.CTkButton(btn_frame, text='保存到最愛', command=lambda: save_to_favorites(result_text['row'], fav_path='最喜歡的.csv'), width=130)
    save_btn.pack(side="left", padx=(0, 8))

    close_btn = ctk.CTkButton(btn_frame, text='關閉', command=secondary_window.destroy, width=90)
    close_btn.pack(side="left")

# 確認和離開按鈕
btn_right = ctk.CTkFrame(bottomFrame, fg_color="transparent")
btn_right.pack(side="right", padx=12, pady=10)

button = ctk.CTkButton(btn_right, text="確認", command=accumulate_choices, width=130, height=48)
button.pack(side="left", padx=(0, 8))

exit_button = ctk.CTkButton(btn_right, text="離開", command=exit_app, width=130, height=48)
exit_button.pack(side="left")

window.mainloop()