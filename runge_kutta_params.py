from pydantic import BaseModel

class RungeKuttaParams(BaseModel):
    equation: str
    x0: float
    y0: float
    x_final: float
    h: float
    