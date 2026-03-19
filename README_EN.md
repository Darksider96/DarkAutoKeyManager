# 🛠️ Dark AutoKeyManager v1.1

**Dark AutoKeyManager** is a robust automation tool developed by **Darksider96** (creator of DarkMonitor and DBS Mods) to simplify DayZ Standalone server management. Focused on productivity and security, this software automates mod key synchronization and server startup configuration.

---

## 🚀 Features

The software offers two distinct operating modes to suit your needs:

### 🏠 Local Server Mode
* **Key Synchronization**: Automatically scans mod folders (e.g., `@TakistanPlus`) and copies `.bikey` files to the root `/keys` directory.
* **Automatic Cleanup**: Removes orphaned keys from mods that are no longer present, preventing signature mismatches.
* **`start.bat` Update**: Uses Regex to find and update the `-mod=` line in your launch file, keeping it in sync with physical server folders.

### 🌐 Online Server Mode
* **Key Security**: Focuses solely on `/keys` folder integrity, ensuring only keys from active mods remain.
* **Config Preservation**: Does not modify `start.bat`, ideal for servers using GSP panels or custom startup scripts.

### 🆕 Multilingual Support (v1.1)
* Includes a toggle button to switch the UI between **Português** and **English** instantly.

---

## 🛠️ How to Use

1. Place the `DarkAutoKeyManager.exe` executable in your DayZ server root folder (next to `DayZServer_x64.exe`).
2. Run the program.
3. Choose your desired mode (**Local** or **Online**).
4. Click **START AUTOMATION**.
5. Check the activity log. Your server is sanitized and configured.

---

## 💻 Technical Stack

Built with a **Full-Stack Development** approach:
* **Language**: Python 3.12.
* **GUI**: Tkinter with dark mode styling and dynamic text translation.
* **Compiling**: PyInstaller with built-in resource support (`_MEIPASS`).

---

## 👤 Author

Developed by **Johnatan (Darksider96)**.
> Creator of tools like **DarkMonitor**, **Reino da Lógica**, and various mods for the DayZ community (DBS Mods).

---

## 📄 License

This project is licensed under the **MIT License**.