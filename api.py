from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, declarative_base
from fastapi.middleware.cors import CORSMiddleware

# Database setup
DATABASE_URL = "sqlite:///./data.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Models
class FormEntry(Base):
    __tablename__ = "form_entries"
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    pharmacy_name = Column(String, nullable=False)
    business_address = Column(String, nullable=False)
    drugs = relationship("DrugDetail", back_populates="form_entry")

class DrugDetail(Base):
    __tablename__ = "drug_details"
    id = Column(Integer, primary_key=True, index=True)
    form_entry_id = Column(Integer, ForeignKey("form_entries.id"), nullable=False)
    brand_name = Column(String, nullable=False)
    dosage_form = Column(String, nullable=False)
    strength = Column(String, nullable=False)
    notes = Column(String, nullable=False)  # Replaced generic_designation with notes
    manufacturer_name = Column(String, nullable=False)
    manufacturer_address = Column(String, nullable=False)
    form_entry = relationship("FormEntry", back_populates="drugs")

Base.metadata.create_all(bind=engine)

# FastAPI setup
app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (change this to specific domains in production)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Pydantic models for request validation
class DrugDetailModel(BaseModel):
    brand_name: str
    dosage_form: str
    strength: str
    notes: str  # Replaced generic_designation with notes
    manufacturer_name: str
    manufacturer_address: str

class FormEntryModel(BaseModel):
    full_name: str
    pharmacy_name: str
    business_address: str
    drug_details: list[DrugDetailModel]

# Routes
@app.post("/submit")
def submit_form(entry: FormEntryModel):
    db = SessionLocal()
    form_entry = FormEntry(
        full_name=entry.full_name,
        pharmacy_name=entry.pharmacy_name,
        business_address=entry.business_address,
    )
    db.add(form_entry)
    db.commit()
    db.refresh(form_entry)

    for drug in entry.drug_details:
        drug_detail = DrugDetail(
            form_entry_id=form_entry.id,
            brand_name=drug.brand_name,
            dosage_form=drug.dosage_form,
            strength=drug.strength,
            notes=drug.notes,  # Replaced generic_designation with notes
            manufacturer_name=drug.manufacturer_name,
            manufacturer_address=drug.manufacturer_address,
        )
        db.add(drug_detail)

    db.commit()
    db.close()
    return {"message": "Form submitted successfully!"}

@app.get("/entries")
def get_entries():
    db = SessionLocal()
    entries = db.query(FormEntry).all()
    result = []
    for entry in entries:
        drugs = db.query(DrugDetail).filter(DrugDetail.form_entry_id == entry.id).all()
        drug_details = [
            {
                "brand_name": drug.brand_name,
                "dosage_form": drug.dosage_form,
                "strength": drug.strength,
                "notes": drug.notes,
                "manufacturer_name": drug.manufacturer_name,  # Ensure this is included
                "manufacturer_address": drug.manufacturer_address,
            }
            for drug in drugs
        ]
        result.append({
            "id": entry.id,
            "full_name": entry.full_name,
            "pharmacy_name": entry.pharmacy_name,
            "business_address": entry.business_address,
            "drug_details": drug_details,
        })
    db.close()
    return result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)