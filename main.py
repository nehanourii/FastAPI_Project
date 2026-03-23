from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field
from typing import Optional, List
import math

app = FastAPI()

# =========================
# Q1 - Root
# =========================
@app.get("/")
def home():
    return {"message": "Welcome to MediCare Clinic"}


# =========================
# Q2 - Doctors Data
# =========================
doctors = [
    {"id": 1, "name": "Dr. Asha", "specialization": "Cardiologist", "fee": 500, "experience_years": 10, "is_available": True},
    {"id": 2, "name": "Dr. Rahul", "specialization": "Dermatologist", "fee": 300, "experience_years": 5, "is_available": True},
    {"id": 3, "name": "Dr. Meena", "specialization": "Pediatrician", "fee": 400, "experience_years": 8, "is_available": False},
    {"id": 4, "name": "Dr. John", "specialization": "General", "fee": 200, "experience_years": 3, "is_available": True},
    {"id": 5, "name": "Dr. Arun", "specialization": "Cardiologist", "fee": 600, "experience_years": 15, "is_available": True},
    {"id": 6, "name": "Dr. Neha", "specialization": "Dermatologist", "fee": 350, "experience_years": 7, "is_available": False},
]

@app.get("/doctors")
def get_doctors():
    available_count = sum(1 for d in doctors if d["is_available"])
    return {
        "doctors": doctors,
        "total": len(doctors),
        "available_count": available_count
    }


# =========================
# Q5 - Doctors Summary
# =========================
@app.get("/doctors/summary")
def doctors_summary():
    total = len(doctors)
    available = sum(1 for d in doctors if d["is_available"])
    most_exp = max(doctors, key=lambda x: x["experience_years"])
    cheapest = min(doctors, key=lambda x: x["fee"])

    specialization_count = {}
    for d in doctors:
        spec = d["specialization"]
        specialization_count[spec] = specialization_count.get(spec, 0) + 1

    return {
        "total_doctors": total,
        "available": available,
        "most_experienced": most_exp["name"],
        "cheapest_fee": cheapest["fee"],
        "specialization_count": specialization_count
    }


# =========================
# Q3 - Get Doctor by ID
# =========================
@app.get("/doctors/{doctor_id}")
def get_doctor(doctor_id: int):
    for d in doctors:
        if d["id"] == doctor_id:
            return d
    raise HTTPException(status_code=404, detail="Doctor not found")


# =========================
# Q4 - Appointments Init
# =========================
appointments = []
appt_counter = 1

@app.get("/appointments")
def get_appointments():
    return {"appointments": appointments, "total": len(appointments)}


# =========================
# Q6 - Pydantic Model
# =========================
class AppointmentRequest(BaseModel):
    patient_name: str = Field(..., min_length=2)
    doctor_id: int = Field(..., gt=0)
    date: str = Field(..., min_length=8)
    reason: str = Field(..., min_length=5)
    appointment_type: str = "in-person"
    senior_citizen: bool = False


# =========================
# Q7 - Helpers
# =========================
def find_doctor(doctor_id):
    for d in doctors:
        if d["id"] == doctor_id:
            return d
    return None

def calculate_fee(base_fee, appointment_type, senior=False):
    if appointment_type == "video":
        fee = base_fee * 0.8
    elif appointment_type == "emergency":
        fee = base_fee * 1.5
    else:
        fee = base_fee

    final_fee = fee
    if senior:
        final_fee = fee * 0.85

    return int(fee), int(final_fee)


# =========================
# Q8 + Q9 - Create Appointment
# =========================
@app.post("/appointments")
def create_appointment(req: AppointmentRequest):
    global appt_counter

    doctor = find_doctor(req.doctor_id)
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")

    if not doctor["is_available"]:
        raise HTTPException(status_code=400, detail="Doctor not available")

    base_fee = doctor["fee"]
    original_fee, final_fee = calculate_fee(base_fee, req.appointment_type, req.senior_citizen)

    appointment = {
        "appointment_id": appt_counter,
        "patient": req.patient_name,
        "doctor": doctor["name"],
        "doctor_id": doctor["id"],
        "date": req.date,
        "type": req.appointment_type,
        "original_fee": original_fee,
        "final_fee": final_fee,
        "status": "scheduled"
    }

    appointments.append(appointment)
    appt_counter += 1

    doctor["is_available"] = False

    return appointment


# =========================
# Q10 - Filter Doctors
# =========================
@app.get("/doctors/filter")
def filter_doctors(
    specialization: Optional[str] = None,
    max_fee: Optional[int] = None,
    min_experience: Optional[int] = None,
    is_available: Optional[bool] = None
):
    result = doctors

    if specialization is not None:
        result = [d for d in result if d["specialization"] == specialization]

    if max_fee is not None:
        result = [d for d in result if d["fee"] <= max_fee]

    if min_experience is not None:
        result = [d for d in result if d["experience_years"] >= min_experience]

    if is_available is not None:
        result = [d for d in result if d["is_available"] == is_available]

    return {"results": result, "count": len(result)}


# =========================
# Q11 - Add Doctor
# =========================
class NewDoctor(BaseModel):
    name: str = Field(..., min_length=2)
    specialization: str = Field(..., min_length=2)
    fee: int = Field(..., gt=0)
    experience_years: int = Field(..., gt=0)
    is_available: bool = True


@app.post("/doctors", status_code=201)
def add_doctor(doc: NewDoctor):
    for d in doctors:
        if d["name"].lower() == doc.name.lower():
            raise HTTPException(status_code=400, detail="Doctor already exists")

    new_doc = doc.dict()
    new_doc["id"] = len(doctors) + 1
    doctors.append(new_doc)

    return new_doc


# =========================
# Q12 - Update Doctor
# =========================
@app.put("/doctors/{doctor_id}")
def update_doctor(doctor_id: int, fee: Optional[int] = None, is_available: Optional[bool] = None):
    doctor = find_doctor(doctor_id)
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")

    if fee is not None:
        doctor["fee"] = fee

    if is_available is not None:
        doctor["is_available"] = is_available

    return doctor


# =========================
# Q13 - Delete Doctor
# =========================
@app.delete("/doctors/{doctor_id}")
def delete_doctor(doctor_id: int):
    doctor = find_doctor(doctor_id)
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")

    for a in appointments:
        if a["doctor_id"] == doctor_id and a["status"] == "scheduled":
            raise HTTPException(status_code=400, detail="Doctor has active appointments")

    doctors.remove(doctor)
    return {"message": "Doctor deleted"}


# =========================
# Q14 + Q15 - Appointment Status
# =========================
def find_appointment(aid):
    for a in appointments:
        if a["appointment_id"] == aid:
            return a
    return None


@app.post("/appointments/{aid}/confirm")
def confirm(aid: int):
    appt = find_appointment(aid)
    if not appt:
        raise HTTPException(404)
    appt["status"] = "confirmed"
    return appt


@app.post("/appointments/{aid}/cancel")
def cancel(aid: int):
    appt = find_appointment(aid)
    if not appt:
        raise HTTPException(404)

    appt["status"] = "cancelled"

    doctor = find_doctor(appt["doctor_id"])
    if doctor:
        doctor["is_available"] = True

    return appt


@app.post("/appointments/{aid}/complete")
def complete(aid: int):
    appt = find_appointment(aid)
    if not appt:
        raise HTTPException(404)

    appt["status"] = "completed"
    return appt


@app.get("/appointments/active")
def active_appointments():
    return [a for a in appointments if a["status"] in ["scheduled", "confirmed"]]


@app.get("/appointments/by-doctor/{doctor_id}")
def by_doctor(doctor_id: int):
    return [a for a in appointments if a["doctor_id"] == doctor_id]


# =========================
# Q16 - Search Doctors
# =========================
@app.get("/doctors/search")
def search_doctors(keyword: str):
    result = [d for d in doctors if keyword.lower() in d["name"].lower()
              or keyword.lower() in d["specialization"].lower()]

    if not result:
        return {"message": "No doctors found"}

    return {"results": result, "total_found": len(result)}


# =========================
# Q17 - Sort Doctors
# =========================
@app.get("/doctors/sort")
def sort_doctors(sort_by: str = "fee"):
    if sort_by not in ["fee", "name", "experience_years"]:
        raise HTTPException(400, "Invalid sort field")

    return sorted(doctors, key=lambda x: x[sort_by])


# =========================
# Q18 - Pagination Doctors
# =========================
@app.get("/doctors/page")
def paginate(page: int = 1, limit: int = 3):
    start = (page - 1) * limit
    end = start + limit
    total_pages = math.ceil(len(doctors) / limit)

    return {
        "page": page,
        "total_pages": total_pages,
        "data": doctors[start:end]
    }


# =========================
# Q19 - Appointments Search/Sort/Page
# =========================
@app.get("/appointments/search")
def search_appt(patient_name: str):
    return [a for a in appointments if patient_name.lower() in a["patient"].lower()]


@app.get("/appointments/sort")
def sort_appt(sort_by: str = "final_fee"):
    return sorted(appointments, key=lambda x: x.get(sort_by, 0))


@app.get("/appointments/page")
def page_appt(page: int = 1, limit: int = 2):
    start = (page - 1) * limit
    end = start + limit
    return appointments[start:end]


# =========================
# Q20 - Browse Doctors
# =========================
@app.get("/doctors/browse")
def browse(
    keyword: Optional[str] = None,
    sort_by: str = "fee",
    order: str = "asc",
    page: int = 1,
    limit: int = 4
):
    result = doctors

    if keyword:
        result = [d for d in result if keyword.lower() in d["name"].lower()
                  or keyword.lower() in d["specialization"].lower()]

    reverse = order == "desc"
    result = sorted(result, key=lambda x: x[sort_by], reverse=reverse)

    total = len(result)
    start = (page - 1) * limit
    end = start + limit

    return {
        "total": total,
        "page": page,
        "results": result[start:end]
    }