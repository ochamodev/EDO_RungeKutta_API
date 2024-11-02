from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import matplotlib.pyplot as plt
from io import BytesIO
from runge_kutta import string_to_function, runge_kutta_1, runge_kutta_2, runge_kutta_4, calculate_exact_solution
from runge_kutta_params import RungeKuttaParams
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
import sympy as sp
import uvicorn

app = FastAPI()
origins = [
    "http://localhost",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Endpoint para resolver la EDO y generar el gráfico (POST)
@app.post("/runge-kutta")
async def solve_runge_kutta(params: RungeKuttaParams):
    # Convertir la ecuación string en una función
    f = string_to_function(params.equation)
    x_exact = np.arange(params.x0, params.x_final + params.h, params.h)

    y_solved_function = calculate_exact_solution(params.equation, params.x0, params.y0)
    x1, y1, runge_k1 = runge_kutta_1(f, params.x0, params.y0, params.x_final, params.h)
    x2, y2, runge_k2 = runge_kutta_2(f, params.x0, params.y0, params.x_final, params.h)
    x4, y4, runge_k4 = runge_kutta_4(f, params.x0, params.y0, params.x_final, params.h)

    y_exact = y_solved_function(x_exact)

    plt.figure()
    plt.plot(x1, y1, label="Solución RK1 (Euler)", linestyle="--", color="green")
    plt.plot(x2, y2, label="Solución RK2", linestyle="-.", color="orange")
    plt.plot(x4, y4, label="Solución RK4", color="red")
    plt.plot(x_exact, y_exact, label='Solución exacta', color='purple', linestyle='--')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.legend()
    
    # Guardar el gráfico en un buffer
    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    
    # Guardar el gráfico en un buffer
    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)

    results = {
        "rk1": runge_k1,
        "rk2": runge_k2,
        "rk4": runge_k4
    }

    app.state.graph_image = buf.getvalue()

    return {
        "calcs": results,
        "graph_url": "/runge-kutta-graph"
    }

@app.get("/runge-kutta-graph")
async def get_runge_kutta_graph():
    buf = BytesIO(app.state.graph_image)
    return StreamingResponse(buf, media_type="image/png")


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)