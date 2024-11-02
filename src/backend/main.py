# Libs
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import datetime
import asyncio

# Self made modules
import DB_Manager.manager as dbm
import DB_Classes.employee as emp

import Logging.logging as logger

app = FastAPI()

origins = [
    "http://127.0.0.1:8000",
    "http://localhost:3000",
    "http://localhost:63342",
    "http://127.0.0.1:8000/clock-in/",
    "http://127.0.0.1:8000/clock-out/",
]

# Add the CORS middleware to the FastAPI app
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,            # Allow specific origins
    allow_credentials=True,            # Allow cookies to be sent in requests
    allow_methods=["*"],               # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],               # Allow all headers
)


db = dbm.DBManager("Database.db")

id_to_location = {
    "111111" : "Notts", # Nottingham
    "Notts" : "Notts",

    "111112" : "Leics", # Leicester
    "Leics" : "Leics",

    "111113" : "Doncs", # Doncaster
    "Doncs" : "Doncs"
}

@app.get("/")
async def root():
    return {
        "status" : "ok",
        "message": f"Server running on {origins[0]}",
        "Teapot" : 418
    }

@app.post("/clock-in/")
async def clock_in(shift: emp.EmployeeSimple):
    now = datetime.datetime.now()

    res = db.set_shift_start(shift.shift_id, id_to_location[shift.location_id], now)
    if not res:
        logger.logFail(f"Statement could not be executed")
        return {
            "status" : "failed"
        }

    logger.logSuccess(f"Time ({now}) sent to database, updated field and commited")

    return {
        "status" : "finished"
    }


@app.post("/clock-out/")
async def clock_out(shift: emp.EmployeeSimple):
    now = datetime.datetime.now()

    res = db.clock_out(now, shift.employee_id, shift.shift_id)
    if not res:
        logger.logFail(f"Statement could not be executed")
        return {
            "status" : "failed"
        }

    logger.logSuccess(f"Time ({now}) updated in database, total time worked changed")

    return {
        "status" : "finished"
    }

if __name__ == "__main__":
    db.DO_NOT_USE_create_DB()
    db.DO_NOT_USE_add_test_data()

    #thing = emp.Employee(m_staff_id=1, m_name="John Test", m_hour_rate=12.5, m_total_pay=0)
    #asyncio.run(clock_in(thing))
    pass