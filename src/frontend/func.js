let logged_in = false
let clocked_in = false

const base_api_url = "http://127.0.0.1:8000"

const clock_in_url = `${base_api_url}/clock-in/`
const clock_out_url = `${base_api_url}/clock-out/`

function checkCheckedIn() {
    if (clocked_in) {
        clock_out_api()
        clocked_in = false
        document.getElementById("cib").innerHTML = "Clock in"
    } else {
        clock_in_api()
        clocked_in = true
        document.getElementById("cib").innerHTML = "Clock out"
    }
}

function updateLoginDetails() {
    if (logged_in === false) {
        let a = document.getElementById("eid").value
        let b = document.getElementById("lid").value
        let c = document.getElementById("sid").value
        localStorage.setItem("employee_id", a)
        localStorage.setItem("location_id", b)
        localStorage.setItem("shift_id", c)
        logged_in = true
    }
    else {
        localStorage.removeItem("employee_id")
        localStorage.removeItem("location_id")
        localStorage.removeItem("shift_id")
        logged_in = false 
    }
    updatePage()
}
function updatePage() {
    if (logged_in) {
        document.getElementById("icb").innerHTML = "logout"
        document.getElementById("checkinoutid").style.display = "flex"
    } else {
        document.getElementById("icb").innerHTML = "login"
        document.getElementById("checkinoutid").style.display = "none"
    }

    if (clocked_in) {
        document.getElementById("cib").innerHTML = "Clock out"
    } else {
        document.getElementById("cib").innerHTML = "Clock in"
    }
}

function boilerplateRubbishForAPI(employee_id, location_id, shift_id) {
    console.log(`eid ${employee_id}, lid ${location_id}, sid ${shift_id}`)

    if (!employee_id || !location_id || !shift_id) {
        console.log("Failed at reading values")
        throw new Error('Some values are null');
    }

    const data = {
        "employee_id" : employee_id,
        "location_id" : location_id,
        "shift_id" : shift_id
    }

    return {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    }
}

function clock_in_api() {
    let employee_id = localStorage.getItem("employee_id")
    let location_id = localStorage.getItem("location_id")
    let shift_id = localStorage.getItem("shift_id")

    console.log("Clocking in")

    let request_options= boilerplateRubbishForAPI(employee_id, location_id, shift_id)

    fetch(clock_in_url, request_options).then(response=> {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json
    }).then(data => {
        console.log("SUCCESSFUL!")
    })
}

function clock_out_api() {
    let employee_id = localStorage.getItem("employee_id")
    let location_id = localStorage.getItem("location_id")
    let shift_id = localStorage.getItem("shift_id")

    console.log("Clocking out")

    let request_options = boilerplateRubbishForAPI(employee_id, location_id, shift_id)

    fetch(clock_out_url, request_options).then(response=> {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json
    }).then(data => {
        console.log("SUCCESSFUL!")
    })
}

document.addEventListener("DOMContentLoaded", function() {
    let eid = localStorage.getItem("employee_id")
    let lid = localStorage.getItem("location_id")
    let sid = localStorage.getItem("shift_id")

    if (eid !== null) {
        document.getElementById("eid").value = eid
    }
    if (lid !== null) {
        document.getElementById("lid").value = lid
    }
    if (sid !== null) {
        document.getElementById("sid").value = sid
    }

    if (eid !== null && lid !== null && sid !== null) {
        logged_in = true
    }

    updatePage()

    document.getElementById("cib").addEventListener("click", checkCheckedIn)
    
    document.getElementById("icb").addEventListener("click", updateLoginDetails)
});

