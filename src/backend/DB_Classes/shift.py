from pydantic import BaseModel

class Shift (BaseModel):
    def __init__(
            self,
            shift_id: int,
            location_name: str,
            staff_id: int,
            in_time: str,
            hours: float,
            absent: bool,
            auth: bool,
            reason: str,
            /, **data) -> None:
        super().__init__(**data)

        self.shift_id: int = shift_id
        self.location_name = location_name
        self.staff_id = staff_id
        self.in_time = in_time
        self.hours = hours
        self.absent = absent
        self.auth = auth
        self.reason = reason