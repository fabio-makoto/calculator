from fastapi import FastAPI, Request, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

import webbrowser

from main_calculator import NewCostCalculator

app = FastAPI()


app.mount("/static", StaticFiles(directory="static"), name="static")


templates = Jinja2Templates(directory="templates")


@app.get("/home", response_class=HTMLResponse)
async def home(request: Request):
        return templates.TemplateResponse("index.html", {"request": request})
    

@app.post("/new", response_class=HTMLResponse)
async def get_new_data(request: Request):
    return templates.TemplateResponse("new.html", {"request": request, "title": "Calculadora de Preços Barbante"})


@app.post("/new/new_return_cost", response_class=HTMLResponse)
async def post_new_data(request: Request, starting_weight: int = Form(...), quantity_used: int = Form(...), total_used_weight: int = Form(...), paid_value: float = Form(...)):
    cost_calculator = NewCostCalculator(starting_weight, quantity_used, total_used_weight, paid_value)
    cost = cost_calculator.get_cost()
    total_paid = f"R${cost_calculator.get_total_paid():.2f}"
    rounded_sell_price = round(cost_calculator.get_cost() * 2.5)
    profit = rounded_sell_price - cost
    reinvest = profit * 30 / 100
    own_profit = profit * 70 / 100

    return templates.TemplateResponse("return-new-cost.html", {"request": request, "total_weight": f"{cost_calculator.get_total_weight()}g", "quantity_used": f"{quantity_used} un.", "total_used_weight": f"{total_used_weight}g", "total_paid": total_paid, "cost": f"R${cost:.2f}", "sell_price": f"R${rounded_sell_price:.2f}", "profit": f"R${profit:.2f}", "reinvest": f"R${reinvest+cost:.2f}", "own_profit": f"R${own_profit:.2f}"})


@app.get("/new/new_return_cost/shopee_profit", response_class=HTMLResponse)
async def post_shopee_profit(request: Request):
    return templates.TemplateResponse("shopee_profit.html", {"request": request})


@app.post("/new/new_return_cost/shopee_profit/return_profit", response_class=HTMLResponse)
async def post_return_shopee_profit(request: Request, cost_shopee: float = Form(...), sell_price: float = Form(...)):
    final_value = (sell_price - (sell_price * 12 / 100)) - 2
    final_profit = final_value - cost_shopee
    value_to_reinvest = cost_shopee + (final_profit * 30 / 100)  # aqui estou pegando 30% do lucro bruto + o custo
    your_profit = final_profit * 70 / 100  # aqui estou pegando 70% do lucro bruto para mim

    return templates.TemplateResponse("return_shopee_profit.html", {"request": request, "cost": f"R${cost_shopee:.2f}", "sell_price": f"R${sell_price:.2f}", "final_value": f"R${final_value:.2f}", "total_final_profit": f"R${final_profit:.2f}", "value_to_reinvest": f"R${value_to_reinvest:.2f}", "your_profit": f"R${your_profit:.2f}"})


@app.post("/used", response_class=HTMLResponse)
async def get_used_data(request: Request):
     return templates.TemplateResponse("used.html", {"request": request, "title": "Calculadora de Preços Barbante"})


if __name__ == "__main__":
    import uvicorn

    webbrowser.open("http://localhost:8004/home")

    uvicorn.run("main:app", host="localhost", port=8004, reload=True)
