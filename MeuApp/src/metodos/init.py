from .bisseccao import MetodoBisseccao
from .newton_raphson import MetodoNewtonRaphson
from .secante import MetodoSecante
from .gauss import MetodoGauss

METODOS_DISPONIVEIS = {
    "bisseccao": MetodoBisseccao(),
    "newton_raphson": MetodoNewtonRaphson(),
    "secante": MetodoSecante(),
    "gauss": MetodoGauss(),
}