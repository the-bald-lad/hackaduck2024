from pydantic import BaseModel

class Employee(BaseModel):
    m_staff_id: int
    m_name: str
    m_hour_rate: float
    m_total_pay: float

    def __init__(self, **data):
        super().__init__(**data)

class EmployeeSimple(BaseModel):
    employee_id: str
    location_id: str
    shift_id: str
