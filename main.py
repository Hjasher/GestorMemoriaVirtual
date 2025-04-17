import tkinter as tk
from tkinter import ttk, messagebox
from memory_manager import MemoryManager
from visualization import visualize_memory

class VirtualMemoryManagerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestor de Memoria Virtual")
        self.root.geometry("900x650")

        # Variables de control
        self.algorithm = tk.StringVar(value="FIFO")
        self.num_frames = tk.IntVar(value=4)
        self.future_accesses = tk.StringVar(value="1,2,3,4,1,2")  # Ejemplo para Óptimo

        # Inicializar MemoryManager (se actualiza al iniciar simulación)
        self.memory_manager = None

        # Crear interfaz
        self._create_widgets()

    def _create_widgets(self):
        # Frame de configuración
        config_frame = ttk.LabelFrame(self.root, text="Configuración", padding=10)
        config_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        # Selección de algoritmo
        ttk.Label(config_frame, text="Algoritmo:").grid(row=0, column=0, sticky="w")
        algorithm_menu = ttk.Combobox(
            config_frame, 
            textvariable=self.algorithm,
            values=["FIFO", "LRU", "OPTIMAL"],
            state="readonly"
        )
        algorithm_menu.grid(row=0, column=1, sticky="ew")

        # Número de marcos
        ttk.Label(config_frame, text="Marcos de memoria:").grid(row=1, column=0, sticky="w")
        ttk.Spinbox(config_frame, from_=1, to=10, textvariable=self.num_frames).grid(row=1, column=1, sticky="ew")

        # Entrada para secuencia futura (solo visible en Óptimo)
        self.future_label = ttk.Label(config_frame, text="Secuencia futura (separada por comas):")
        self.future_entry = ttk.Entry(config_frame, textvariable=self.future_accesses)
        
        # Botón de inicio
        ttk.Button(
            config_frame, 
            text="Iniciar Simulación", 
            command=self._initialize_simulation
        ).grid(row=3, column=0, columnspan=2, pady=5)

        # Frame de operación
        operation_frame = ttk.LabelFrame(self.root, text="Operación", padding=10)
        operation_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        # Entradas para proceso/página
        ttk.Label(operation_frame, text="ID del Proceso:").grid(row=0, column=0, sticky="w")
        self.process_id_entry = ttk.Entry(operation_frame)
        self.process_id_entry.grid(row=0, column=1, sticky="ew")

        ttk.Label(operation_frame, text="ID de la Página:").grid(row=1, column=0, sticky="w")
        self.page_id_entry = ttk.Entry(operation_frame)
        self.page_id_entry.grid(row=1, column=1, sticky="ew")

        # Botón de solicitud
        ttk.Button(
            operation_frame, 
            text="Solicitar Memoria", 
            command=self._request_memory,
            state="disabled"
        ).grid(row=2, column=0, columnspan=2, pady=5)

        # Área de estadísticas
        self.stats_text = tk.Text(operation_frame, height=5, state="disabled")
        self.stats_text.grid(row=3, column=0, columnspan=2, sticky="ew")

        # Actualizar visibilidad de la secuencia futura
        self.algorithm.trace_add("write", self._toggle_future_access_visibility)

    def _toggle_future_access_visibility(self, *args):
        if self.algorithm.get() == "OPTIMAL":
            self.future_label.grid(row=2, column=0, sticky="w")
            self.future_entry.grid(row=2, column=1, sticky="ew")
        else:
            self.future_label.grid_remove()
            self.future_entry.grid_remove()

    def _initialize_simulation(self):
        try:
            # Crear MemoryManager con la configuración seleccionada
            self.memory_manager = MemoryManager(
                num_frames=self.num_frames.get(),
                algorithm=self.algorithm.get()
            )
            # Habilitar botón de solicitud
            self.root.nametowidget(".!labelframe2.!button").config(state="normal")
            self._update_stats()
            messagebox.showinfo("Simulación iniciada", f"Algoritmo: {self.algorithm.get()}\nMarcos: {self.num_frames.get()}")
        except Exception as e:
            messagebox.showerror("Error", f"Error al iniciar: {str(e)}")

    def _request_memory(self):
        try:
            process_id = int(self.process_id_entry.get())
            page_id = int(self.page_id_entry.get())
            
            future_accesses = None
            if self.algorithm.get() == "OPTIMAL":
                future_accesses = [int(x.strip()) for x in self.future_accesses.get().split(",")]

            # Realizar solicitud
            is_hit = self.memory_manager.request_memory(process_id, page_id, future_accesses)
            result = "✅ Acierto" if is_hit else "❌ Fallo"
            messagebox.showinfo("Resultado", f"Acceso a Página {page_id}: {result}")

            # Actualizar interfaz
            self._update_stats()
            visualize_memory(self.memory_manager)

        except ValueError:
            messagebox.showerror("Error", "IDs deben ser números enteros")
        except Exception as e:
            messagebox.showerror("Error", f"Error en solicitud: {str(e)}")

    def _update_stats(self):
        stats = self.memory_manager.get_stats()
        self.stats_text.config(state="normal")
        self.stats_text.delete(1.0, tk.END)
        self.stats_text.insert(tk.END, 
            f"""Estadísticas:
- Fallos de página: {stats['page_faults']}
- Aciertos: {stats['page_hits']}
- Eficiencia: {stats['efficiency']:.2%}"""
        )
        self.stats_text.config(state="disabled")

if __name__ == "__main__":
    root = tk.Tk()
    app = VirtualMemoryManagerGUI(root)
    root.mainloop()

