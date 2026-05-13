const API_URL = "http://localhost:8000";

const token = localStorage.getItem("token");
const role = localStorage.getItem("role");

// ======================
// LOGIN
// ======================

const loginForm = document.getElementById("loginForm");

if (loginForm) {

    loginForm.addEventListener("submit", async (e) => {

        e.preventDefault();

        const username =
            document.getElementById("username").value;

        const password =
            document.getElementById("password").value;

        const formData = new URLSearchParams();

        formData.append("username", username);
        formData.append("password", password);

        try {

            const response = await fetch(
                `${API_URL}/auth/login`,
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                        "application/x-www-form-urlencoded"
                    },

                    body: formData
                }
            );

            const data = await response.json();

            if (response.ok) {

                localStorage.setItem(
                    "token",
                    data.access_token
                );

                localStorage.setItem(
                    "role",
                    data.role
                );

                document.getElementById("message").innerHTML =
                `
                    <span class="text-success">
                        Login successful
                    </span>
                `;

                setTimeout(() => {

                    window.location.href =
                        "dashboard.html";

                }, 1000);

            } else {

                document.getElementById("message").innerHTML =
                `
                    <span class="text-danger">
                        ${data.detail}
                    </span>
                `;
            }

        } catch (error) {

            console.log(error);

            document.getElementById("message").innerHTML =
            `
                <span class="text-danger">
                    Server Error
                </span>
            `;
        }

    });

}


// ======================
// REGISTER
// ======================

const registerForm =
    document.getElementById("registerForm");

if (registerForm) {

    registerForm.addEventListener(
        "submit",
        async (e) => {

            e.preventDefault();

            const username =
                document.getElementById(
                    "regUsername"
                ).value;

            const email =
                document.getElementById(
                    "regEmail"
                ).value;

            const password =
                document.getElementById(
                    "regPassword"
                ).value;

            const role =
                document.getElementById(
                    "regRole"
                ).value;

            try {

                const response = await fetch(
                    `${API_URL}/auth/register`,
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                            "application/json"
                        },

                        body: JSON.stringify({
                            username,
                            email,
                            password,
                            role
                        })
                    }
                );

                const data = await response.json();

                if (response.ok) {

                    document.getElementById(
                        "registerMessage"
                    ).innerHTML =
                    `
                        <span class="text-success">
                            Registration successful
                        </span>
                    `;

                    setTimeout(() => {

                        window.location.href =
                            "login.html";

                    }, 1000);

                } else {

                    document.getElementById(
                        "registerMessage"
                    ).innerHTML =
                    `
                        <span class="text-danger">
                            ${data.detail}
                        </span>
                    `;
                }

            } catch (error) {

                console.log(error);

                document.getElementById(
                    "registerMessage"
                ).innerHTML =
                `
                    <span class="text-danger">
                        Server Error
                    </span>
                `;
            }

        }
    );
}


// ======================
// LOGOUT
// ======================

function logout() {

    localStorage.removeItem("token");
    localStorage.removeItem("role");

    window.location.href = "login.html";
}


// ======================
// DASHBOARD LOAD
// ======================

if (window.location.pathname.includes("dashboard.html")) {

    loadMetrics();
    loadStudents();

    if (role === "student") {

        const addSection =
            document.getElementById(
                "addStudentSection"
            );

        if (addSection) {
            addSection.style.display = "none";
        }
    }
}


// ======================
// ADD STUDENT
// ======================

const studentForm =
    document.getElementById("studentForm");

if (studentForm) {

    studentForm.addEventListener(
        "submit",
        async (e) => {

            e.preventDefault();

            const name =
                document.getElementById(
                    "studentName"
                ).value;

            const department =
                document.getElementById(
                    "studentDepartment"
                ).value;

            const gpa =
                document.getElementById(
                    "studentGpa"
                ).value;

            try {

                const response = await fetch(
                    `${API_URL}/students/`,
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                            "application/json",

                            "Authorization":
                            `Bearer ${token}`
                        },

                        body: JSON.stringify({
                            name,
                            department,
                            gpa: parseFloat(gpa)
                        })
                    }
                );

                if (response.ok) {

                    studentForm.reset();

                    loadStudents();

                } else {

                    const data =
                        await response.json();

                    alert(data.detail);
                }

            } catch (error) {

                console.log(error);
            }

        }
    );
}


// ======================
// DELETE STUDENT
// ======================

async function deleteStudent(id) {

    const confirmDelete = confirm(
        "Are you sure?"
    );

    if (!confirmDelete) return;

    try {

        const response = await fetch(
            `${API_URL}/students/${id}`,
            {
                method: "DELETE",

                headers: {
                    "Authorization":
                    `Bearer ${token}`
                }
            }
        );

        if (response.ok) {

            loadStudents();

        } else {

            alert("Delete failed");
        }

    } catch (error) {

        console.log(error);
    }
}


// ======================
// EDIT STUDENT
// ======================

async function editStudent(
    id,
    oldName,
    oldDepartment,
    oldGpa
) {

    const name = prompt(
        "Enter new name",
        oldName
    );

    const department = prompt(
        "Enter new department",
        oldDepartment
    );

    const gpa = prompt(
        "Enter new GPA",
        oldGpa
    );

    if (!name || !department || !gpa)
        return;

    try {

        const response = await fetch(
            `${API_URL}/students/${id}`,
            {
                method: "PUT",

                headers: {
                    "Content-Type":
                    "application/json",

                    "Authorization":
                    `Bearer ${token}`
                },

                body: JSON.stringify({
                    name,
                    department,
                    gpa: parseFloat(gpa)
                })
            }
        );

        if (response.ok) {

            loadStudents();

        } else {

            alert("Update failed");
        }

    } catch (error) {

        console.log(error);
    }
}


// ======================
// LOAD METRICS
// ======================

async function loadMetrics() {

    try {

        const response = await fetch(
            `${API_URL}/metrics`
        );

        const data = await response.json();

        document.getElementById(
            "totalRequests"
        ).innerText =
            data.metrics.total_requests;

        document.getElementById(
            "errors"
        ).innerText =
            data.metrics.errors;

        document.getElementById(
            "responseTime"
        ).innerText =
            data.metrics.response_time;

    } catch (error) {

        console.log(error);
    }
}


// ======================
// LOAD STUDENTS
// ======================

async function loadStudents() {

    try {

        const response = await fetch(
            `${API_URL}/students/`,
            {
                headers: {
                    "Authorization":
                    `Bearer ${token}`
                }
            }
        );

        const students =
            await response.json();

        const table =
            document.getElementById(
                "studentsTable"
            );

        table.innerHTML = "";

        students.forEach(student => {

            table.innerHTML += `
                <tr>

                    <td>${student.id}</td>

                    <td>${student.name}</td>

                    <td>${student.department}</td>

                    <td>${student.gpa}</td>

                    <td>

                        ${
                            role === "admin"

                            ?

                            `
                            <button
                                class="btn btn-warning btn-sm"
                                onclick="editStudent(
                                    ${student.id},
                                    '${student.name}',
                                    '${student.department}',
                                    ${student.gpa}
                                )"
                            >
                                Edit
                            </button>

                            <button
                                class="btn btn-danger btn-sm"
                                onclick="deleteStudent(${student.id})"
                            >
                                Delete
                            </button>
                            `

                            :

                            `
                            <span class="text-muted">
                                Read Only
                            </span>
                            `
                        }

                    </td>

                </tr>
            `;
        });

    } catch (error) {

        console.log(error);
    }
}


// ======================
// GLOBAL FUNCTIONS
// ======================

window.deleteStudent = deleteStudent;
window.editStudent = editStudent;