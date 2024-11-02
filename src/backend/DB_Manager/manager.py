import sqlite3 as sql
from datetime import datetime

class DBManager:
    def __init__(self, path: str) -> None:
        if path == "": return

        self.__connection = sql.connect(path)
        self.__cursor = self.__connection.cursor()

    def DO_NOT_USE_create_DB(self) -> None:
        """
        DO NOT USE UNLESS YOU KNOW WHAT YOU ARE DOING
        I SWEAR TO WHATEVER GOD YOU WANT TO BELIEVE IN,
        I WILL FIND YOU BEFORE THIS MESSAGE DOES IF YOU USE THIS FUNCTION
        :return:
        """
        self.__cursor.execute(
            "CREATE TABLE Employee("
            "staffID INT PRIMARY KEY, "
            "name VARCHAR(30), "
            "hourRate DECIMAL(3,2), "
            "totalPay DECIMAL(6,2))")
        self.__cursor.execute(
            "CREATE TABLE Shift("
            "shiftID INT PRIMARY KEY, "
            "locationName VARCHAR(30), "
            "staffID INT, "
            "inTime CHAR(16), "
            "hours DECIMAL(2,2), "
            "desiredin CHAR(16),"
            "desiredout CHAR(16),"
            "absent BOOLEAN DEFAULT TRUE, "
            "authorised BOOLEAN DEFAULT FALSE, "
            "reason VARCHAR(500), "
            "CONSTRAINT shift_fk_staffID FOREIGN KEY (staffID) REFERENCES User(staffID) ON DELETE CASCADE)")

    def DO_NOT_USE_add_test_data(self):
        self.__cursor.execute("INSERT INTO Employee (staffID, name, hourRate, totalPay) "
                              "VALUES (1, 'John Test', 12.5, 0.0)")

        self.__cursor.execute("INSERT INTO Employee (staffID, name, hourRate, totalPay) "
                              "VALUES (2, 'Simon Test', 16.5, 0.0)")

        self.__connection.commit()

    def set_shift_start(self, staff_id: str, location: str, now: datetime) -> bool:
        #Find shift based off location and employee info in db, if shift found add the now time to clock in time

        curdate = str(now.date())
        curtime = str(now.time())

        now = curdate[0:4] + "," + curdate[5:7] + "," + curdate[8:10] + "," + curtime[0:2] + "," + curtime[3:5]

        statement: str = ("UPDATE Shift "
                          "SET "
                          f"inTime = '{now}' "
                          f"WHERE staffID = '{staff_id}' AND locationName = '{location}';")

        self.__cursor.execute(statement)
        self.__connection.commit()

        try:
            self.__cursor.execute(statement)
            self.__connection.commit()
        except sql.ProgrammingError:
            return False
        return True

    def clock_out(self, now: datetime, staff_id: str, shift_id: str) -> bool:
        time1 = self.__cursor.execute("SELECT inTime FROM Shift WHERE shiftID = ?;", shift_id)

        time1 = time1.fetchone()[0]

        time2 = datetime(int(time1[0:4]), int(time1[5:7]), int(time1[8:10]), int(time1[11:13]), int(time1[14:16]))

        diff = now - time2

        diff= diff.total_seconds()/3600

        diff = round(diff, 4)

        try:
            self.__cursor.execute("UPDATE Shift SET hours = ? WHERE shiftID = ?;",
                                  (diff, shift_id))
            self.__cursor.execute("UPDATE Employee SET totalpay = totalpay + (hourRate * ?) WHERE staffID = ?;",
                                  (diff, staff_id))
            self.__connection.commit()
        except sql.ProgrammingError:
            return False
        return True