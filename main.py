import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import database as db
import excel as ex

class StoreApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quản lý kho hàng")
        self.root.geometry("1150x600")
        db.init_db()

        # --- Menu Strip 2 (Top File Menu) ---
        menubar = tk.Menu(self.root)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Nhập", command=self.import_file, accelerator="Ctrl+I")
        file_menu.add_command(label="Xuất", command=self.export_file, accelerator="Ctrl+O")
        menubar.add_cascade(label="File", menu=file_menu)
        
        list_menu = tk.Menu(menubar, tearoff=0)
        list_menu.add_command(label="Thêm mới", command=self.open_add_window, accelerator="Ctrl+N")
        list_menu.add_command(label="Xóa hàng", command=self.delete_selected, accelerator="Delete")
        menubar.add_cascade(label="Danh sách", menu=list_menu)
        
        self.root.config(menu=menubar)

        # --- Menu Strip 1 (Search and Add Bar) ---
        search_frame = tk.Frame(self.root)
        search_frame.pack(fill="x", padx=5, pady=5)

        tk.Button(search_frame, text="Thêm Mới", command=self.open_add_window, bg="lightgreen").pack(side="left")
        
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", self.filter_data)
        tk.Entry(search_frame, textvariable=self.search_var, width=80).pack(side="right", padx=5)
        
        self.search_type = ttk.Combobox(search_frame, values=["Tên hàng", "Mã hàng"])
        self.search_type.set("Tên hàng")
        self.search_type.pack(side="right", padx=5)
        tk.Label(search_frame, text="Tìm kiếm theo:").pack(side="right")

        # --- Treeview (ListView Replacement) ---
        columns = ("id", "name", "qty", "price", "total", "note")
        self.tree = ttk.Treeview(self.root, columns=columns, show='headings')
        
        headings = ["Mã hàng", "Tên hàng", "Số lượng", "Giá tiền", "Tổng tiền", "Ghi chú"]
        for col, head in zip(columns, headings):
            self.tree.heading(col, text=head)
            self.tree.column(col, width=150)
        
        self.tree.pack(fill="both", expand=True, padx=5, pady=5)
        self.tree.bind("<Double-1>", self.open_edit_window)

        # Shortcuts
        self.root.bind("<Control-i>", lambda e: self.import_file())
        self.root.bind("<Control-o>", lambda e: self.export_file())
        self.root.bind("<Control-n>", lambda e: self.open_add_window())
        self.root.bind("<Delete>", lambda e: self.delete_selected())

        self.refresh_table()

    def refresh_table(self, data=None):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        items = data if data is not None else db.get_all_items()
        for row in items:
            self.tree.insert("", "end", values=row)

    def filter_data(self, *args):
        query = self.search_var.get().lower()
        all_data = db.get_all_items()
        col_idx = 1 if self.search_type.get() == "Tên hàng" else 0
        
        filtered = [r for r in all_data if query in str(r[col_idx]).lower()]
        self.refresh_table(filtered)

    def open_add_window(self):
        # Implementation of Form2 logic
        self.data_window("Thêm mới", None)

    def open_edit_window(self, event):
        # Implementation of Form3 logic
        selected = self.tree.selection()
        if selected:
            item_data = self.tree.item(selected[0])['values']
            self.data_window("Chỉnh sửa", item_data)

    def data_window(self, title, data):
        win = tk.Toplevel(self.root)
        win.title(title)
        
        labels = ["Mã hàng", "Tên hàng", "Số lượng", "Giá tiền", "Ghi chú"]
        entries = []
        for i, text in enumerate(labels):
            tk.Label(win, text=text).grid(row=i, column=0, padx=5, pady=5)
            ent = tk.Entry(win, width=40)
            ent.grid(row=i, column=1, padx=5, pady=5)
            if data: ent.insert(0, data[i] if i < 2 else data[i]) # Simplified mapping
            entries.append(ent)

        def save():
            try:
                item_id, name = entries[0].get(), entries[1].get()
                qty, price = int(entries[2].get()), float(entries[3].get())
                note = entries[4].get()
                total = qty * price
                
                if title == "Thêm mới":
                    if not db.add_item(item_id, name, qty, price, total, note):
                        messagebox.showerror("Lỗi", "Mã hàng bị trùng!")
                        return
                else:
                    db.update_item(item_id, name, qty, price, total, note)
                
                self.refresh_table()
                win.destroy()
            except ValueError:
                messagebox.showwarning("Nhập sai", "Vui lòng kiểm tra lại dữ liệu số.")

        tk.Button(win, text="Lưu", command=save, bg="lawn green").grid(row=5, column=1, sticky="e", pady=10)

    def delete_selected(self):
        selected = self.tree.selection()
        if selected:
            item_id = self.tree.item(selected[0])['values'][0]
            db.delete_item(item_id)
            self.refresh_table()

    def import_file(self):
        path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
        if path:
            if messagebox.askyesno("Xác nhận", "Nhập từ tập tin sẽ xóa dữ liệu cũ?"):
                c, d = ex.import_from_excel(path)
                msg = f"Thành công {c} hàng."
                if d > 0: msg += f" {d} hàng trùng bị bỏ qua."
                messagebox.showinfo("Nhập file", msg)
                self.refresh_table()

    def export_file(self):
        path = filedialog.asksaveasfilename(defaultextension=".xlsx")
        if path:
            if ex.export_to_excel(path):
                messagebox.showinfo("Xuất file", "Xuất dữ liệu thành công!")

if __name__ == "__main__":
    root = tk.Tk()
    app = StoreApp(root)
    root.mainloop()