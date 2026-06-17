function showAlert(message, type = "success") {
    const alertBox = document.getElementById("alertBox");
    if (!alertBox) {
        alert(message);
        return;
    }
    alertBox.innerHTML = `
        <div class="alert alert-${type} alert-dismissible fade show" role="alert">
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `;
}

function logout() {
    localStorage.removeItem("loginUser");
    window.location.href = "index.html";
}

function checkLogin() {
    const user = localStorage.getItem("loginUser");
    if (!user) {
        alert("请先登录");
        window.location.href = "index.html";
    }
}

function renderNavbar(title) {
    const navbar = document.getElementById("navbar");
    if (!navbar) return;

    navbar.innerHTML = `
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
      <div class="container-fluid">
        <a class="navbar-brand" href="#">超市进销存管理系统</a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarsExample07">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarsExample07">
          <ul class="navbar-nav me-auto mb-2 mb-lg-0">
            <li class="nav-item"><a class="nav-link ${title === 'employee' ? 'active' : ''}" href="employee.html">员工管理</a></li>
            <li class="nav-item"><a class="nav-link ${title === 'customer' ? 'active' : ''}" href="customer.html">客户管理</a></li>
            <li class="nav-item"><a class="nav-link ${title === 'good' ? 'active' : ''}" href="good.html">商品管理</a></li>
            <li class="nav-item"><a class="nav-link ${title === 'purchase' ? 'active' : ''}" href="purchase.html">采购管理</a></li>
            <li class="nav-item"><a class="nav-link ${title === 'statistics' ? 'active' : ''}" href="statistics.html">统计查询</a></li>
            <li class="nav-item"><a class="nav-link ${title === 'export' ? 'active' : ''}" href="export.html">数据导出</a></li>
          </ul>
          <button class="btn btn-light btn-sm" onclick="logout()">退出登录</button>
        </div>
      </div>
    </nav>
    `;
}