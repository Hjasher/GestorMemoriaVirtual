class MemoryManager:
    def __init__(self, num_frames, algorithm="FIFO"):
        """
        Inicializa el gestor de memoria virtual.
        
        Args:
            num_frames (int): Número de marcos de memoria física.
            algorithm (str): Algoritmo de reemplazo ("FIFO", "LRU", "OPTIMAL").
        """
        self.num_frames = num_frames
        self.frames = [None] * num_frames  # Marcos de memoria física
        self.page_table = {}               # {page_id: process_id}
        self.access_history = []           # Historial de accesos
        self.page_faults = 0               # Contador de fallos de página
        self.page_hits = 0                 # Contador de aciertos
        self.algorithm = algorithm         # Algoritmo seleccionado

    def request_memory(self, process_id, page_id, future_accesses=None):
        """
        Simula una solicitud de memoria por parte de un proceso.
        
        Args:
            process_id (int): ID del proceso solicitante.
            page_id (int): ID de la página solicitada.
            future_accesses (list, optional): Secuencia futura para OPTIMAL.
            
        Returns:
            bool: True si fue un acierto, False si fue un fallo.
        """
        if page_id in self.page_table:
            # Acierto: actualiza el proceso dueño y registra acceso
            self.page_table[page_id] = process_id  # ¡Cambio clave aquí!
            self.access_history.append(page_id)
            self.page_hits += 1
            return True  # Acierto

        # Fallo de página: cargar la página en memoria
        self.page_faults += 1
        if None in self.frames:
            empty_frame = self.frames.index(None)
            self.frames[empty_frame] = page_id
        else:
            if self.algorithm == "FIFO":
                self._replace_page_fifo(page_id)
            elif self.algorithm == "LRU":
                self._replace_page_lru(page_id)
            elif self.algorithm == "OPTIMAL":
                if future_accesses is None:
                    raise ValueError("OPTIMAL requiere future_accesses")
                self._replace_page_optimal(page_id, future_accesses)

        # Registrar la nueva página (o reemplazo)
        self.page_table[page_id] = process_id  # Asignar/actualizar dueño
        self.access_history.append(page_id)
        return False  # Fallo

    def _replace_page_fifo(self, page_id):
        """Reemplazo FIFO (First-In-First-Out)."""
        oldest_page = self.access_history.pop(0)
        frame_to_replace = self.frames.index(oldest_page)
        del self.page_table[oldest_page]  # Mantener consistencia
        self.frames[frame_to_replace] = page_id

    def _replace_page_lru(self, page_id):
        """Reemplazo LRU (Least Recently Used)."""
        # Últimos accesos de cada página en el historial
        last_access = {page: idx for idx, page in enumerate(self.access_history)}
        oldest_page = min(last_access.keys(), key=lambda k: last_access[k])
        frame_to_replace = self.frames.index(oldest_page)
        del self.page_table[oldest_page]
        self.frames[frame_to_replace] = page_id

    def _replace_page_optimal(self, page_id, future_accesses):
        """Reemplazo Óptimo (requiere secuencia futura)."""
        frames_in_use = set(self.frames)
        future_uses = {}
        
        # Analizar usos futuros
        for idx, future_page in enumerate(future_accesses):
            if future_page in frames_in_use and future_page not in future_uses:
                future_uses[future_page] = idx

        # Buscar página óptima para reemplazar
        for frame in self.frames:
            if frame not in future_uses:  # Página que no se usará
                oldest_page = frame
                break
        else:
            # Si todas aparecen, elegir la última en usarse
            oldest_page = max(future_uses.keys(), key=lambda k: future_uses[k])

        frame_to_replace = self.frames.index(oldest_page)
        del self.page_table[oldest_page]
        self.frames[frame_to_replace] = page_id

    def get_memory_state(self):
        """Devuelve el estado actual de la memoria."""
        return self.frames.copy(), self.page_table.copy()

    def get_access_history(self):
        """Devuelve el historial de accesos."""
        return self.access_history.copy()

    def get_stats(self):
        """
        Devuelve estadísticas de rendimiento.
        
        Returns:
            dict: {
                "page_faults": int,
                "page_hits": int,
                "efficiency": float (tasa de aciertos)
            }
        """
        total_accesses = self.page_hits + self.page_faults
        efficiency = self.page_hits / total_accesses if total_accesses > 0 else 0
        return {
            "page_faults": self.page_faults,
            "page_hits": self.page_hits,
            "efficiency": efficiency
        }

    def reset(self):
        """Reinicia el estado del gestor de memoria."""
        self.frames = [None] * self.num_frames
        self.page_table = {}
        self.access_history = []
        self.page_faults = 0
        self.page_hits = 0