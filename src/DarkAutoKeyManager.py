import os
import sys
import shutil
import re
import ctypes
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext

# --- FUNÇÃO PARA LOCALIZAR ARQUIVOS NO EXECUTÁVEL ---
def resource_path(relative_path):
    """ Retorna o caminho absoluto para o recurso, funciona para dev e para PyInstaller """
    try:
        # PyInstaller cria uma pasta temporária e armazena o caminho em _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# --- CORREÇÃO PARA ÍCONE NA BARRA DE TAREFAS ---
try:
    myappid = 'dark.autokeymanager.v1' 
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except Exception:
    pass

class DarkAutoKeyManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Dark AutoKeyManager v1.0")
        
        # USA A FUNÇÃO resource_path PARA ACHAR O ÍCONE
        try:
            # O caminho agora aponta para a pasta assets, subindo um nível se necessário
            icon_path = resource_path(os.path.join("assets", "icon.ico"))
            self.root.iconbitmap(icon_path)
        except Exception as e:
            print(f"Erro ao localizar ícone: {e}")

        self.root.geometry("650x550")
        self.root.configure(bg="#1e1e1e")

        self.server_path = tk.StringVar(value=os.getcwd())
        self.mode = tk.StringVar(value="local")

        # --- UI ---
        tk.Label(root, text="Dark AutoKeyManager", font=("Segoe UI", 20, "bold"), 
                 fg="#00aaff", bg="#1e1e1e").pack(pady=20)

        path_frame = tk.Frame(root, bg="#1e1e1e")
        path_frame.pack(pady=10, padx=30, fill="x")
        tk.Label(path_frame, text="Diretório do Servidor DayZ:", fg="#cccccc", bg="#1e1e1e").pack(anchor="w")
        
        tk.Entry(path_frame, textvariable=self.server_path, font=("Segoe UI", 10), 
                 bg="#2d2d2d", fg="#ffffff", borderwidth=0, insertbackground="white").pack(side="left", fill="x", expand=True, pady=5, ipady=4)
        
        tk.Button(path_frame, text="Procurar", command=self.browse_path, bg="#444444", 
                  fg="white", relief="flat", padx=10).pack(side="right", padx=(10, 0), pady=5)

        mode_frame = tk.LabelFrame(root, text=" Modo de Operação ", fg="#00aaff", bg="#1e1e1e", 
                                   font=("Segoe UI", 10, "bold"), padx=15, pady=10)
        mode_frame.pack(pady=20, padx=30, fill="x")
        tk.Radiobutton(mode_frame, text="Servidor LOCAL (Atualiza Keys + start.bat)", variable=self.mode, value="local", fg="#ffffff", bg="#1e1e1e", selectcolor="#333333").pack(anchor="w")
        tk.Radiobutton(mode_frame, text="Servidor ONLINE (Apenas Sincronização de Keys)", variable=self.mode, value="online", fg="#ffffff", bg="#1e1e1e", selectcolor="#333333").pack(anchor="w")

        self.btn_run = tk.Button(root, text="INICIAR AUTOMAÇÃO", font=("Segoe UI", 12, "bold"), 
                                 bg="#007acc", fg="white", relief="flat", command=self.start_process)
        self.btn_run.pack(pady=10, padx=30, fill="x", ipady=10)

        self.log_widget = scrolledtext.ScrolledText(root, height=12, font=("Consolas", 9), 
                                                   bg="#000000", fg="#00ff00", relief="flat", state="disabled")
        self.log_widget.pack(pady=(5, 20), padx=30, fill="both", expand=True)

    def browse_path(self):
        folder = filedialog.askdirectory()
        if folder: self.server_path.set(folder)

    def write_log(self, text):
        self.log_widget.configure(state="normal")
        self.log_widget.insert(tk.END, f"> {text}\n")
        self.log_widget.configure(state="disabled")
        self.log_widget.see(tk.END)
        self.root.update_idletasks()

    def start_process(self):
        path = self.server_path.get()
        if not os.path.exists(path):
            messagebox.showerror("Erro", "Diretório não encontrado.")
            return
        self.log_widget.configure(state="normal")
        self.log_widget.delete("1.0", tk.END)
        self.log_widget.configure(state="disabled")
        try:
            self.manage_keys(path)
            if self.mode.get() == "local": self.update_bat(path)
            self.write_log("--- PROCESSO CONCLUÍDO ---")
            messagebox.showinfo("Sucesso", "Automação finalizada!")
        except Exception as e:
            self.write_log(f"ERRO: {str(e)}")

    def manage_keys(self, path):
        self.write_log("Sincronizando .bikey...")
        key_folder = os.path.join(path, "keys")
        if not os.path.exists(key_folder): os.makedirs(key_folder)
        mods = [d for d in os.listdir(path) if d.startswith("@") and os.path.isdir(os.path.join(path, d))]
        valid_keys = set()
        for mod in mods:
            mod_key_path = os.path.join(path, mod, "keys")
            if os.path.exists(mod_key_path):
                for f in os.listdir(mod_key_path):
                    if f.endswith(".bikey"):
                        valid_keys.add(f)
                        shutil.copy2(os.path.join(mod_key_path, f), os.path.join(key_folder, f))
        self.write_log(f"{len(valid_keys)} chaves sincronizadas.")

    def update_bat(self, path):
        self.write_log("Atualizando start.bat...")
        bat_file = os.path.join(path, "start.bat")
        if not os.path.exists(bat_file): return
        mods = sorted([d for d in os.listdir(path) if d.startswith("@")])
        mod_line = ";".join(mods)
        with open(bat_file, "r", encoding="utf-8") as f: lines = f.readlines()
        new_lines = []
        for line in lines:
            if "-mod=" in line:
                new_lines.append(re.sub(r'("-mod=[^"]*")', f'"-mod={mod_line}"', line))
            else: new_lines.append(line)
        with open(bat_file, "w", encoding="utf-8") as f: f.writelines(new_lines)

if __name__ == "__main__":
    root = tk.Tk()
    app = DarkAutoKeyManager(root)
    root.mainloop()