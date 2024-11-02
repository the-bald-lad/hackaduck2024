import sqlite3
import os
from datetime import datetime
from xmlrpc.client import DateTime

con = sqlite3.connect("../backend/Database.db")
cur = con.cursor()

def addShift():
    loc       = input("Enter location:")
    staffID   = input("Enter Staff ID:")
    year      = input("Enter Shift year:")
    month     = input("Enter Shift month:")
    day       = input("Enter Shift day:")
    hour      = input("Enter Start Hour:")
    minute    = input("Enter Start Minute:")
    shiftTime = year + "," + month + "," + day + "," + hour + "," + minute
    len       = int(input("Enter Length of Shift(in hours):"))
    ftime     = str(int(hour) + len)
    endTime   = year + "," + month + "," + day + "," + ftime + "," + minute
    last      = 0

    for i in cur.execute("SELECT shiftID FROM Shift"):
        last = i[0]

    last += 1
    cur.execute("INSERT INTO Shift(shiftID,locationName,staffID,desiredin,desiredout) VALUES (?,?,?,?,?)",(last,loc,staffID,shiftTime,endTime))
    con.commit()

def manageShift():
    ID = int(input("Enter Shift ID:"))
    change = str(input("What Should Be Changed:"))
    new = str(input("What Should Be The New Value:"))
    updateDB('Shift',change,new,'shiftID',ID)

def deleteShift():
    ID = int(input("Enter Shift ID to delete:"))
    cur.execute("DELETE FROM Shift WHERE shiftID=?",(ID,))
    con.commit()

def addEmployee():
    name = str(input("Enter Employee Name:"))
    rate = float(input("Enter Pay Rate of Employee:"))
    for i in cur.execute("SELECT staffID FROM Employee"):
        last = i[0]
    last += 1
    cur.execute("INSERT INTO Employee(staffID,name,hourRate,totalpay) VALUES(?,?,?,0)",(last,name,rate))
    con.commit()

def manageEmployee():
    ID = int(input("Enter Employee ID:"))
    change = str(input("What Should Be Changed:"))
    new = str(input("What Should Be The New Value:"))
    updateDB('Employee', change, new, 'staffID', ID)

def deleteEmployee():
    ID = int(input("Enter Staff ID to delete:"))
    cur.execute("DELETE FROM Employee WHERE staffID=?", (ID,))
    con.commit()

def viewShifts():
    print("What would you like to view?")
    print("1: Entire view")
    print("2: Sort by staff ID")
    print("3: Sort by location name")
    print("4: Sort by absent")
    answer = str(input("Please enter choice:"))
    if answer == "1":
        print("ID|location|staffID|Shift Time|hrs|Start|End|Absent|Authorised|Reason")
        for row in cur.execute("SELECT * FROM Shift"):
            print(row)
    if answer == "2":
        id = int(input("Enter Staff ID:"))
        print("ID|location|staffID|Shift Time|hrs|Start|End|Absent|Authorised|Reason")
        for row in cur.execute("SELECT * FROM Shift WHERE staffID = ?", (id)):
            print(row)
    if answer == "3":
        loc = int(input("Enter location name"))
        print("ID|location|staffID|Shift Time|hrs|Start|End|Absent|Authorised|Reason")
        for row in cur.execute("SELECT * FROM Shift WHERE locationName = ? SORT BY staffID", (loc)):
            print(row)
    if answer == "4":
        print("ID|location|staffID|Shift Time|hrs|Start|End|Absent|Authorised|Reason")
        for row in cur.execute("SELECT * FROM Shift WHERE absent = 1 SORT BY staffID"):
            print(row)

def viewEmployees():
    print("What would you like to view?")
    print("1: Sort by staff ID view")
    print("2: Sort by total pay")
    print("3: Sort by hourly pay")
    answer = str(input("Please enter choice:"))
    print("StaffID|Name|PayPerHour|Total")
    if answer == "1":
        for row in cur.execute("SELECT * FROM Employee ORDER BY staffID"):
            print(row)
    if answer == "2":
        for row in cur.execute("SELECT * FROM Employee ORDER BY totalPay"):
            print(row)
    if answer == "3":
        for row in cur.execute("SELECT * FROM Employee ORDER BY hourlyPay"):
            print(row)

def updateDB(table,change,new,condition,searchVal):
    cur.execute(f"UPDATE {table} SET {change} = ? WHERE {condition} = ?",(new, searchVal))
    con.commit()

def timesheet():
    for row in cur.execute("SELECT staffID, name FROM Employee"):
        timesheet = open(row[1] +" - " + row[0] + ".txt", "w")
        timesheet.write("ShiftID     Start Time              End Time")
        for col in cur.execute("SELECT shiftID, desiredin, desiredout FROM Shift WHERE staffID = ?",(row[0])):
            desin = col[0][11:13] + ":" + col[0][14:16] + "-" + col[0][8:10] + "/" + col[0][5:7] + "/" + col[0][0:4]
            desout = col[1][11:13] + ":" + col[1][14:16] + "-" + col[1][8:10] + "/" + col[1][5:7] + "/" + col[1][0:4]
            timesheet.write(col[0] + "\t\t\t" + desin + "\t\t" + desout + "\n")

        timesheet.close()



def main():
    print("Welcome to Admin Management")
    print("Which function would you like to run?")
    print("1: Add shift")
    print("2: Edit Shift")
    print("3: Remove shift")
    print("4: Add employee")
    print("5: Manage employee")
    print("6: Remove employee")
    print("7: View Shifts")
    print("8: View Employees")
    print("9: View Payroll")
    print("10: Output Timesheet")
    print("11: Exit")
    answer = int(input("Enter your choice: "))

    if answer == 1:
        addShift()
    if answer == 2:
        manageShift()
    if answer == 3:
        deleteShift()
    if answer == 4:
        addEmployee()
    if answer == 5:
        manageEmployee()
    if answer == 6:
        deleteEmployee()
    if answer == 7:
        viewShifts()
    if answer == 8:
        viewEmployees()
    if answer == 9:
        for row in cur.execute("SELECT staffID, name, totalPay FROM Employee "):
            print(row)
    if answer == 10:
        timesheet()
    if answer == 11:
        print("Thank you. Have a good day!")
        exit()


if __name__ == "__main__":
    while True:
        main()