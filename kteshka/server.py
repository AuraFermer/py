from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Currency Converter API")


RATES = {
    "USD": 1.0,
    "EUR": 0.85,
    "RUB": 90.0,
    "GBP": 0.75,
    "JPY": 140.0,
    "CNY": 7.2
}

class ConversionRequest(BaseModel):
    amount: float
    from_currency: str
    to_currency: str

@app.post("/convert")
def convert_currency(req: ConversionRequest):
    
    if req.amount < 0:
        raise HTTPException(status_code=400, detail="Сумма не может быть отрицательной")
    
    
    supported = ", ".join(RATES.keys())
    if req.from_currency not in RATES or req.to_currency not in RATES:
        raise HTTPException(status_code=400, detail=f"Неизвестная валюта. Поддерживаются: {supported}")
    
   
    cross_rate = RATES[req.to_currency] / RATES[req.from_currency]
    result = req.amount * cross_rate
    
    return {
        "amount": req.amount,
        "from": req.from_currency,
        "to": req.to_currency,
        "rate": round(cross_rate, 4),
        "result": round(result, 2)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)