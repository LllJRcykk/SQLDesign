async function login() {
    const eid = document.getElementById("eid").value.trim();
    const epas = document.getElementById("epas").value.trim();

    if (!eid || !epas) {
        showAlert("请输入员工编号和密码", "danger");
        return;
    }

    try {
        const res = await fetch(`${API_BASE}/employees/login`, {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({ eid, epas })
        });
        const data = await res.json();

        if (data.success) {
            localStorage.setItem("loginUser", JSON.stringify(data.data));
            window.location.href = "employee.html";
        } else {
            showAlert(data.msg, "danger");
        }
    } catch (e) {
        showAlert("登录请求失败：" + e, "danger");
    }
}