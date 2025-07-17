"""
Fake Jack‑Henry core‑banking API
Runs on http://localhost:8001
"""
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

app = FastAPI(title="JackHenryLite")

# --- toy data --------------------------------------------------------------
DATA = {
    "123": {"balance": 182_345.67, "name": "Operating", "type": "DDA"},
    "987": {"balance": 45_200.11,  "name": "Reserve",   "type": "Savings"},
}

class BalanceReq(BaseModel):
    account: str

# --- endpoint --------------------------------------------------------------
@app.post("/balance")
def get_balance(req: BalanceReq):
    return {"account": req.account,
            **DATA.get(req.account, {"error": "not found"})}

# --- entry‑point -----------------------------------------------------------
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001, reload=True)
