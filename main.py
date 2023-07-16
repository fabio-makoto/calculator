from fastapi import FastAPI, Request, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

import webbrowser

from main_calculator import CostCalculator

app = FastAPI()


app.mount("/static", StaticFiles(directory="static"), name="static")


templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def get_user_data(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "title": "Calculadora de Custo Barbante"})


@app.post("/return_cost", response_class=HTMLResponse)
async def post_user_data(request: Request, starting_weight: int = Form(...), quantity_used: int = Form(...), total_used_weight: int = Form(...), paid_value: float = Form(...)):
    cost_calculator = CostCalculator(starting_weight, quantity_used, total_used_weight, paid_value)
    cost = f"R${cost_calculator.get_cost():.2f}"
    total_paid = f"R${cost_calculator.get_total_paid():.2f}"
    sell_price = f"R${cost_calculator.get_cost() * 3:.2f}"

    return templates.TemplateResponse("return-cost.html", {"request": request, "total_weight": f"{cost_calculator.get_total_weight()}g", "quantity_used": f"{quantity_used} un.", "total_used_weight": f"{total_used_weight}g", "total_paid": total_paid, "cost": cost, "sell_price": sell_price})


if __name__ == "__main__":
    import uvicorn

    webbrowser.open("http://localhost:8001")

    uvicorn.run("main:app", host="localhost", port=8001, reload=True)
