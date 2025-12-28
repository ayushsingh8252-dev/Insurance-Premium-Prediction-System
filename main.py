from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Annotated
import pickle
import pandas as pd

# ---------------- City Tiers ----------------
tier_1_cities = [
    "Mumbai", "Delhi", "Bangalore", "Chennai",
    "Kolkata", "Hyderabad", "Pune"
]

tier_2_cities = [
    "Jaipur", "Chandigarh", "Indore", "Lucknow",
    "Patna", "Ranchi", "Coimbatore", "Bhopal"
]

# ---------------- App ----------------
app = FastAPI()

# ---------------- Load Model ----------------
with open("model (1).pkl", "rb") as f:
    model = pickle.load(f)

# ---------------- Input Schema ----------------
class UserInput(BaseModel):
    age: Annotated[int, Field(gt=0, lt=120)]
    weight: Annotated[float, Field(gt=0)]
    height: Annotated[float, Field(gt=0)]
    income_lpa: Annotated[float, Field(ge=0)]
    smoker: bool
    city: str
    occupation: str

    @computed_field
    @property
    def bmi(self) -> float:
        return self.weight / ((self.height / 100) ** 2)

    @computed_field
    @property
    def lifestyle_risk(self) -> str:
        if self.smoker and self.bmi > 30:
            return "High"
        elif self.smoker or self.bmi > 27:
            return "Medium"
        return "Low"

    @computed_field
    @property
    def age_group(self) -> str:
        if self.age < 18:
            return "Young"
        elif self.age <= 45:
            return "Adult"
        elif self.age <= 65:
            return "Middle"
        return "Senior"

    @computed_field
    @property
    def city_tier(self) -> int:
        if self.city in tier_1_cities:
            return 1
        elif self.city in tier_2_cities:
            return 2
        return 3

    @computed_field
    @property
    def occupation_clean(self) -> str:
        return self.occupation.strip().lower()

# ---------------- Prediction ----------------
@app.post("/predict")
def predict(data: UserInput):

    input_df = pd.DataFrame([{
        "bmi": data.bmi,
        "age_group": data.age_group,
        "lifestyle_risk": data.lifestyle_risk,
        "city_tier": data.city_tier,
        "income_lpa": data.income_lpa,
        "occupation": data.occupation_clean
    }])

    prediction = model.predict(input_df)[0]   # "Low" / "Medium" / "High"

    return JSONResponse(
        status_code=200,
        content={"predicted_premium": prediction}
    )
