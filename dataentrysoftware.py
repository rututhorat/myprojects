from tkinter import *
from tkinter import messagebox, ttk
import re
import sqlite3

root = Tk()
root.title("Data Entry Software ")
root.geometry("1300x800")

# ================= Database Setup =================
conn = sqlite3.connect("data.db")
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        age INTEGER NOT NULL,
        gender TEXT NOT NULL,
        email TEXT NOT NULL,
        phone TEXT NOT NULL
    )
""")
conn.commit()

# ================= Functions =================
def validate_fields():
    fn = txtf.get().strip()
    ln = txtl.get().strip()
    a = txta.get().strip()
    gender = gender_cb.get().strip()
    email = txte.get().strip()
    phone = txtp.get().strip()

    if fn == "":
        messagebox.showerror("Error", "First Name cannot be empty")
        return False
    if ln == "":
        messagebox.showerror("Error", "Last Name cannot be empty")
        return False
    if a == "":
        messagebox.showerror("Error", "Age cannot be empty")
        return False
    if not a.isdigit() or int(a) <= 0:
        messagebox.showerror("Error", "Age must be a valid number greater than 0")
        return False
    if gender == "" or gender not in ["Male", "Female", "Other"]:
        messagebox.showerror("Error", "Please select a valid Gender")
        return False

    email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if not re.match(email_pattern, email):
        messagebox.showerror("Error", "Invalid Email Address")
        return False

    if not phone.isdigit() or len(phone) != 10:
        messagebox.showerror("Error", "Phone Number must be 10 digits")
        return False

    return True

def load_records():
    for row in tree.get_children():
        tree.delete(row)
    cursor.execute("SELECT * FROM users")
    for row in cursor.fetchall():
        tree.insert("", "end", iid=row[0], values=(row[1], row[2], row[3], row[4], row[5], row[6]))

def is_duplicate(fn, ln, skip_id=None):
    query = "SELECT id FROM users WHERE first_name=? AND last_name=?"
    params = (fn, ln)
    cursor.execute(query, params)
    result = cursor.fetchall()
    if skip_id:
        result = [r for r in result if r[0] != skip_id]
    return len(result) > 0

def savedata():
    if not validate_fields():
        return
    fn = txtf.get().strip()
    ln = txtl.get().strip()
    a = int(txta.get().strip())
    gender = gender_cb.get().strip()
    email = txte.get().strip()
    phone = txtp.get().strip()

    if is_duplicate(fn, ln):
        messagebox.showerror("Error", f"Record for {fn} {ln} already exists!")
        return

    cursor.execute("INSERT INTO users (first_name, last_name, age, gender, email, phone) VALUES (?, ?, ?, ?, ?, ?)",
                   (fn, ln, a, gender, email, phone))
    conn.commit()
    messagebox.showinfo("Save", "Record Saved Successfully")
    clear_fields()
    load_records()

def clear_fields():
    txtf.delete(0, END)
    txtl.delete(0, END)
    txta.delete(0, END)
    gender_cb.set("")
    txte.delete(0, END)
    txtp.delete(0, END)
    search_entry.delete(0, END)

def select_record(event):
    selected = tree.focus()
    if not selected:
        return
    values = tree.item(selected, "values")
    clear_fields()
    txtf.insert(0, values[0])
    txtl.insert(0, values[1])
    txta.insert(0, values[2])
    gender_cb.set(values[3])
    txte.insert(0, values[4])
    txtp.insert(0, values[5])

def update_record():
    selected = tree.focus()
    if not selected:
        messagebox.showwarning("Warning", "Please select a record to update")
        return
    if not validate_fields():
        return
    fn = txtf.get().strip()
    ln = txtl.get().strip()
    a = int(txta.get().strip())
    gender = gender_cb.get().strip()
    email = txte.get().strip()
    phone = txtp.get().strip()
    record_id = int(selected)

    if is_duplicate(fn, ln, skip_id=record_id):
        messagebox.showerror("Error", f"Record for {fn} {ln} already exists!")
        return

    cursor.execute("""
        UPDATE users
        SET first_name=?, last_name=?, age=?, gender=?, email=?, phone=?
        WHERE id=?
    """, (fn, ln, a, gender, email, phone, record_id))
    conn.commit()
    messagebox.showinfo("Update", "Record Updated Successfully")
    clear_fields()
    load_records()

def delete_record():
    selected = tree.focus()
    if not selected:
        messagebox.showwarning("Warning", "Please select a record to delete")
        return
    confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this record?")
    if confirm:
        cursor.execute("DELETE FROM users WHERE id=?", (int(selected),))
        conn.commit()
        clear_fields()
        load_records()
        messagebox.showinfo("Deleted", "Record Deleted Successfully")

def search_records():
    query_text = search_entry.get().strip()
    for row in tree.get_children():
        tree.delete(row)
    if query_text == "":
        load_records()
        return
    query = """
        SELECT * FROM users 
        WHERE first_name LIKE ? OR last_name LIKE ? OR gender LIKE ? OR email LIKE ? OR phone LIKE ?
    """
    param = ('%'+query_text+'%', '%'+query_text+'%', '%'+query_text+'%', '%'+query_text+'%', '%'+query_text+'%')
    cursor.execute(query, param)
    for row in cursor.fetchall():
        tree.insert("", "end", iid=row[0], values=(row[1], row[2], row[3], row[4], row[5], row[6]))

# ================= GUI Setup =================
header = Label(root, text="DATA ENTRY FORM WITH SQLITE & SEARCH", font="lucida 20 bold", bg="lightblue", fg="black")
header.grid(row=0, column=0, columnspan=2, pady=20, ipadx=10, ipady=10)

# Labels & Entry fields
lblf = Label(root, text="Enter First Name", font="lucida 15 bold")
txtf = Entry(root, font="lucida 15 bold")
lbll = Label(root, text="Enter Last Name", font="lucida 15 bold")
txtl = Entry(root, font="lucida 15 bold")
lbla = Label(root, text="Enter Age", font="lucida 15 bold")
txta = Entry(root, font="lucida 15 bold")
lblg = Label(root, text="Select Gender", font="lucida 15 bold")
gender_cb = ttk.Combobox(root, font="lucida 15 bold", values=["Male", "Female", "Other"], state="readonly")
lble = Label(root, text="Enter Email", font="lucida 15 bold")
txte = Entry(root, font="lucida 15 bold")
lblp = Label(root, text="Enter Phone Number", font="lucida 15 bold")
txtp = Entry(root, font="lucida 15 bold")

widgets = [(lblf, txtf), (lbll, txtl), (lbla, txta), (lblg, gender_cb), (lble, txte), (lblp, txtp)]
for i, (lbl, ent) in enumerate(widgets, start=3):
    lbl.grid(row=i, column=0, padx=15, pady=10, sticky="w")
    ent.grid(row=i, column=1, padx=15, pady=10)

# Buttons
btnsav = Button(root, text="Save Data", font="lucida 15 bold", bg="yellow", command=savedata)
btnsav.grid(row=9, column=0, padx=15, pady=15, ipadx=15, ipady=5)
btnupd = Button(root, text="Update", font="lucida 15 bold", bg="lightblue", command=update_record)
btnupd.grid(row=9, column=1, padx=15, pady=15, ipadx=15, ipady=5)
btndel = Button(root, text="Delete", font="lucida 15 bold", bg="red", fg="white", command=delete_record)
btndel.grid(row=10, column=0, padx=15, pady=15, ipadx=15, ipady=5)
btnclr = Button(root, text="Clear", font="lucida 15 bold", bg="lightgreen", command=clear_fields)
btnclr.grid(row=10, column=1, padx=15, pady=15, ipadx=15, ipady=5)

# Search
search_lbl = Label(root, text="Search Records:", font="lucida 15 bold")
search_lbl.grid(row=11, column=0, sticky="w", padx=15)
search_entry = Entry(root, font="lucida 15 bold")
search_entry.grid(row=11, column=1, sticky="w", padx=15)
search_entry.bind("<KeyRelease>", lambda event: search_records())

# Table
tree = ttk.Treeview(root, columns=("First Name", "Last Name", "Age", "Gender", "Email", "Phone"), show="headings", height=10)
tree.grid(row=12, column=0, columnspan=2, padx=20, pady=20)
for col in tree["columns"]:
    tree.heading(col, text=col)
    tree.column(col, width=150, anchor="center")
tree.bind("<ButtonRelease-1>", select_record)

# Load records initially
load_records()



root.mainloop()
conn.close()
