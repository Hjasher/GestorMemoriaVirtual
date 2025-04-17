import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.colors import LinearSegmentedColormap
import os

def export_figure(figure, default_name):
    """Guarda una figura matplotlib como PNG"""
    filepath = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[("PNG files", "*.png"), ("All files", "*.*")],
        initialfile=default_name,
        title="Guardar gráfico como PNG"
    )
    if filepath:
        try:
            figure.savefig(filepath, dpi=300, bbox_inches='tight')
            messagebox.showinfo("Éxito", f"Gráfico guardado como:\n{os.path.basename(filepath)}")
            return True
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar:\n{str(e)}")
    return False

def visualize_memory(memory_manager):
    # Obtener datos del memory_manager
    frames, page_table = memory_manager.get_memory_state()
    access_history = memory_manager.get_access_history()
    stats = memory_manager.get_stats()

    # Crear ventana de visualización
    visualization_window = tk.Toplevel()
    visualization_window.title("Estado de la Memoria - Algoritmo: " + memory_manager.algorithm)
    visualization_window.geometry("1000x850")  # Aumentado para mejor visualización

    # Notebook (pestañas)
    notebook = ttk.Notebook(visualization_window)
    notebook.pack(fill="both", expand=True)

    # --- Pestaña 1: Estado de Memoria ---
    tab_memory = ttk.Frame(notebook)
    notebook.add(tab_memory, text="Memoria")

    # Heatmap de marcos (VERSIÓN MEJORADA)
    heatmap_frame = ttk.LabelFrame(tab_memory, text="Marcos de Memoria", padding=10)
    heatmap_frame.pack(fill="x", padx=10, pady=5)

    # Configuración del heatmap con más espacio
    fig_heatmap, ax_heatmap = plt.subplots(figsize=(10, 2.8))  # Altura aumentada
    plt.subplots_adjust(bottom=0.35)  # Más margen inferior para etiquetas
    
    cmap = LinearSegmentedColormap.from_list("custom", ["white", "steelblue"])
    heatmap_data = [[1 if frame is not None else 0 for frame in frames]]
    
    # Heatmap con etiquetas rotadas
    heatmap = ax_heatmap.imshow(heatmap_data, cmap=cmap, aspect="auto", vmin=0, vmax=1)
    ax_heatmap.set_xticks(range(len(frames)))
    ax_heatmap.set_xticklabels(
        [f"Frame {i}" for i in range(len(frames))],
        rotation=45,
        ha="right",
        fontsize=10,
        rotation_mode="anchor"
    )
    ax_heatmap.set_yticks([])
    
    # Texto de páginas más claro
    for i, frame in enumerate(frames):
        if frame is not None:
            ax_heatmap.text(
                i, 0, f"P{frame}",
                ha="center", va="center",
                color="white", fontweight="bold", fontsize=12
            )

    # Botón de exportación
    heatmap_btn_frame = ttk.Frame(heatmap_frame)
    heatmap_btn_frame.pack(fill="x", pady=5)
    ttk.Button(
        heatmap_btn_frame,
        text="Exportar Heatmap como PNG",
        command=lambda: export_figure(fig_heatmap, f"heatmap_{memory_manager.algorithm}")
    ).pack(side="left", padx=5)

    canvas_heatmap = FigureCanvasTkAgg(fig_heatmap, master=heatmap_frame)
    canvas_heatmap.draw()
    canvas_heatmap.get_tk_widget().pack(fill="x")

    # Tabla de páginas
    table_frame = ttk.LabelFrame(tab_memory, text="Tabla de Páginas", padding=10)
    table_frame.pack(fill="x", padx=10, pady=10)

    for i, (page_id, process_id) in enumerate(page_table.items()):
        ttk.Label(table_frame, text=f"Página {page_id} → Proceso {process_id}").grid(row=i, column=0, sticky="w")

    # --- Pestaña 2: Estadísticas ---
    tab_stats = ttk.Frame(notebook)
    notebook.add(tab_stats, text="Estadísticas")

    stats_frame = ttk.LabelFrame(tab_stats, text="Rendimiento", padding=10)
    stats_frame.pack(fill="both", expand=True, padx=10, pady=10)

    fig_stats, ax_stats = plt.subplots(figsize=(8, 4))
    metrics = ["Fallos", "Aciertos"]
    values = [stats["page_faults"], stats["page_hits"]]
    colors = ["salmon", "lightgreen"]
    
    bars = ax_stats.bar(metrics, values, color=colors)
    ax_stats.set_title(f"Eficiencia: {stats['efficiency']:.2%}")
    ax_stats.set_ylabel("Cantidad")
    
    for bar in bars:
        height = bar.get_height()
        ax_stats.annotate(f"{height}",
            xy=(bar.get_x() + bar.get_width() / 2, height),
            xytext=(0, 3),
            textcoords="offset points",
            ha="center", va="bottom")

    # Botón de exportación para estadísticas
    stats_btn_frame = ttk.Frame(stats_frame)
    stats_btn_frame.pack(fill="x", pady=5)
    ttk.Button(
        stats_btn_frame,
        text="Exportar Gráfico como PNG",
        command=lambda: export_figure(fig_stats, f"stats_{memory_manager.algorithm}")
    ).pack(side="left", padx=5)

    canvas_stats = FigureCanvasTkAgg(fig_stats, master=stats_frame)
    canvas_stats.draw()
    canvas_stats.get_tk_widget().pack(fill="both", expand=True)

    # --- Pestaña 3: Historial ---
    tab_history = ttk.Frame(notebook)
    notebook.add(tab_history, text="Historial")

    history_frame = ttk.LabelFrame(tab_history, text="Historial de Accesos", padding=10)
    history_frame.pack(fill="both", expand=True, padx=10, pady=10)

    canvas = tk.Canvas(history_frame)
    scrollbar = ttk.Scrollbar(history_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas)

    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    temp_history = []
    for i, page_id in enumerate(access_history):
        color = "green" if page_id in temp_history else "red"
        temp_history.append(page_id)
        ttk.Label(
            scrollable_frame,
            text=f"Acceso {i}: Página {page_id}",
            foreground="white",
            background=color,
            padding=5,
            font=('Helvetica', 10, 'bold')
        ).grid(row=i, column=0, sticky="ew", pady=2)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    visualization_window.mainloop()