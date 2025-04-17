# 🖥️ Gestor de Memoria Virtual - Simulación de Algoritmos de Paginación

**Autor**: Hjasher Diblathaim Medina Carranza  
**Cuenta**: 20231900178  
**Asignatura**: Sistemas Operativos I  
**Institución**: UNAH-CURC  

## 📌 Descripción
Simulador interactivo que implementa tres algoritmos de reemplazo de páginas en memoria virtual, desarrollado en Python con interfaz gráfica (Tkinter). Ideal para entender el comportamiento de:  
- **FIFO** (First-In, First-Out)  
- **LRU** (Least Recently Used)  
- **Óptimo** (Teórico)  

## 🎯 Objetivos
- Simular la gestión de memoria por paginación  
- Comparar visualmente el rendimiento de algoritmos  
- Generar estadísticas de fallos/aciertos  

## 🚀 Características
| Funcionalidad          | Detalle                                                                 |
|------------------------|-------------------------------------------------------------------------|
| Heatmap interactivo    | Visualización de marcos de memoria (azul=ocupado, blanco=libre)        |
| Gráficos comparativos  | Fallos vs aciertos                                                     |
| Exportación a PNG      | Guardado de gráficas para análisis posterior                           |
| Interfaz intuitiva     | Pestañas separadas para memoria, estadísticas e historial              |

## ⚙️ Requisitos
```bash
# Hardware
- Procesador: 1 GHz o superior
- RAM: 2 GB+ (para secuencias largas)

# Software
- Python 3.8+
- Bibliotecas:
  pip install matplotlib numpy