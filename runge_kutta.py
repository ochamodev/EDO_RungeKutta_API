import numpy as np
import sympy as sp

def calculate_exact_solution(ecuacion_str, x0, y0):
    # Definir las variables simbólicas
    x = sp.Symbol('x')
    y = sp.Function('y')(x)
    
    ode_expr = sp.sympify(ecuacion_str, locals={'x': x, 'y': y})
    ode = sp.Eq(sp.Derivative(y, x), ode_expr)

    solution = sp.dsolve(ode, y, ics={y.subs(x, x0): y0})

    y_sol = sp.lambdify(x, solution.rhs, 'numpy')

    return y_sol



def string_to_function(ecuacion_str):
    x, y = sp.symbols('x y')
    ecuacion = sp.sympify(ecuacion_str)
    return sp.lambdify((x, y), ecuacion, 'numpy')

def runge_kutta_1(f, x0, y0, x_final, h):
    n = int((x_final - x0) / h)
    x = np.linspace(x0, x_final, n + 1)
    y = np.zeros(n + 1)
    y[0] = y0
    results = []
    for i in range(n):
        y[i + 1] = y[i] + h * f(x[i], y[i]) 
        results.append({"x": x[i], "y": y[i]})
    
    return x, y, results

def runge_kutta_2(f, x0, y0, x_final, h):
    n = int((x_final - x0) / h)
    x = np.linspace(x0, x_final, n + 1)
    y = np.zeros(n + 1)
    y[0] = y0
    results = []
    for i in range(n):
        k1 = h * f(x[i], y[i])
        k2 = h * f(x[i] + h / 2, y[i] + k1 / 2)
        y[i + 1] = y[i] + k2  # Actualización usando k2
        results.append({"x": x[i], "y": y[i]})
    
    return x, y, results

def runge_kutta_4(f, x0, y0, x_final, h):
    n = int((x_final - x0) / h)
    x = np.linspace(x0, x_final, n + 1)
    y = np.zeros(n + 1)
    y[0] = y0
    results = []  # Guardamos los resultados
    for i in range(n):
        k1 = h * f(x[i], y[i])
        k2 = h * f(x[i] + h / 2, y[i] + k1 / 2)
        k3 = h * f(x[i] + h / 2, y[i] + k2 / 2)
        k4 = h * f(x[i] + h, y[i] + k3)
        y[i + 1] = y[i] + (k1 + 2 * k2 + 2 * k3 + k4) / 6
        results.append({"x": x[i], "y": y[i]})
    
    return x, y, results
