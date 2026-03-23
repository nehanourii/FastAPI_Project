# 🏥 Medical Appointment System (FastAPI)

## 📌 Overview

The Medical Appointment System is a RESTful API built using FastAPI that helps manage doctors, schedule appointments, and track consultation activities. It simulates a real-world clinic system where patients can book appointments with doctors based on availability, specialization, and consultation type.

---

## 🎯 Features

* 👨‍⚕️ Manage doctors (add, update, delete, view)
* 📅 Book and manage appointments
* 🔍 Search and filter doctors
* 💰 Automatic consultation fee calculation
* 📊 Summary and analytics of doctors
* 🔄 Appointment workflow (schedule → confirm → complete/cancel)
* 📄 Pagination, sorting, and advanced browsing

---

## ⚙️ Tech Stack

* Python
* FastAPI
* Pydantic (for validation)
* Uvicorn (server)

---

## 🧩 Modules

### 1. Doctor Management

* Add new doctors
* Update doctor details (fee, availability)
* Delete doctors (with validation)
* View all doctors and individual doctor details

### 2. Appointment Management

* Book appointments with doctors
* Validate doctor availability
* Track appointment status:

  * Scheduled
  * Confirmed
  * Completed
  * Cancelled

### 3. Fee Calculation

* In-person consultation → 100% fee
* Video consultation → 80% fee
* Emergency consultation → 150% fee
* Senior citizens → Additional 15% discount

### 4. Search & Filter

* Search doctors by name or specialization
* Filter by:

  * Specialization
  * Maximum fee
  * Experience
  * Availability

### 5. Sorting & Pagination

* Sort doctors by:

  * Fee
  * Name
  * Experience
* Paginate results for better performance

### 6. Advanced Features

* Combined browsing (search + sort + pagination)
* Appointment search, sorting, and pagination
* Doctor summary insights

---

## 🔁 API Workflow

1. View doctors
2. Select doctor based on specialization/availability
3. Book appointment
4. Confirm appointment
5. Complete or cancel appointment

---

## 📌 Sample Response

```json
{
  "message": "Appointment scheduled successfully",
  "appointment": {
    "appointment_id": 1,
    "patient": "Rahul",
    "doctor": "Dr. Asha",
    "status": "scheduled"
  }
}
```

---

## 🚀 How to Run

```bash
uvicorn main:app --reload
```

Then open:
👉 http://127.0.0.1:8000/docs

---

## 🎓 Learning Outcome

* REST API development using FastAPI
* Data validation with Pydantic
* CRUD operations
* API design and structuring
* Real-world backend logic implementation

---

## 📌 Conclusion

This project demonstrates how a clinic can efficiently manage doctors and appointments using a backend system. It ensures proper scheduling, reduces manual work, and provides a scalable solution for healthcare management.

---
