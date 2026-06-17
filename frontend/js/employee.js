function initPage() {
    checkLogin();
    renderNavbar("employee");
    loadEmployees();
}

function getEmployeeFormData() {
    return {
        eid: document.getElementById("eid").value.trim(),
        ename: document.getElementById("ename").value.trim(),
        epas: document.getElementById("epas").value.trim(),
        elevel: document.getElementById("elevel").value,
        etel_phone: document.getElementById("etel_phone").value.trim(),
        esalary: parseFloat(document.getElementById("esalary").value || 0),
        other: document.getElementById("other").value.trim()
    };
}

function fillEmployeeForm(item) {
    document.getElementById("eid").value = item.eid || "";
    document.getElementById("ename").value = item.ename || "";
    document.getElementById("epas").value = item.epas || "";
    document.getElementById("elevel").value = item.elevel || "20";
    document.getElementById("etel_phone").value = item.etel_phone || "";
    document.getElementById("esalary").value = item.esalary || 0;
    document.getElementById("other").value = item.other || "";
}

async function loadEmployees() {
    const res = await fetch(`${API_BASE}/employees/`);
    const data = await res.json();
    const tbody = document.querySelector("#employeeTable tbody");
    tbody.innerHTML = "";

    data.data.forEach(item => {
        const tr = document.createElement("tr");
        tr.style.cursor = "pointer";
        tr.onclick = () => fillEmployeeForm(item);
        tr.innerHTML = `
            <td>${item.eid}</td>
            <td>${item.ename}</td>
            <td>${item.epas}</td>
            <td>${item.elevel}</td>
            <td>${item.etel_phone}</td>
            <td>${item.esalary}</td>
            <td>${item.other || ""}</td>
        `;
        tbody.appendChild(tr);
    });
}

async function addEmployee() {
    const body = getEmployeeFormData();
    const res = await fetch(`${API_BASE}/employees/`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(body)
    });
    const data = await res.json();
    showAlert(data.msg, data.success ? "success" : "danger");
    if (data.success) loadEmployees();
}

async function updateEmployee() {
    const body = getEmployeeFormData();
    const res = await fetch(`${API_BASE}/employees/${body.eid}`, {
        method: "PUT",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(body)
    });
    const data = await res.json();
    showAlert(data.msg, data.success ? "success" : "danger");
    if (data.success) loadEmployees();
}

async function deleteEmployee() {
    const eid = document.getElementById("eid").value.trim();
    if (!eid) {
        showAlert("请输入员工编号", "danger");
        return;
    }
    const res = await fetch(`${API_BASE}/employees/${eid}`, {
        method: "DELETE"
    });
    const data = await res.json();
    showAlert(data.msg, data.success ? "success" : "danger");
    if (data.success) loadEmployees();
}

async function searchByName() {
    const keyword = document.getElementById("searchName").value.trim();
    const res = await fetch(`${API_BASE}/employees/search/name?keyword=${encodeURIComponent(keyword)}`);
    const data = await res.json();
    const tbody = document.querySelector("#employeeTable tbody");
    tbody.innerHTML = "";
    data.data.forEach(item => {
        const tr = document.createElement("tr");
        tr.onclick = () => fillEmployeeForm(item);
        tr.innerHTML = `
            <td>${item.eid}</td>
            <td>${item.ename}</td>
            <td>${item.epas}</td>
            <td>${item.elevel}</td>
            <td>${item.etel_phone}</td>
            <td>${item.esalary}</td>
            <td>${item.other || ""}</td>
        `;
        tbody.appendChild(tr);
    });
}