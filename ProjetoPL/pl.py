import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import linprog

def init_app():
    root = tk.Tk()
    root.title("Aplicação de Programação Linear")
    root.geometry("600x400")
    root.configure(bg="#f0f0f0")
    
    style = ttk.Style()
    style.configure("TLabel", background="#f0f0f0", font=("Arial", 12))
    style.configure("TButton", font=("Arial", 10, "bold"))

    create_method_selection(root)
    root.mainloop()

def create_method_selection(root):
    clear_widgets(root)
    frame = ttk.Frame(root, padding="10")
    frame.grid(row=0, column=0, padx=20, pady=20)
    
    ttk.Label(frame, text="Escolha o Método:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
    method_combobox = ttk.Combobox(frame, values=["Função Objetiva", "Simplex", "Método de Transporte"])
    method_combobox.grid(row=0, column=1, padx=10, pady=10)
    method_combobox.current(0)
    
    ttk.Button(frame, text="Selecionar", 
               command=lambda: load_method_interface(root, method_combobox.get())).grid(
        row=1, column=0, columnspan=2, pady=20)

def load_method_interface(root, method):
    clear_widgets(root)
    if method in ["Função Objetiva", "Simplex"]:
        create_linear_method_interface(root, method)
    elif method == "Método de Transporte":
        create_transport_method_interface(root)
    else:
        messagebox.showerror("Erro", f"Método '{method}' não é válido.")

def clear_widgets(root):
    for widget in root.winfo_children():
        widget.destroy()

def create_linear_method_interface(root, method):
    clear_widgets(root)
    frame = ttk.Frame(root, padding="10")
    frame.grid(row=0, column=0, padx=20, pady=20)

    obj_entry = create_labeled_entry(frame, "Coeficientes da Função Objetiva (ex: 3 5):", 0)
    restrictions_entry = create_labeled_entry(frame, "Restrições (ex: 1 1 <= 4; 2 1 <= 6):", 1)
    optimization_type = create_labeled_combobox(frame, "Tipo de Otimização:", ["Maximizar", "Minimizar"], 2)
    
    ttk.Button(frame, text="Resolver",
               command=lambda: solve_problem(root, obj_entry, restrictions_entry, optimization_type, method)).grid(
        row=3, column=0, columnspan=2, pady=20)
    
    ttk.Button(frame, text="Voltar", command=lambda: create_method_selection(root)).grid(row=4, column=0, columnspan=2, pady=10)

def create_transport_method_interface(root):
    clear_widgets(root)
    frame = ttk.Frame(root, padding="10")
    frame.grid(row=0, column=0, padx=20, pady=20)

    supply_entry = create_labeled_entry(frame, "Fornecimento (ex: 20 30 25):", 0)
    demand_entry = create_labeled_entry(frame, "Demanda (ex: 30 25 20):", 1)
    costs_entry = create_labeled_entry(frame, "Matriz de Custos (ex: 8 6 10; 9 12 13):", 2)
    
    ttk.Button(frame, text="Resolver",
               command=lambda: transport_method(root, supply_entry, demand_entry, costs_entry)).grid(
        row=3, column=0, columnspan=2, pady=20)
    
    ttk.Button(frame, text="Voltar", command=lambda: create_method_selection(root)).grid(row=4, column=0, columnspan=2, pady=10)

def create_labeled_entry(frame, text, row):
    ttk.Label(frame, text=text).grid(row=row, column=0, padx=10, pady=10, sticky="w")
    entry = ttk.Entry(frame, width=30)
    entry.grid(row=row, column=1, padx=10, pady=10)
    return entry

def create_labeled_combobox(frame, text, values, row):
    ttk.Label(frame, text=text).grid(row=row, column=0, padx=10, pady=10, sticky="w")
    combobox = ttk.Combobox(frame, values=values)
    combobox.grid(row=row, column=1, padx=10, pady=10)
    combobox.current(0)
    return combobox

def solve_problem(root, obj_entry, restrictions_entry, optimization_type, method):
    try:
        obj_func = list(map(float, obj_entry.get().split()))
        A_ub, b_ub = parse_restrictions(restrictions_entry.get())

        if len(obj_func) > 2:
            messagebox.showerror("Erro", "A função só suporta problemas com duas variáveis para visualização.")
            return

        if method == "Função Objetiva":
            plot_objective_function(obj_func, A_ub, b_ub, optimization_type.get())
        elif method == "Simplex":
            simplex_method(root, obj_func, A_ub, b_ub, optimization_type.get())
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {str(e)}")

def parse_restrictions(restrictions):
    A_ub, b_ub = [], []
    for restriction in restrictions.split(';'):
        parts = restriction.split()
        operator = next(op for op in ["<=", ">=", "="] if op in parts)
        index = parts.index(operator)
        coefficients = list(map(float, parts[:index]))
        limit = float(parts[index + 1])

        if operator == "<=":
            A_ub.append(coefficients)
            b_ub.append(limit)
        elif operator == ">=":
            A_ub.append([-c for c in coefficients])
            b_ub.append(-limit)
        elif operator == "=":
            A_ub += [coefficients, [-c for c in coefficients]]
            b_ub += [limit, -limit]
    return A_ub, b_ub

def plot_objective_function(obj_func, A_ub, b_ub, opt_type):
    x = np.linspace(0, 10, 100)
    fig, ax = plt.subplots()
    for i, (coeffs, limit) in enumerate(zip(A_ub, b_ub)):
        if coeffs[1] != 0:  # Verificação para evitar divisão por zero
            y = (limit - coeffs[0] * x) / coeffs[1]
            ax.plot(x, y, label=f'Restrição {i + 1}')
        else:
            messagebox.showwarning("Atenção", f"Coeficiente zero em Restrição {i + 1}. Não é possível calcular y.")

    if opt_type == "Minimizar":
        y_obj = (-obj_func[0] * x) / obj_func[1] if obj_func[1] != 0 else np.inf
    else:  # Maximizar
        y_obj = (obj_func[0] * x) / obj_func[1] if obj_func[1] != 0 else np.inf
        
    ax.plot(x, y_obj, '--', label='Função Objetiva')

    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.legend()
    plt.show()

def simplex_method(root, obj_func, A_ub, b_ub, opt_type):
    if opt_type == "Maximizar":
        obj_func = [-coef for coef in obj_func]  # Converter para minimização
    result = linprog(c=obj_func, A_ub=np.array(A_ub), b_ub=np.array(b_ub), method='highs')

    result_window = tk.Toplevel(root)
    result_window.title("Resultado do Simplex")
    ttk.Label(result_window, text=f"Status: {result.message}").pack()
    ttk.Label(result_window, text=f"Função Objetiva: {result.fun:.2f}").pack()
    ttk.Label(result_window, text=f"Variáveis: {result.x}").pack()

def transport_method(root, supply_entry, demand_entry, costs_entry):
    try:
        supply = list(map(int, supply_entry.get().split()))
        demand = list(map(int, demand_entry.get().split()))
        costs = [list(map(int, row.split())) for row in costs_entry.get().split(';')]

        if sum(supply) != sum(demand):
            messagebox.showerror("Erro", "A oferta total deve ser igual à demanda total.")
            return

        allocation, total_cost = northwest_corner_method(supply, demand, costs)
        
        result_window = tk.Toplevel(root)
        result_window.title("Resultado do Método de Transporte")

        tree = ttk.Treeview(result_window, columns=[f"C{i+1}" for i in range(len(demand))], show="headings")
        for i in range(len(demand)):
            tree.heading(f"C{i+1}", text=f"C{i+1}")
        for row in allocation:
            tree.insert("", "end", values=row)
        tree.pack()
        
        ttk.Label(result_window, text=f"Custo Total: {total_cost}").pack()

    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {str(e)}")

def northwest_corner_method(supply, demand, costs):
    allocation = [[0] * len(demand) for _ in range(len(supply))]
    total_cost = 0

    i = j = 0
    while i < len(supply) and j < len(demand):
        allocation[i][j] = min(supply[i], demand[j])
        total_cost += allocation[i][j] * costs[i][j]
        supply[i] -= allocation[i][j]
        demand[j] -= allocation[i][j]
        if supply[i] == 0:
            i += 1
        elif demand[j] == 0:
            j += 1

    return allocation, total_cost

init_app()
