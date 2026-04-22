import tkinter as tk
from tkinter import ttk, messagebox
import os
import winsound  
import threading 

class SimuladorChampionsPoderoso:
    def __init__(self, root):
        self.root = root
        self.root.title("UEFA Champions League - Analytics & Standings")
        self.root.geometry("1000x900") # Aumentamos un poco el alto para los nombres
        self.root.configure(bg="#000428") 
        
        self.matriz_datos = []

        # --- FUNCIÓN DE AUDIO (Usa himno.wav) ---
        def reproducir_audio():
            try:
                ruta_base = os.path.dirname(__file__)
                ruta_audio = os.path.join(ruta_base, "himno.wav.wav")
                if os.path.exists(ruta_audio):
                    winsound.PlaySound(ruta_audio, winsound.SND_FILENAME | winsound.SND_LOOP | winsound.SND_ASYNC)
            except:
                pass

        threading.Thread(target=reproducir_audio, daemon=True).start()

        # --- CABECERA ---
        self.frame_top = tk.Frame(self.root, bg="#000428")
        self.frame_top.pack(fill="x", pady=5)

        try:
            from PIL import Image, ImageTk
            ruta_logo = os.path.join(os.path.dirname(__file__), "logo.jpg")
            img_abierta = Image.open(ruta_logo)
            img_abierta = img_abierta.resize((130, 130)) 
            self.logo = ImageTk.PhotoImage(img_abierta)
            tk.Label(self.frame_top, image=self.logo, bg="#000428").pack()
        except:
            tk.Label(self.frame_top, text="UEFA", font=("Impact", 50), fg="#ffffff", bg="#000428").pack()

        # --- TEXTO PROFESIONAL ---
        tk.Label(self.frame_top, text="OFFICIAL DATA MANAGEMENT SYSTEM", font=("Verdana", 11, "bold"), fg="#00d4ff", bg="#000428").pack()
        tk.Label(self.frame_top, text="ESTADÍSTICAS EN TIEMPO REAL - TEMPORADA 2026", font=("Arial", 9, "italic"), fg="#ffffff", bg="#000428").pack(pady=(2, 5))

        # --- ESTADÍSTICAS RÁPIDAS ---
        self.frame_stats = tk.Frame(self.root, bg="#000428")
        self.frame_stats.pack(fill="x", padx=30)
        self.lbl_conteo = tk.Label(self.frame_stats, text="Equipos en Sistema: 0", font=("Arial", 10, "bold"), fg="#ffffff", bg="#001233", padx=10, pady=5)
        self.lbl_conteo.pack(side="left")

        # --- PANEL DE CONTROL ---
        frame = tk.LabelFrame(self.root, text=" PANEL DE COMPETICIÓN ", bg="#001233", fg="white", font=("Arial", 10, "bold"), bd=2)
        frame.pack(pady=10, padx=30, fill="x")

        self.equipos_reales = sorted(["Real Madrid", "Manchester City", "Bayern Múnich", "PSG", "Liverpool", 
                                     "Inter de Milán", "FC Barcelona", "Arsenal", "Bayer Leverkusen", 
                                     "Atlético de Madrid", "Borussia Dortmund", "Juventus"])

        self.vars = {}
        tk.Label(frame, text="CLUB", bg="#001233", fg="#ffffff", font=("Arial", 8, "bold")).grid(row=0, column=0, padx=10, pady=5)
        self.combo_equipo = ttk.Combobox(frame, values=self.equipos_reales, state="readonly", width=18, font=("Arial", 10))
        self.combo_equipo.grid(row=1, column=0, padx=10, pady=10)
        self.combo_equipo.set("Elegir...")

        campos_num = ["G", "E", "P", "GF", "GC"]
        for i, c in enumerate(campos_num):
            tk.Label(frame, text=c, bg="#001233", fg="#ffffff", font=("Arial", 8, "bold")).grid(row=0, column=i+1, padx=10, pady=5)
            self.vars[c] = tk.Entry(frame, width=7, justify="center", font=("Arial", 11))
            self.vars[c].grid(row=1, column=i+1, padx=10, pady=10)

        tk.Button(frame, text="REGISTRAR", bg="#2ecc71", fg="white", font=("Arial", 10, "bold"), command=self.registrar, width=12, cursor="hand2", relief="flat").grid(row=1, column=6, padx=10)
        tk.Button(frame, text="REINICIAR", bg="#e74c3c", fg="white", font=("Arial", 10, "bold"), command=self.limpiar_matriz, width=10, cursor="hand2", relief="flat").grid(row=1, column=7, padx=5)

        # --- TABLA ---
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="#ffffff", rowheight=30, font=("Arial", 10))
        style.configure("Treeview.Heading", background="#003366", foreground="white", font=("Arial", 9, "bold"))

        cols = ("Pos", "Club", "PJ", "G", "E", "P", "GF", "GC", "DG", "Pts")
        self.tabla = ttk.Treeview(self.root, columns=cols, show="headings", height=10)
        for c in cols:
            self.tabla.heading(c, text=c)
            self.tabla.column(c, width=90, anchor="center")
        
        self.tabla.tag_configure('clasificado', background='#c8e6c9', foreground='#1b5e20') 
        self.tabla.tag_configure('eliminado', background='#ffcdd2', foreground='#b71c1c')
        self.tabla.tag_configure('normal', background='#ffffff')
        self.tabla.pack(pady=10, padx=30, fill="both", expand=True)

        # --- SECCIÓN DE AUTORES (CRÉDITOS FINALES) ---
        frame_autores = tk.Frame(self.root, bg="#000428")
        frame_autores.pack(side="bottom", pady=20)

        tk.Label(frame_autores, text="DESARROLLADO POR:", font=("Arial", 8, "bold"), fg="#00d4ff", bg="#000428").pack()
        
        nombres = "Cesar Jaramillo  •  Andrés Patiño  •  John Sarmiento"
        tk.Label(frame_autores, text=nombres, font=("Verdana", 10, "bold"), fg="#ffffff", bg="#000428").pack()

        tk.Label(frame_autores, text="Estructura de Datos - Unidad 3 | UEFA Analytics v2.0", font=("Arial", 7), fg="#555555", bg="#000428").pack(pady=2)

    def registrar(self):
        try:
            n = self.combo_equipo.get()
            if n == "Elegir...":
                messagebox.showwarning("Atención", "Selecciona un equipo")
                return
            g, e, p = int(self.vars["G"].get()), int(self.vars["E"].get()), int(self.vars["P"].get())
            gf, gc = int(self.vars["GF"].get()), int(self.vars["GC"].get())
            if g < 0 or e < 0 or p < 0 or gf < 0 or gc < 0:
                messagebox.showerror("Error", "No se permiten negativos.")
                return
            for equipo in self.matriz_datos:
                if equipo[0] == n.upper():
                    messagebox.showwarning("Duplicado", f"{n} ya está registrado.")
                    return
            pj = g + e + p
            dg = gf - gc
            pts = (g * 3) + (e * 1)
            self.matriz_datos.append([n.upper(), pj, g, e, p, gf, gc, dg, pts])
            self.matriz_datos.sort(key=lambda x: (x[8], x[7]), reverse=True)
            self.actualizar_tabla()
            self.limpiar_campos()
        except ValueError:
            messagebox.showerror("Error", "Ingresa números válidos")

    def limpiar_campos(self):
        for v in self.vars.values(): v.delete(0, tk.END)
        self.combo_equipo.set("Elegir...")

    def limpiar_matriz(self):
        if messagebox.askyesno("Confirmar", "¿Deseas borrar toda la tabla?"):
            self.matriz_datos = []
            self.actualizar_tabla()

    def actualizar_tabla(self):
        for i in self.tabla.get_children(): self.tabla.delete(i)
        self.lbl_conteo.config(text=f"Equipos en Sistema: {len(self.matriz_datos)}")
        for i, fila in enumerate(self.matriz_datos):
            if i < 4: tag = 'clasificado'
            elif i >= 8: tag = 'eliminado'
            else: tag = 'normal'
            self.tabla.insert("", "end", values=(i+1, *fila), tags=(tag,))

if __name__ == "__main__":
    root = tk.Tk()
    app = SimuladorChampionsPoderoso(root)
    root.mainloop()