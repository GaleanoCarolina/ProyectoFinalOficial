import tkinter as tk
from tkinter import ttk
import ttkbootstrap as tb
import math
from tkinter import messagebox

# aca devuelvo el factorial ya convertido en numeroentero para poder usarlo en el calculo de combinaciones Y PERM
def factorial_convertido(x):
    if x < 0 or int(x) != x:
        raise ValueError("El valor debe ser un entero no negativo")
    return math.factorial(int(x))

def combinacion_normal(n, r):
    n_i, r_i = int(n), int(r)
    if r_i < 0 or n_i < 0:
        raise ValueError("n y r deben ser enteros no negativos")
    return factorial_convertido(n_i) // (factorial_convertido(r_i) * factorial_convertido(n_i - r_i))

def calcular_perm_comb_valores(n, r, tipo):
    if tipo == "Permutación sin repetición (P(n,r))":
        if not isinstance(r, int):
            return "r debe ser un número entero."
        if n < 0 or r < 0:
            return "n y r deben ser no negativos."
        if r > n:
            return "Para permutación sin repetición, r no puede ser mayor que n."
        formula = f"P({n},{r}) = {n}! / ({n}-{r})!"
        resultado = factorial_convertido(n) // factorial_convertido(n - r)

    elif tipo == "Permutación con repetición (n^r)":
        if not isinstance(r, int):
            return "r debe ser un número entero."
        if n < 0 or r < 0:
            return "n y r deben ser no negativos."
        formula = f"n^r = {n}^{r}"
        resultado = pow(n, r)

    elif tipo == "Permutación con repetición (n!/(a!*b!*...))":
        partes = str(r).split(",")
        partes_limpias = [p.strip() for p in partes if p.strip() != ""]
        try:
            partes_nums = [int(p) for p in partes_limpias]
        except:
            return "Para la permutación con repetición factorial ingrese las repeticiones separadas por comas (ej: 2,2 o 2,1,1)."

        if n < 0:
            return "n debe ser no negativo."

        # solo una repetición dada
        if len(partes_nums) == 1:
            rep = partes_nums[0]
            if rep < 0:
                return "Las repeticiones deben ser no negativas."
            if rep > n:
                return "Una repetición no puede ser mayor que n."
            formula = f"{n}! / ({rep}!)"
            resultado = factorial_convertido(n) // factorial_convertido(rep)

        # varias repeticiones
        else:
            for rep in partes_nums:
                if rep < 0:
                    return "Las repeticiones deben ser no negativas."
            if sum(partes_nums) != n:
                return "La suma de las repeticiones debe ser igual a n."
            denom = 1
            for rep in partes_nums:
                denom *= factorial_convertido(rep)
            formula = f"{n}! / (" + " * ".join([f"{x}!" for x in partes_nums]) + ")"
            resultado = factorial_convertido(n) // denom

    elif tipo == "Combinación sin repetición (C(n,r))":
        if not isinstance(r, int):
            return "r debe ser un número entero."
        if n < 0 or r < 0:
            return "n y r deben ser no negativos."
        if r > n:
            return "Para combinación sin repetición, r no puede ser mayor que n."
        formula = f"C({n},{r}) = {n}! / ({r}! * {n-r}!)"
        resultado = combinacion_normal(n, r)

    elif tipo == "Combinación con repetición (C(n+r-1,r))":
        if not isinstance(r, int):
            return "r debe ser un número entero."
        if n < 0 or r < 0:
            return "n y r deben ser no negativos."
        formula = f"C({n}+{r}-1,{r}) = ({n+r-1})! / ({r}! * ({n-1})!)"
        resultado = combinacion_normal(n + r - 1, r)

    else:
        return "Seleccione una opción válida."

    if isinstance(resultado, int) or (isinstance(resultado, float) and resultado.is_integer()):
        return f"{formula}\nResultado: {int(resultado)}"
    else:
        return f"{formula}\nResultado: {resultado}"

def calcular_mcd_valores(a, b):
    pasos = []
    x, y = a, b
    while y != 0:
        pasos.append(f"{x} = {y} * ({x // y}) + {x % y}")
        x, y = y, x % y
    salida_texto = "Algoritmo de Euclides:\n" + "\n".join(pasos)
    salida_texto += f"\n\nM.C.D.({a}, {b}) = {x}"
    return salida_texto

# Conjuntospor aqui
def obtener_conjuntos(entry_A, entry_B):
    try:
        A = [x.strip() for x in entry_A.get().split(",") if x.strip()]
        B = [x.strip() for x in entry_B.get().split(",") if x.strip()]
        if not A or not B:
            raise ValueError
        return A, B
    except:
        messagebox.showerror("Error", "Ingrese ambos conjuntos correctamente separados por comas")
        return None, None

def union(entry_A, entry_B, resultado):
    A, B = obtener_conjuntos(entry_A, entry_B)
    if A is not None:
        resultado.set(f"Resultado: {{ {', '.join(sorted(set(A + B)))} }}")

def interseccion(entry_A, entry_B, resultado):
    A, B = obtener_conjuntos(entry_A, entry_B)
    if A is not None:
        resultado.set(f"Resultado: {{ {', '.join([x for x in A if x in B])} }}")

def diferencia(entry_A, entry_B, resultado):
    A, B = obtener_conjuntos(entry_A, entry_B)
    if A is not None:
        resultado.set(f"Resultado: {{ {', '.join([x for x in A if x not in B])} }}")

def abrir_matematicas(parent=None):
    is_root = parent is None
    if is_root:
        app = tb.Window(themename="superhero")
    else:
        app = tb.Toplevel(parent)

    app.title("Operaciones Matemáticas")
    app.geometry("760x620")
    tb.Label(app, text="Operaciones Matemáticas", font=("Arial", 20, "bold")).pack(pady=8)

    notebook = tb.Notebook(app)
    notebook.pack(expand=True, fill="both", padx=12, pady=8)

    tab_perm = ttk.Frame(notebook)
    notebook.add(tab_perm, text="Permutaciones / Combinaciones")

    frame_inputs = tb.Frame(tab_perm)
    frame_inputs.pack(pady=6)

    tb.Label(frame_inputs, text="n (total de elementos):").grid(row=0, column=0, padx=6, pady=4, sticky="e")
    entry_n = tb.Entry(frame_inputs, width=12)
    entry_n.grid(row=0, column=1, padx=6, pady=4)

    tb.Label(frame_inputs, text="r (elementos a elegir / repeticiones):").grid(row=1, column=0, padx=6, pady=4, sticky="e")
    entry_r = tb.Entry(frame_inputs, width=20)
    entry_r.grid(row=1, column=1, padx=6, pady=4)

    tb.Label(tab_perm, text="Tipo de cálculo:").pack(pady=(8,2))
    combo_perm_comb = tb.Combobox(tab_perm, values=[
        "Permutación sin repetición (P(n,r))",
        "Permutación con repetición (n^r)",
        "Permutación con repetición (n!/(a!*b!*...))",
        "Combinación sin repetición (C(n,r))",
        "Combinación con repetición (C(n+r-1,r))"
    ], state="readonly", width=45)
    combo_perm_comb.current(0)
    combo_perm_comb.pack(pady=6)

    salida_perm = tk.StringVar()
    tb.Label(tab_perm, text="Resultado:", font=("Arial", 13, "bold")).pack()
    tb.Label(tab_perm, textvariable=salida_perm, font=("Consolas", 11), justify="left", wraplength=700, bootstyle="light").pack(fill="both", padx=10, pady=8)

    def manejar_calculo_perm_comb():
        val_n = entry_n.get().strip()
        val_r = entry_r.get().strip()
        if val_n == "" or val_r == "":
            messagebox.showerror("Error", "Debe ingresar ambos valores (n y r).")
            return
        try:
            if combo_perm_comb.get() == "Permutación con repetición (n!/(a!*b!*...))":
                resultado_texto = calcular_perm_comb_valores(int(val_n), val_r, combo_perm_comb.get())
            else:
                resultado_texto = calcular_perm_comb_valores(int(val_n), int(val_r), combo_perm_comb.get())
            salida_perm.set(resultado_texto)
        except ValueError:
            messagebox.showerror("Error", "Entrada inválida. Use números enteros válidos.")

    tb.Button(tab_perm, text="Calcular", bootstyle="success",
              command=manejar_calculo_perm_comb).pack(pady=8)

    tab_mcd = ttk.Frame(notebook)
    notebook.add(tab_mcd, text="M.C.D. (Euclides)")

    frame_mcd = tb.Frame(tab_mcd)
    frame_mcd.pack(pady=8)

    tb.Label(frame_mcd, text="Número A:").grid(row=0, column=0, padx=6, pady=4, sticky="e")
    entry_a = tb.Entry(frame_mcd, width=12)
    entry_a.grid(row=0, column=1, padx=6, pady=4)

    tb.Label(frame_mcd, text="Número B:").grid(row=1, column=0, padx=6, pady=4, sticky="e")
    entry_b = tb.Entry(frame_mcd, width=12)
    entry_b.grid(row=1, column=1, padx=6, pady=4)

    salida_mcd = tk.StringVar()
    tb.Label(tab_mcd, text="Resultado:", font=("Arial", 13, "bold")).pack()
    tb.Label(tab_mcd, textvariable=salida_mcd, font=("Consolas", 11), justify="left", wraplength=700, bootstyle="light").pack(fill="both", padx=10, pady=8)

    def manejar_mcd():
        val_a = entry_a.get().strip()
        val_b = entry_b.get().strip()
        if val_a == "" or val_b == "":
            messagebox.showerror("Error", "Debe ingresar ambos valores (A y B).")
            return
        try:
            salida_mcd.set(calcular_mcd_valores(int(val_a), int(val_b)))
        except ValueError:
            messagebox.showerror("Error", "Entrada inválida. Use números enteros válidos.")

    tb.Button(tab_mcd, text="Calcular M.C.D.", bootstyle="success",
              command=manejar_mcd).pack(pady=8)

    tab_conj = ttk.Frame(notebook)
    notebook.add(tab_conj, text="Conjuntos")

    tb.Label(tab_conj, text="Operaciones con Conjuntos", font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=3, pady=10)

    tb.Label(tab_conj, text="Conjunto A:").grid(row=1, column=0, padx=10, pady=5)
    entry_A = tb.Entry(tab_conj, width=30)
    entry_A.grid(row=1, column=1, padx=10, pady=5)

    tb.Label(tab_conj, text="Conjunto B:").grid(row=2, column=0, padx=10, pady=5)
    entry_B = tb.Entry(tab_conj, width=30)
    entry_B.grid(row=2, column=1, padx=10, pady=5)

    resultado_conj = tk.StringVar()
    resultado_conj.set("Resultado aparecerá aquí")

    tb.Button(tab_conj, text="Unión (∪)", bootstyle="success",
              command=lambda: union(entry_A, entry_B, resultado_conj)).grid(row=3, column=0, padx=10, pady=10)
    tb.Button(tab_conj, text="Intersección (∩)", bootstyle="info",
              command=lambda: interseccion(entry_A, entry_B, resultado_conj)).grid(row=3, column=1, padx=10, pady=10)
    tb.Button(tab_conj, text="Diferencia (−)", bootstyle="warning",
              command=lambda: diferencia(entry_A, entry_B, resultado_conj)).grid(row=3, column=2, padx=10, pady=10)

    tb.Label(tab_conj, textvariable=resultado_conj, font=("Arial", 12), bootstyle="info").grid(row=4, column=0, columnspan=3, pady=20)

    def limpiar_todo():
        entry_n.delete(0, tk.END)
        entry_r.delete(0, tk.END)
        entry_a.delete(0, tk.END)
        entry_b.delete(0, tk.END)
        entry_A.delete(0, tk.END)
        entry_B.delete(0, tk.END)
        salida_perm.set("")
        salida_mcd.set("")
        resultado_conj.set("Resultado aparecerá aquí")

    tb.Button(app, text="Limpiar Todo", bootstyle="danger", command=limpiar_todo).pack(pady=6)

    if is_root:
        app.mainloop()
