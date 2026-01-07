from fastapi import FastAPI
from app.api import dashboard, insights, optimization, ab_testing

app = FastAPI(title="AI Marketing Platform")

app.include_router(dashboard)
app.include_router(insights)
app.include_router(optimization)
app.include_router(ab_testing)



@app.get("/")
def root():
    return {"status": "API running successfully"}



