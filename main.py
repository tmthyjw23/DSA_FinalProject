"""
APLIKASI MANAJEMEN PROYEK
Dibangun dengan Python dan Tkinter
Mengimplementasikan struktur data dan algoritma dasar
"""

import tkinter as tk
from tkinter import messagebox
from ttkbootstrap import Style
from ttkbootstrap.constants import *
from ttkbootstrap.widgets import Entry, Button, Label, Frame

# ================================================
#                 STRUKTUR DATA
# ================================================

class LinkedListNode:
    """Node untuk Linked List"""
    def __init__(self, data):
        self.data = data  # Data yang disimpan (dictionary task)
        self.next = None  # Referensi ke node berikutnya

class LinkedList:
    """Implementasi Linked List Single Pointer"""
    def __init__(self):
        self.head = None  # Node pertama dalam linked list

    def append(self, data):
        """Menambahkan node baru di akhir linked list"""
        new_node = LinkedListNode(data)
        if not self.head:
            self.head = new_node
            return
        current = self.head
        while current.next:  # Traverse sampai node terakhir
            current = current.next
        current.next = new_node

    def remove(self, data):
        """Menghapus node berdasarkan nama task"""
        current = self.head
        prev = None
        while current:
            if current.data["name"] == data["name"]:
                if prev:
                    prev.next = current.next  # Skip node yang dihapus
                else:
                    self.head = current.next  # Update head jika node pertama
                return True
            prev = current
            current = current.next
        return False

    def to_list(self):
        """Konversi linked list ke Python list"""
        result = []
        current = self.head
        while current:
            result.append(current.data)
            current = current.next
        return result

class Stack:
    """Implementasi Stack menggunakan Python list"""
    def __init__(self):
        self.stack = []  # Struktur data stack

    def push(self, item):
        """Menambahkan item ke top of stack"""
        self.stack.append(item)

    def pop(self):
        """Mengambil dan menghapus item dari top of stack"""
        return self.stack.pop() if self.stack else None

    def remove(self, data):
        """Menghapus item tertentu dari stack (jika ada)"""
        if data in self.stack:
            self.stack.remove(data)
            return True
        return False

class Queue:
    """Implementasi Queue menggunakan Python list"""
    def __init__(self):
        self.queue = []  # Struktur data queue

    def enqueue(self, item):
        """Menambahkan item ke akhir queue"""
        self.queue.append(item)

    def dequeue(self):
        """Mengambil dan menghapus item dari front of queue"""
        return self.queue.pop(0) if self.queue else None

    def remove(self, data):
        """Menghapus item tertentu dari queue (jika ada)"""
        if data in self.queue:
            self.queue.remove(data)
            return True
        return False

class TreeNode:
    """Node untuk Binary Search Tree"""
    def __init__(self, task):
        self.task = task    # Data task (dictionary)
        self.left = None    # Child kiri
        self.right = None   # Child kanan

class Tree:
    """Implementasi Binary Search Tree untuk penyimpanan task"""
    def __init__(self):
        self.root = None  # Root node dari tree

    def insert(self, task):
        """Memasukkan task baru ke dalam tree secara rekursif"""
        def _insert(node):
            if not node:
                return TreeNode(task)
            if task["name"] < node.task["name"]:
                node.left = _insert(node.left)
            else:
                node.right = _insert(node.right)
            return node
        self.root = _insert(self.root)

    def delete(self, name):
        """Menghapus node berdasarkan nama task"""
        def _delete(node, name):
            if not node:
                return node
                
            # Pencarian node yang akan dihapus
            if name < node.task["name"]:
                node.left = _delete(node.left, name)
            elif name > node.task["name"]:
                node.right = _delete(node.right, name)
            else:
                # Kasus node dengan 0 atau 1 child
                if not node.left:
                    return node.right
                elif not node.right:
                    return node.left
                
                # Kasus node dengan 2 child: cari successor inorder
                temp = self._min_node(node.right)
                node.task = temp.task  # Salin data successor
                node.right = _delete(node.right, temp.task["name"])
            return node
        self.root = _delete(self.root, name)

    def _min_node(self, node):
        """Mencari node dengan nilai terkecil di subtree"""
        current = node
        while current.left:
            current = current.left
        return current

    def search(self, name):
        """Pencarian task berdasarkan nama"""
        def _search(node, name):
            if not node:
                return None
            if name == node.task["name"]:
                return node.task
            elif name < node.task["name"]:
                return _search(node.left, name)
            else:
                return _search(node.right, name)
        return _search(self.root, name)

# ================================================
#                 ALGORITMA
# ================================================

def linear_search(tasks, duration):
    """Algoritma Linear Search untuk mencari durasi tertentu"""
    for i, task in enumerate(tasks):
        if task["duration"] == duration:
            return i  # Mengembalikan index jika ditemukan
    return -1  # Return -1 jika tidak ditemukan

def binary_search(tasks, keyword):
    """Algoritma Binary Search untuk mencari nama task"""
    sorted_tasks = merge_sort(tasks.copy(), key="name")  # Data harus terurut
    left, right = 0, len(sorted_tasks) - 1
    
    while left <= right:
        mid = (left + right) // 2
        mid_name = sorted_tasks[mid]["name"].lower()
        
        # Pencarian case-insensitive
        if mid_name == keyword.lower():
            return sorted_tasks[mid]
        elif mid_name < keyword.lower():
            left = mid + 1
        else:
            right = mid - 1
    return None  # Return None jika tidak ditemukan

def bubble_sort(tasks, key="name"):
    """Algoritma Bubble Sort untuk mengurutkan task"""
    arr = tasks.copy()
    for i in range(len(arr)):
        # Membandingkan elemen bertetangga
        for j in range(len(arr) - i - 1):
            if arr[j][key] > arr[j + 1][key]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]  # Tukar posisi
    return arr

def merge_sort(tasks, key="name"):
    """Algoritma Merge Sort rekursif untuk mengurutkan task"""
    if len(tasks) <= 1:
        return tasks
    
    # Bagi list menjadi dua bagian
    mid = len(tasks) // 2
    left = merge_sort(tasks[:mid], key)
    right = merge_sort(tasks[mid:], key)
    
    return merge(left, right, key)

def merge(left, right, key):
    """Fungsi helper untuk menggabungkan dua list terurut"""
    result = []
    while left and right:
        # Bandingkan elemen pertama dari masing-masing list
        if left[0][key] <= right[0][key]:
            result.append(left.pop(0))
        else:
            result.append(right.pop(0))
    return result + left + right  # Gabungkan sisa elemen

def total_duration_recursive(tasks):
    """Menghitung total durasi menggunakan rekursi"""
    # Base case: list kosong
    if not tasks:
        return 0
    # Recursive case: jumlah elemen pertama + sisa list
    return tasks[0]["duration"] + total_duration_recursive(tasks[1:])

# ================================================
#                  GUI
# ================================================

class WelcomeScreen:
    """Tampilan awal aplikasi"""
    def __init__(self, root, on_continue):
        self.root = root
        self.root.title("Selamat Datang")
        
        # Frame utama
        self.frame = Frame(root, bootstyle="light", width=500, height=300)
        self.frame.pack_propagate(0)
        self.frame.pack(padx=30, pady=30)
        
        # Komponen GUI
        Label(self.frame, 
              text="Selamat Datang di Aplikasi Manajemen Proyek",
              font=("Helvetica", 16, "bold"), 
              bootstyle="dark").pack(pady=30)
        
        Button(self.frame, 
               text="Mulai", 
               bootstyle=SUCCESS, 
               command=self.start_app).pack(pady=10)
        
        self.on_continue = on_continue

    def start_app(self):
        """Menghancurkan frame welcome dan memulai aplikasi utama"""
        self.frame.destroy()
        self.on_continue()

class ProjectApp:
    """Aplikasi utama manajemen proyek"""
    def __init__(self, root):
        self.root = root
        self.root.title("Aplikasi Manajemen Proyek")
        
        # Inisialisasi struktur data
        self.tasks = []          # List untuk menyimpan semua task
        self.linked_list = LinkedList()  # Linked list
        self.stack = Stack()     # Stack
        self.queue = Queue()     # Queue
        self.tree = Tree()       # Binary Search Tree

        # Frame input
        entry_frame = Frame(root, padding=10)
        entry_frame.pack(pady=10)

        # Input nama tugas
        Label(entry_frame, text="Nama Tugas:").grid(row=0, column=0, padx=5, sticky=W)
        self.name_entry = Entry(entry_frame, width=30)
        self.name_entry.grid(row=1, column=0, padx=5, pady=5)

        # Input durasi
        Label(entry_frame, text="Durasi (jam):").grid(row=0, column=1, padx=5, sticky=W)
        self.duration_entry = Entry(entry_frame, width=30)
        self.duration_entry.grid(row=1, column=1, padx=5, pady=5)

        # Frame tombol aksi
        button_frame = Frame(root, padding=10)
        button_frame.pack(pady=5)

        # Daftar tombol dengan fungsi terkait
        buttons = [
            ("Tambah Tugas", self.add_task),
            ("Selesaikan Tugas", self.complete_task),
            ("Tampilkan Semua (LinkedList)", self.show_tasks),
            ("Urutkan Nama (Bubble Sort)", self.sort_bubble_name),
            ("Urutkan Durasi (Merge Sort)", self.sort_merge_duration),
            ("Cari Nama (Binary Search)", self.search_task_binary),
            ("Cari Durasi (Linear Search)", self.search_task_linear),
            ("Durasi Total (Rekursi)", self.show_total_duration)
        ]
        
        # Membuat tombol secara dinamis
        for text, command in buttons:
            Button(button_frame, 
                   text=text, 
                   command=command).pack(fill=X, pady=2)

    def add_task(self):
        """Menambahkan task baru ke semua struktur data"""
        # Validasi input
        name = self.name_entry.get().strip()
        duration_str = self.duration_entry.get().strip()

        if not name or not duration_str:
            messagebox.showwarning("Input Kosong", "Harap isi semua field!")
            return

        try:
            duration = int(duration_str)
            if duration <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Durasi harus bilangan bulat positif")
            return

        # Membuat task dictionary
        task = {"name": name, "duration": duration}
        
        # Menambahkan ke semua struktur data
        self.tasks.append(task)
        self.linked_list.append(task)
        self.stack.push(task)
        self.queue.enqueue(task)
        self.tree.insert(task)
        
        messagebox.showinfo("Berhasil", f"Tugas '{name}' ditambahkan")

    def complete_task(self):
        """Menghapus task dari semua struktur data"""
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showwarning("Input Kosong", "Masukkan nama tugas!")
            return

        # Mencari task yang akan dihapus
        task_to_remove = None
        for task in self.tasks:
            if task["name"].lower() == name.lower():
                task_to_remove = task
                break

        if not task_to_remove:
            messagebox.showinfo("Tidak Ditemukan", f"Tugas '{name}' tidak ada")
            return

        # Menghapus dari semua struktur data
        self.tasks.remove(task_to_remove)
        self.linked_list.remove(task_to_remove)
        self.stack.remove(task_to_remove)
        self.queue.remove(task_to_remove)
        self.tree.delete(name)
        
        messagebox.showinfo("Berhasil", f"Tugas '{name}' dihapus")

    def show_tasks(self):
        """Menampilkan semua task dari linked list"""
        tasks = self.linked_list.to_list()
        if not tasks:
            messagebox.showinfo("Info", "Belum ada tugas")
            return
        task_list = "\n".join([f"• {t['name']} ({t['duration']} jam)" for t in tasks])
        messagebox.showinfo("Daftar Tugas", task_list)

    def sort_bubble_name(self):
        """Menampilkan hasil sorting nama menggunakan Bubble Sort"""
        sorted_tasks = bubble_sort(self.tasks, key="name")
        self._show_sorted_result(sorted_tasks, "Diurutkan berdasarkan Nama")

    def sort_merge_duration(self):
        """Menampilkan hasil sorting durasi menggunakan Merge Sort"""
        sorted_tasks = merge_sort(self.tasks, key="duration")
        self._show_sorted_result(sorted_tasks, "Diurutkan berdasarkan Durasi")

    def _show_sorted_result(self, tasks, title):
        """Fungsi helper untuk menampilkan hasil sorting"""
        if not tasks:
            messagebox.showinfo("Info", "Belum ada tugas")
            return
        task_list = "\n".join([f"• {t['name']} ({t['duration']} jam)" for t in tasks])
        messagebox.showinfo(title, task_list)

    def search_task_linear(self):
        """Mencari task berdasarkan durasi menggunakan Linear Search"""
        duration_str = self.duration_entry.get().strip()
        if not duration_str:
            messagebox.showwarning("Input Kosong", "Masukkan durasi!")
            return
        
        try:
            duration = int(duration_str)
        except ValueError:
            messagebox.showerror("Error", "Durasi harus angka")
            return

        idx = linear_search(self.tasks, duration)
        if idx != -1:
            task = self.tasks[idx]
            messagebox.showinfo("Ditemukan", 
                f"Tugas: {task['name']}\nDurasi: {task['duration']} jam")
        else:
            messagebox.showinfo("Tidak Ditemukan", "Tugas tidak ditemukan")

    def search_task_binary(self):
        """Mencari task berdasarkan nama menggunakan Binary Search"""
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showwarning("Input Kosong", "Masukkan nama tugas!")
            return

        result = binary_search(self.tasks, name)
        if result:
            messagebox.showinfo("Ditemukan", 
                f"Tugas: {result['name']}\nDurasi: {result['duration']} jam")
        else:
            messagebox.showinfo("Tidak Ditemukan", "Tugas tidak ditemukan")

    def show_total_duration(self):
        """Menampilkan total durasi menggunakan rekursi"""
        total = total_duration_recursive(self.tasks)
        messagebox.showinfo("Total Durasi", 
            f"Total durasi semua tugas: {total} jam")

# ================================================
#                  MAIN
# ================================================

def main():
    """Fungsi utama untuk menjalankan aplikasi"""
    style = Style(theme="cosmo")  # Tema GUI
    root = style.master
    
    def start_main_app():
        """Callback untuk memulai aplikasi utama"""
        for widget in root.winfo_children():
            widget.destroy()
        ProjectApp(root)
    
    WelcomeScreen(root, start_main_app)
    root.mainloop()

if __name__ == "__main__":
    main()