import tkinter as tk
from tkinter import filedialog, messagebox, colorchooser, font
import os
import ctypes

# Funções auxiliares
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def save_file(filename, content):
    with open(filename, 'w') as file:
        file.write(content)
        messagebox.showinfo("Sucesso", "Arquivo salvo com sucesso!")

def set_text_color():
    color = colorchooser.askcolor(title="Selecione a cor do texto")
    if color[1]:
        text_area.config(fg=color[1])

def set_background_color():
    color = colorchooser.askcolor(title="Selecione a cor de fundo")
    if color[1]:
        text_area.config(bg=color[1])

def on_key_press(event):
    if event.char == '>':
        current_font = font.Font(text_area, text_area.cget("font"))
        text_area.tag_configure("title", font=("Arial", 14))
        text_area.configure(font=("Arial", 14))
        text_area.mark_set("title_start", "insert")
    elif event.keysym == "Return":
        text_area.tag_remove("title", "title_start", "insert")

# Configurações da janela principal
window = tk.Tk()
window.title("rGabriel Docs")
window.configure(bg="#333333")

# Definindo a cor das bordas
ctypes.windll.dwmapi.DwmSetWindowAttribute(window.winfo_id(), 2, ctypes.byref(ctypes.c_int(0)), 4)

# Variáveis globais
current_file = None

# Funções do editor
def open_file():
    global current_file

    file_path = filedialog.askopenfilename(filetypes=[("Arquivos de Texto", "*.txt")])

    if file_path:
        try:
            with open(file_path, 'r') as file:
                content = file.read()
                text_area.delete('1.0', tk.END)
                text_area.insert(tk.END, content)
                current_file = file_path
                window.title(f"rGabriel Docs - {current_file}")
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro ao abrir o arquivo:\n{str(e)}")

def save_file():
    global current_file

    if current_file:
        try:
            content = text_area.get('1.0', tk.END)
            save_file(current_file, content)
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro ao salvar o arquivo:\n{str(e)}")
    else:
        save_file_as()

def save_file_as():
    global current_file

    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Arquivos de Texto", "*.txt")])

    if file_path:
        try:
            content = text_area.get('2.0', tk.END)
            save_file(file_path, content)
            current_file = file_path
            window.title(f"SimpleText - {current_file}")
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro ao salvar o arquivo:\n{str(e)}")

# Área de texto
text_area = tk.Text(window, bg="#1a1a1a", fg="#ffffff", insertbackground="#ffffff")
text_area.pack(expand=True, fill=tk.BOTH)

# Configuração do evento de teclado
text_area.bind("->", on_key_press)

# Menu
menu_bar = tk.Menu(window)
file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Abrir", command=open_file)
file_menu.add_command(label="Salvar", command=save_file)
file_menu.add_command(label="Salvar como", command=save_file_as)
file_menu.add_separator()
file_menu.add_command(label="Sair", command=window.quit)
menu_bar.add_cascade(label="Arquivo", menu=file_menu)

# Opções
options_menu = tk.Menu(menu_bar, tearoff=0)
options_menu.add_command(label="Cor do Texto", command=set_text_color)
options_menu.add_command(label="Cor de Fundo", command=set_background_color)
menu_bar.add_cascade(label="Opções", menu=options_menu)

window.config(menu=menu_bar)

# Execução da janela principal
window.mainloop()
