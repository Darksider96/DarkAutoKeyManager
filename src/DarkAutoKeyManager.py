import os
import sys
import shutil
import re
import ctypes
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext

# --- TÉCNICO: resource_path e ctypes ---
def resource_path(relative_path):
    try: base_path = sys._MEIPASS
    except Exception: base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

try:
    myappid = 'dark.autokeymanager.v1.1' 
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except Exception: pass

# --- DICIONÁRIO DE TRADUÇÕES ---
TEXTS = {
    'pt': {
        'title': 'Dark AutoKeyManager v1.1',
        'dir_label': 'Diretório do Servidor DayZ:',
        'browse': 'Procurar',
        'mode_frame': ' Modo de Operação ',
        'radio_local': 'Servidor LOCAL (Atualiza Keys + start.bat)',
        'radio_online': 'Servidor ONLINE (Apenas Segurança de Keys)',
        'btn_start': 'INICIAR AUTOMAÇÃO',
        'log_label': 'Log de Atividades:',
        'lang_btn': 'English 🇺🇸',
        'msg_err_dir': 'Diretório não encontrado.',
        'msg_err_critical': 'Falha Crítica: ',
        'msg_success': 'Automação finalizada!',
        'log_start': 'Iniciando em:',
        'log_mod': 'Detectados {count} mods.',
        'log_keys': '{count} keys sincronizadas.',
        'log_cleaned': '{count} keys obsoletas removidas.',
        'log_preserv_bat': '[info] start.bat preservado.',
        'log_err_bat': '[erro] -mod= não localizado no start.bat.',
        'log_final': '--- PROCESSO CONCLUÍDO ---'
    },
    'en': {
        'title': 'Dark AutoKeyManager v1.1',
        'dir_label': 'DayZ Server Directory:',
        'browse': 'Browse',
        'mode_frame': ' Operation Mode ',
        'radio_local': 'LOCAL Server (Update Keys + start.bat)',
        'radio_online': 'ONLINE Server (Keys Security Only)',
        'btn_start': 'START AUTOMATION',
        'log_label': 'Activity Log:',
        'lang_btn': 'Português 🇧🇷',
        'msg_err_dir': 'Directory not found.',
        'msg_err_critical': 'Critical Failure: ',
        'msg_success': 'Automation finished!',
        'log_start': 'Starting at:',
        'log_mod': 'Detected {count} mods.',
        'log_keys': '{count} keys synchronized.',
        'log_cleaned': '{count} obsolete keys removed.',
        'log_preserv_bat': '[info] start.bat preserved.',
        'log_err_bat': '[erro] -mod= tag not found in start.bat.',
        'log_final': '--- PROCESS COMPLETED ---'
    }
}

class DarkAutoKeyManager:
    def __init__(self, root):
        self.root = root
        self.current_lang = 'pt' # Idioma inicial
        self.T = TEXTS[self.current_lang] # Atalho para tradução atual
        
        self.root.title(self.T['title'])
        
        try:
            icon_path = resource_path(os.path.join("assets", "icon.ico"))
            self.root.iconbitmap(icon_path)
        except Exception: pass 

        self.root.geometry("680x580")
        self.root.configure(bg="#1e1e1e")

        self.server_path = tk.StringVar(value=os.getcwd())
        self.mode = tk.StringVar(value="local")

        # --- CONSTRUÇÃO DA INTERFACE ---
        # Header + Botão de Idioma
        header_frame = tk.Frame(root, bg="#1e1e1e")
        header_frame.pack(pady=15, padx=30, fill="x")

        tk.Label(header_frame, text="Dark AutoKeyManager", font=("Segoe UI", 20, "bold"), 
                 fg="#00aaff", bg="#1e1e1e").pack(side="left")
        
        # Botão de Trocar Idioma
        self.btn_lang = tk.Button(header_frame, text=self.T['lang_btn'], font=("Segoe UI", 9), 
                                  bg="#333333", fg="white", relief="flat", command=self.toggle_language)
        self.btn_lang.pack(side="right", padx=(10, 0))

        # Seleção de Diretório
        path_frame = tk.Frame(root, bg="#1e1e1e")
        path_frame.pack(pady=10, padx=30, fill="x")
        
        self.lbl_dir = tk.Label(path_frame, text=self.T['dir_label'], fg="#cccccc", bg="#1e1e1e")
        self.lbl_dir.pack(anchor="w")
        
        tk.Entry(path_frame, textvariable=self.server_path, font=("Segoe UI", 10), 
                             bg="#2d2d2d", fg="#ffffff", borderwidth=0, insertbackground="white").pack(side="left", fill="x", expand=True, pady=5, ipady=4)
        
        self.btn_browse = tk.Button(path_frame, text=self.T['browse'], command=self.browse_path, bg="#444444", 
                  fg="white", relief="flat", padx=10)
        self.btn_browse.pack(side="right", padx=(10, 0), pady=5)

        # Modo de Operação
        self.mode_frame = tk.LabelFrame(root, text=self.T['mode_frame'], fg="#00aaff", bg="#1e1e1e", font=("Segoe UI", 10, "bold"), padx=15, pady=10)
        self.mode_frame.pack(pady=15, padx=30, fill="x")

        self.radio_l = tk.Radiobutton(self.mode_frame, text=self.T['radio_local'], variable=self.mode, value="local", fg="#ffffff", bg="#1e1e1e", selectcolor="#333333")
        self.radio_l.pack(anchor="w")
        self.radio_o = tk.Radiobutton(self.mode_frame, text=self.T['radio_online'], variable=self.mode, value="online", fg="#ffffff", bg="#1e1e1e", selectcolor="#333333")
        self.radio_o.pack(anchor="w")

        # Botão Executar
        self.btn_run = tk.Button(root, text=self.T['btn_start'], font=("Segoe UI", 12, "bold"), 
                                 bg="#007acc", fg="white", relief="flat", command=self.start_process)
        self.btn_run.pack(pady=10, padx=30, fill="x", ipady=10)

        # Log
        self.lbl_log = tk.Label(root, text=self.T['log_label'], fg="#aaaaaa", bg="#1e1e1e", font=("Segoe UI", 9))
        self.lbl_log.pack(anchor="w", padx=30)
        self.log_w = scrolledtext.ScrolledText(root, height=12, font=("Consolas", 9), bg="#000000", fg="#00ff00", relief="flat", state="disabled")
        self.log_w.pack(pady=(5, 20), padx=30, fill="both", expand=True)

    # --- FUNÇÕES DE IDIOMA ---
    def toggle_language(self):
        # Altera o estado
        self.current_lang = 'en' if self.current_lang == 'pt' else 'pt'
        self.T = TEXTS[self.current_lang]
        
        # Atualiza os textos da UI
        self.root.title(self.T['title'])
        self.btn_lang.configure(text=self.T['lang_btn'])
        self.lbl_dir.configure(text=self.T['dir_label'])
        self.btn_browse.configure(text=self.T['browse'])
        self.mode_frame.configure(text=self.T['mode_frame'])
        self.radio_l.configure(text=self.T['radio_local'])
        self.radio_o.configure(text=self.T['radio_online'])
        self.btn_run.configure(text=self.T['btn_start'])
        self.lbl_log.configure(text=self.T['log_label'])
        self.log_w.configure(state="normal")
        self.log_w.delete("1.0", tk.END) # Limpa log ao mudar idioma
        self.log_w.configure(state="disabled")

    # --- LÓGICA DE FUNCIONAMENTO (ATUALIZADA COM TRADUÇÕES) ---
    def browse_path(self):
        folder = filedialog.askdirectory()
        if folder: self.server_path.set(folder)

    def write_log(self, text):
        self.log_w.configure(state="normal")
        self.log_w.insert(tk.END, f"> {text}\n")
        self.log_w.configure(state="disabled")
        self.log_w.see(tk.END)
        self.root.update_idletasks()

    def start_process(self):
        path = self.server_path.get()
        if not os.path.exists(path):
            messagebox.showerror("Error" if self.current_lang == 'en' else "Erro", self.T['msg_err_dir'])
            return
        
        self.log_w.configure(state="normal")
        self.log_w.delete("1.0", tk.END)
        self.log_w.configure(state="disabled")

        self.write_log(f"{self.T['log_start']} {path}")

        try:
            self.manage_keys(path)
            if self.mode.get() == "local":
                self.update_bat(path)
            else:
                self.write_log(self.T['log_preserv_bat'])
            
            self.write_log(self.T['log_final'])
            messagebox.showinfo(self.T['btn_start'], self.T['msg_success'])
        except Exception as e:
            self.write_log(f"{self.T['msg_err_critical']}{str(e)}")

    def manage_keys(self, path):
        self.write_log(self.T['log_keys_sync'] if 'log_keys_sync' in self.T else "Sincronizando chaves...")
        key_folder = os.path.join(path, "keys")
        if not os.path.exists(key_folder): os.makedirs(key_folder)
        
        mods = [d for d in os.listdir(path) if d.startswith("@") and os.path.isdir(os.path.join(path, d))]
        valid_keys = set()
        
        # Lista de nomes possíveis para a pasta de chaves dentro do mod
        possible_key_dirs = ["keys", "key", "Key", "Keys"]

        for mod in mods:
            for folder_name in possible_key_dirs:
                mod_key_path = os.path.join(path, mod, folder_name)
                
                if os.path.exists(mod_key_path) and os.path.isdir(mod_key_path):
                    for f in os.listdir(mod_key_path):
                        if f.endswith(".bikey"):
                            valid_keys.add(f)
                            shutil.copy2(os.path.join(mod_key_path, f), os.path.join(key_folder, f))
                    # Se achou uma pasta válida e processou, não precisa testar as outras variações para este mod
                    break 
        
        self.write_log(self.T['log_keys'].format(count=len(valid_keys)))

        current_keys = [f for f in os.listdir(key_folder) if f.endswith(".bikey")]
        removed = 0
        for k in current_keys:
            if k not in valid_keys and k != "dayz.bikey":
                os.remove(os.path.join(key_folder, k))
                removed += 1
        if removed > 0: self.write_log(self.T['log_cleaned'].format(count=removed))

    def update_bat(self, path):
        bat_file = os.path.join(path, "start.bat")
        if not os.path.exists(bat_file): return
        mods = sorted([d for d in os.listdir(path) if d.startswith("@")])
        mod_line = ";".join(mods)
        with open(bat_file, "r", encoding="utf-8") as f: lines = f.readlines()
        new_lines = []
        pattern = r'("-mod=[^"]*")'
        replacement = f'"-mod={mod_line}"'
        found = False
        for line in lines:
            if "-mod=" in line:
                new_lines.append(re.sub(pattern, replacement, line))
                found = True
            else: new_lines.append(line)
        if found:
            with open(bat_file, "w", encoding="utf-8") as f: f.writelines(new_lines)
        else:
            self.write_log(self.T['log_err_bat'])

if __name__ == "__main__":
    root = tk.Tk()
    app = DarkAutoKeyManager(root)
    root.mainloop()