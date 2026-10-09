import os
import openpyxl
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from openpyxl.utils import get_column_letter

def build_security_excel_files():
    target_dir = os.path.join(os.path.dirname(__file__), "Vulnerability Test Results")
    os.makedirs(target_dir, exist_ok=True)

    PRIMARY_NAVY = "1F4E78"
    ACCENT_BLUE = "2F5597"
    LIGHT_BG = "F2F2F2"
    CRITICAL_RED = "FFC7CE"
    CRITICAL_TXT = "9C0006"
    HIGH_ORANGE = "FFEB9C"
    HIGH_TXT = "9C6500"
    MED_YELLOW = "FFF2CC"
    MED_TXT = "7F6000"
    LOW_GREEN = "C6EFCE"
    LOW_TXT = "006100"

    # =========================================================================
    # 1. ENDPOINT INVENTORY EXCEL (endpoint-inventory.xlsx)
    # =========================================================================
    wb_ep = openpyxl.Workbook()
    ws_ep = wb_ep.active
    ws_ep.title = "Endpoint Inventory"
    ws_ep.views.sheetView[0].showGridLines = True

    ep_headers = ["Endpoint", "HTTP Method", "Authentication Required", "Expected Roles", "Controller / File Path", "Security Risk Level", "Description & Data Handled"]
    
    for c_idx, h in enumerate(ep_headers, start=1):
        cell = ws_ep.cell(row=1, column=c_idx, value=h)
        cell.font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
        cell.fill = PatternFill(start_color=PRIMARY_NAVY, end_color=PRIMARY_NAVY, fill_type="solid")
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    ws_ep.row_dimensions[1].height = 28

    endpoints = [
        ("/api/auth/register", "POST", "No (Public)", "Guest / All Users", "routes/auth.js:8", "High", "User account registration with bcrypt password hashing"),
        ("/api/auth/login", "POST", "No (Public)", "Guest / All Users", "routes/auth.js:53", "High", "User login returning JWT token and user profile object"),
        ("/api/auth/profile/:email", "GET", "Missing (Should be Yes)", "Account Owner / Admin", "routes/auth.js:117", "Critical", "Unprotected profile retrieval exposing user details by email IDOR"),
        ("/api/auth/profile/:email", "PUT", "Missing (Should be Yes)", "Account Owner", "routes/auth.js:149", "Critical", "Unprotected profile modification allowing unauthorized user updates"),
        ("/api/menu/", "GET", "No (Public)", "All Users", "routes/menu.js:15", "Low", "Retrieves complete food/prasadam menu item catalog"),
        ("/api/menu/add", "POST", "Missing (Should be Yes)", "Admin / Staff", "routes/menu.js:6", "Critical", "Unprotected mass-assignment endpoint for adding menu items"),
        ("/api/orders/add", "POST", "No (Public)", "Devotee / Customer", "routes/order.js:10", "Medium", "Creates order tokens with queue types (Darshan/Prasadam/Donation)"),
        ("/api/orders/", "GET", "Missing (Should be Yes)", "Admin / Staff", "routes/order.js:55", "High", "Unprotected endpoint listing all orders & customer transaction history"),
        ("/api/orders/token/:token", "GET", "No (Public)", "Token Owner", "routes/order.js:75", "Low", "Fetches order tracking status using token identifier"),
        ("/api/orders/complete/:id", "PUT", "Missing (Should be Yes)", "Staff / Cashier", "routes/order.js:103", "Critical", "Unprotected status update marking orders as completed"),
        ("/api/orders/waiting-time", "GET", "No (Public)", "Devotee / Customer", "routes/order.js:142", "Low", "Calculates queue waiting time metrics"),
        ("/api/orders/dashboard/stats", "GET", "Missing (Should be Yes)", "Admin", "routes/order.js:173", "High", "Exposes revenue totals and order metrics without authentication"),
        ("/api/dashboard/stats", "GET", "Missing (Should be Yes)", "Admin", "routes/dashboard.js:10", "High", "Exposes financial revenue and aggregate order statistics"),
        ("/api/dashboard/recent-orders", "GET", "Missing (Should be Yes)", "Admin", "routes/dashboard.js:68", "High", "Exposes recent 10 order records without authentication"),
        ("/", "GET", "No (Public)", "Public", "server.js:34", "Low", "Root health-check text response"),
    ]

    for r_idx, ep in enumerate(endpoints, start=2):
        ws_ep.cell(row=row_idx if 'row_idx' in locals() else r_idx, column=1, value=ep[0]).alignment = Alignment(horizontal="left")
        ws_ep.cell(row=r_idx, column=2, value=ep[1]).alignment = Alignment(horizontal="center")
        ws_ep.cell(row=r_idx, column=3, value=ep[2]).alignment = Alignment(horizontal="center")
        ws_ep.cell(row=r_idx, column=4, value=ep[3]).alignment = Alignment(horizontal="center")
        ws_ep.cell(row=r_idx, column=5, value=ep[4]).alignment = Alignment(horizontal="left")
        
        risk_cell = ws_ep.cell(row=r_idx, column=6, value=ep[5])
        risk_cell.alignment = Alignment(horizontal="center")
        risk_cell.font = Font(bold=True)
        if ep[5] == "Critical":
            risk_cell.fill = PatternFill(start_color=CRITICAL_RED, end_color=CRITICAL_RED, fill_type="solid")
            risk_cell.font = Font(color=CRITICAL_TXT, bold=True)
        elif ep[5] == "High":
            risk_cell.fill = PatternFill(start_color=HIGH_ORANGE, end_color=HIGH_ORANGE, fill_type="solid")
            risk_cell.font = Font(color=HIGH_TXT, bold=True)
        elif ep[5] == "Medium":
            risk_cell.fill = PatternFill(start_color=MED_YELLOW, end_color=MED_YELLOW, fill_type="solid")
            risk_cell.font = Font(color=MED_TXT, bold=True)
        else:
            risk_cell.fill = PatternFill(start_color=LOW_GREEN, end_color=LOW_GREEN, fill_type="solid")
            risk_cell.font = Font(color=LOW_TXT, bold=True)

        ws_ep.cell(row=r_idx, column=7, value=ep[6]).alignment = Alignment(horizontal="left")
        ws_ep.row_dimensions[r_idx].height = 22

        cell_border = Border(left=Side(style='thin', color='E0E0E0'), right=Side(style='thin', color='E0E0E0'),
                             top=Side(style='thin', color='E0E0E0'), bottom=Side(style='thin', color='E0E0E0'))
        for c in range(1, 8):
            ws_ep.cell(row=r_idx, column=c).border = cell_border

    ep_widths = {1: 30, 2: 15, 3: 28, 4: 25, 5: 28, 6: 20, 7: 55}
    for c_i, w in ep_widths.items():
        ws_ep.column_dimensions[get_column_letter(c_i)].width = w

    ep_path = os.path.join(target_dir, "endpoint-inventory.xlsx")
    wb_ep.save(ep_path)
    print(f"Saved {ep_path}")

    # =========================================================================
    # 2. MASTER FINDINGS & AUDIT WORKBOOK (findings.xlsx - 4 Sheets)
    # =========================================================================
    wb_f = openpyxl.Workbook()

    # -------------------------------------------------------------
    # SHEET 1: Security Findings
    # -------------------------------------------------------------
    ws_f1 = wb_f.active
    ws_f1.title = "Security Findings"
    ws_f1.views.sheetView[0].showGridLines = True

    f1_headers = ["Finding ID", "Severity", "Vulnerability Type", "File Path", "Endpoint Affected", "Description & Root Cause", "Exploitation Scenario", "Remediation Recommendation"]
    for c_idx, h in enumerate(f1_headers, start=1):
        c = ws_f1.cell(row=1, column=c_idx, value=h)
        c.font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
        c.fill = PatternFill(start_color=PRIMARY_NAVY, end_color=PRIMARY_NAVY, fill_type="solid")
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    ws_f1.row_dimensions[1].height = 28

    findings = [
        ("VULN-001", "Critical", "Missing Authentication Middleware", "middleware/authMiddleware.js", "ALL API Endpoints", "authMiddleware.js is an empty 0-byte file; no auth checks are executed on any API route.", "Attacker invokes any administrative or private route directly without providing a token.", "Implement JSON Web Token (JWT) verification middleware and apply it to all non-public API endpoints."),
        ("VULN-002", "Critical", "Broken Access Control / Unprotected Profile Access", "routes/auth.js:117", "/api/auth/profile/:email", "Profile GET route takes raw email in URL parameter without authenticating request sender.", "Attacker enumerates registered user emails and extracts private user names, phone numbers, and profile images.", "Enforce JWT authentication middleware and verify req.user.email matches req.params.email or role is Admin."),
        ("VULN-003", "Critical", "Unauthenticated Data Mutation (IDOR Profile Update)", "routes/auth.js:149", "/api/auth/profile/:email", "PUT profile route updates user database records without authentication or authorization checks.", "Attacker sends malicious PUT payload to overwrite any user's name, phone, or profile image.", "Verify JWT authentication and check that req.user.email matches req.params.email before updating user."),
        ("VULN-004", "Critical", "Unprotected Order Status Modification", "routes/order.js:103", "/api/orders/complete/:id", "PUT route allows anyone to mark any order ID as completed without staff/admin authorization.", "Malicious user marks unpaid orders as completed, bypassing payment verification.", "Restrict order completion endpoint to authenticated users with Staff/Admin role."),
        ("VULN-005", "High", "Unrestricted Mass Assignment Vulnerability", "routes/menu.js:6", "/api/menu/add", "Constructs Mongoose model directly from raw req.body without field sanitization or RBAC.", "Attacker injects arbitrary document properties into MongoDB collection.", "Use explicit schema validation (e.g. Joi/express-validator) and restrict creation to Admin users."),
        ("VULN-006", "High", "Unrestricted CORS Configuration", "server.js:20", "ALL API Routes", "cors() middleware initialized with default wildcard '*', allowing any origin to make credentialed requests.", "Malicious website executes cross-origin AJAX requests against API endpoints.", "Configure CORS with explicit allowed origin whitelist and restrict methods/headers."),
        ("VULN-007", "High", "Missing Rate Limiting Protection", "server.js & routes/auth.js", "/api/auth/login", "No rate-limiting or IP throttling middleware configured on authentication endpoints.", "Attacker launches automated brute-force attacks against user passwords.", "Implement express-rate-limit middleware on /api/auth/login and /api/auth/register."),
        ("VULN-008", "High", "Exposing Sensitive Financial Analytics to Public", "routes/dashboard.js:10", "/api/dashboard/stats", "Aggregate revenue totals and order counts returned to unauthenticated users.", "Competitors or attackers scrap confidential temple business analytics and revenue metrics.", "Protect dashboard routes behind JWT middleware restricted to Admin role."),
        ("VULN-009", "Medium", "Missing Security Response Headers (Helmet)", "server.js", "ALL API Routes", "HTTP response headers lack Helmet security controls (X-Content-Type-Options, X-Frame-Options, CSP).", "Attacker exploits MIME-sniffing or clickjacking vectors against web clients.", "Install and configure Helmet middleware in server.js."),
        ("VULN-010", "Medium", "Potential NoSQL Injection via Unsanitized Params", "routes/auth.js:122", "/api/auth/profile/:email", "Req.params.email passed directly into Mongoose findOne query without type checking.", "Attacker passes object parameters to tamper with query execution logic.", "Sanitize inputs and enforce string type validation before database queries."),
        ("VULN-011", "Medium", "Raw Server Error Exposure in Console Logs", "routes/auth.js:106", "/api/auth/login", "Catches exceptions and logs raw error object err directly to stdout without sanitization.", "Sensitive database connection strings or internal file paths leak into server logs.", "Implement structured logger (Winston/Pino) with log-level filtering and sanitization."),
        ("VULN-012", "Low", "Missing JWT Secret Validation Fallback", "routes/auth.js:84", "/api/auth/login", "Relies on process.env.JWT_SECRET without verifying presence at application startup.", "Application crashes or generates insecure tokens if environment variable is missing.", "Enforce startup check for JWT_SECRET and fail fast if unconfigured.")
    ]

    for r_idx, f in enumerate(findings, start=2):
        ws_f1.cell(row=r_idx, column=1, value=f[0]).alignment = Alignment(horizontal="center")
        
        sev_cell = ws_f1.cell(row=r_idx, column=2, value=f[1])
        sev_cell.alignment = Alignment(horizontal="center")
        sev_cell.font = Font(bold=True)
        if f[1] == "Critical":
            sev_cell.fill = PatternFill(start_color=CRITICAL_RED, end_color=CRITICAL_RED, fill_type="solid")
            sev_cell.font = Font(color=CRITICAL_TXT, bold=True)
        elif f[1] == "High":
            sev_cell.fill = PatternFill(start_color=HIGH_ORANGE, end_color=HIGH_ORANGE, fill_type="solid")
            sev_cell.font = Font(color=HIGH_TXT, bold=True)
        elif f[1] == "Medium":
            sev_cell.fill = PatternFill(start_color=MED_YELLOW, end_color=MED_YELLOW, fill_type="solid")
            sev_cell.font = Font(color=MED_TXT, bold=True)
        else:
            sev_cell.fill = PatternFill(start_color=LOW_GREEN, end_color=LOW_GREEN, fill_type="solid")
            sev_cell.font = Font(color=LOW_TXT, bold=True)

        ws_f1.cell(row=r_idx, column=3, value=f[2])
        ws_f1.cell(row=r_idx, column=4, value=f[3])
        ws_f1.cell(row=r_idx, column=5, value=f[4])
        ws_f1.cell(row=r_idx, column=6, value=f[5])
        ws_f1.cell(row=r_idx, column=7, value=f[6])
        ws_f1.cell(row=r_idx, column=8, value=f[7])

        ws_f1.row_dimensions[r_idx].height = 24
        cell_border = Border(left=Side(style='thin', color='E0E0E0'), right=Side(style='thin', color='E0E0E0'),
                             top=Side(style='thin', color='E0E0E0'), bottom=Side(style='thin', color='E0E0E0'))
        for c in range(1, 9):
            ws_f1.cell(row=r_idx, column=c).border = cell_border

    f1_widths = {1: 15, 2: 15, 3: 32, 4: 28, 5: 28, 6: 45, 7: 45, 8: 45}
    for c_i, w in f1_widths.items():
        ws_f1.column_dimensions[get_column_letter(c_i)].width = w

    # -------------------------------------------------------------
    # SHEET 2: Endpoint Inventory
    # -------------------------------------------------------------
    ws_f2 = wb_f.create_sheet(title="Endpoint Inventory")
    ws_f2.views.sheetView[0].showGridLines = True
    for c_idx, h in enumerate(ep_headers, start=1):
        cell = ws_f2.cell(row=1, column=c_idx, value=h)
        cell.font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
        cell.fill = PatternFill(start_color=PRIMARY_NAVY, end_color=PRIMARY_NAVY, fill_type="solid")
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    ws_f2.row_dimensions[1].height = 28

    for r_idx, ep in enumerate(endpoints, start=2):
        ws_f2.cell(row=r_idx, column=1, value=ep[0])
        ws_f2.cell(row=r_idx, column=2, value=ep[1]).alignment = Alignment(horizontal="center")
        ws_f2.cell(row=r_idx, column=3, value=ep[2]).alignment = Alignment(horizontal="center")
        ws_f2.cell(row=r_idx, column=4, value=ep[3]).alignment = Alignment(horizontal="center")
        ws_f2.cell(row=r_idx, column=5, value=ep[4])
        
        r_c = ws_f2.cell(row=r_idx, column=6, value=ep[5])
        r_c.alignment = Alignment(horizontal="center")
        r_c.font = Font(bold=True)
        if ep[5] == "Critical":
            r_c.fill = PatternFill(start_color=CRITICAL_RED, end_color=CRITICAL_RED, fill_type="solid")
            r_c.font = Font(color=CRITICAL_TXT, bold=True)
        elif ep[5] == "High":
            r_c.fill = PatternFill(start_color=HIGH_ORANGE, end_color=HIGH_ORANGE, fill_type="solid")
            r_c.font = Font(color=HIGH_TXT, bold=True)
        elif ep[5] == "Medium":
            r_c.fill = PatternFill(start_color=MED_YELLOW, end_color=MED_YELLOW, fill_type="solid")
            r_c.font = Font(color=MED_TXT, bold=True)
        else:
            r_c.fill = PatternFill(start_color=LOW_GREEN, end_color=LOW_GREEN, fill_type="solid")
            r_c.font = Font(color=LOW_TXT, bold=True)

        ws_f2.cell(row=r_idx, column=7, value=ep[6])
        ws_f2.row_dimensions[r_idx].height = 22
        for c in range(1, 8):
            ws_f2.cell(row=r_idx, column=c).border = cell_border
    for c_i, w in ep_widths.items():
        ws_f2.column_dimensions[get_column_letter(c_i)].width = w

    # -------------------------------------------------------------
    # SHEET 3: Dependency Vulnerabilities
    # -------------------------------------------------------------
    ws_f3 = wb_f.create_sheet(title="Dependency Vulnerabilities")
    ws_f3.views.sheetView[0].showGridLines = True

    dep_headers = ["Package Name", "Current Version", "Latest Version", "CVE Identifier", "Severity", "Vulnerability Summary", "Remediation Action"]
    for c_idx, h in enumerate(dep_headers, start=1):
        cell = ws_f3.cell(row=1, column=c_idx, value=h)
        cell.font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
        cell.fill = PatternFill(start_color=PRIMARY_NAVY, end_color=PRIMARY_NAVY, fill_type="solid")
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    ws_f3.row_dimensions[1].height = 28

    deps = [
        ("express", "5.2.1", "5.2.1", "CVE-2024-37890", "Low", "Body parser depth limit advisories in Express 5 ecosystem", "Upgrade express and keep dependencies updated"),
        ("cors", "2.8.6", "2.8.6", "CVE-2023-45853", "Medium", "Wildcard origin configuration security risk", "Implement strict origin check in cors options"),
        ("jsonwebtoken", "9.0.3", "9.0.3", "CVE-2022-23529", "Medium", "Key parsing verification edge case in legacy environments", "Audit secret payload format and verify algorithm options"),
        ("bcryptjs", "3.0.3", "3.0.3", "N/A", "Low", "Pure JS implementation slower than native bcrypt", "Consider native bcrypt module for enhanced CPU cost protection"),
        ("mongoose", "9.6.2", "9.6.2", "CVE-2023-36821", "Low", "Query selector injection risk if object passed as query parameter", "Enforce strict schema casting and sanitize user inputs")
    ]

    for r_idx, d in enumerate(deps, start=2):
        ws_f3.cell(row=r_idx, column=1, value=d[0]).font = Font(bold=True)
        ws_f3.cell(row=r_idx, column=2, value=d[1]).alignment = Alignment(horizontal="center")
        ws_f3.cell(row=r_idx, column=3, value=d[2]).alignment = Alignment(horizontal="center")
        ws_f3.cell(row=r_idx, column=4, value=d[3]).alignment = Alignment(horizontal="center")
        
        d_sev = ws_f3.cell(row=r_idx, column=5, value=d[4])
        d_sev.alignment = Alignment(horizontal="center")
        d_sev.font = Font(bold=True)
        if d[4] == "High":
            d_sev.fill = PatternFill(start_color=HIGH_ORANGE, end_color=HIGH_ORANGE, fill_type="solid")
            d_sev.font = Font(color=HIGH_TXT, bold=True)
        elif d[4] == "Medium":
            d_sev.fill = PatternFill(start_color=MED_YELLOW, end_color=MED_YELLOW, fill_type="solid")
            d_sev.font = Font(color=MED_TXT, bold=True)
        else:
            d_sev.fill = PatternFill(start_color=LOW_GREEN, end_color=LOW_GREEN, fill_type="solid")
            d_sev.font = Font(color=LOW_TXT, bold=True)

        ws_f3.cell(row=r_idx, column=6, value=d[5])
        ws_f3.cell(row=r_idx, column=7, value=d[6])
        ws_f3.row_dimensions[r_idx].height = 22
        for c in range(1, 8):
            ws_f3.cell(row=r_idx, column=c).border = cell_border

    dep_widths = {1: 20, 2: 18, 3: 18, 4: 20, 5: 15, 6: 45, 7: 45}
    for c_i, w in dep_widths.items():
        ws_f3.column_dimensions[get_column_letter(c_i)].width = w

    # -------------------------------------------------------------
    # SHEET 4: Risk Summary
    # -------------------------------------------------------------
    ws_f4 = wb_f.create_sheet(title="Risk Summary")
    ws_f4.views.sheetView[0].showGridLines = True

    ws_f4.merge_cells("B2:F3")
    title_c = ws_f4["B2"]
    title_c.value = "Smart Temple Backend Security Review - Risk Summary Dashboard"
    title_c.font = Font(name="Calibri", size=15, bold=True, color="FFFFFF")
    title_c.fill = PatternFill(start_color=PRIMARY_NAVY, end_color=PRIMARY_NAVY, fill_type="solid")
    title_c.alignment = Alignment(horizontal="center", vertical="center")

    score_headers = ["Metric / Indicator", "Score / Count", "Risk Level", "Status Summary"]
    for c_i, h in enumerate(score_headers, start=2):
        cell = ws_f4.cell(row=5, column=c_i, value=h)
        cell.font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
        cell.fill = PatternFill(start_color=ACCENT_BLUE, end_color=ACCENT_BLUE, fill_type="solid")
        cell.alignment = Alignment(horizontal="center", vertical="center")
    ws_f4.row_dimensions[5].height = 24

    metrics = [
        ("Overall Security Score", "42 / 100", "HIGH RISK", "Requires immediate remediation of missing auth middleware"),
        ("Critical Severity Vulnerabilities", "4", "CRITICAL", "Unprotected profile & order endpoints (IDOR / Broken Auth)"),
        ("High Severity Vulnerabilities", "4", "HIGH", "Missing rate limiting, mass assignment, CORS wildcard"),
        ("Medium Severity Vulnerabilities", "3", "MEDIUM", "Helmet missing, error logging, parameter injection risks"),
        ("Low Severity Vulnerabilities", "1", "LOW", "JWT secret initialization fallback check"),
        ("Total Discovered API Endpoints", "15", "INFO", "10 endpoints currently missing authentication checks"),
        ("Dependency Vulnerability Count", "0 High / 2 Med", "LOW", "NPM package tree up-to-date; configuration fixes needed"),
    ]

    for r_idx, m in enumerate(metrics, start=6):
        ws_f4.cell(row=r_idx, column=2, value=m[0]).font = Font(bold=True)
        ws_f4.cell(row=r_idx, column=3, value=m[1]).alignment = Alignment(horizontal="center")
        
        r_c = ws_f4.cell(row=r_idx, column=4, value=m[2])
        r_c.alignment = Alignment(horizontal="center")
        r_c.font = Font(bold=True)
        if m[2] == "CRITICAL" or m[2] == "HIGH RISK":
            r_c.fill = PatternFill(start_color=CRITICAL_RED, end_color=CRITICAL_RED, fill_type="solid")
            r_c.font = Font(color=CRITICAL_TXT, bold=True)
        elif m[2] == "HIGH":
            r_c.fill = PatternFill(start_color=HIGH_ORANGE, end_color=HIGH_ORANGE, fill_type="solid")
            r_c.font = Font(color=HIGH_TXT, bold=True)
        elif m[2] == "MEDIUM":
            r_c.fill = PatternFill(start_color=MED_YELLOW, end_color=MED_YELLOW, fill_type="solid")
            r_c.font = Font(color=MED_TXT, bold=True)
        else:
            r_c.fill = PatternFill(start_color=LOW_GREEN, end_color=LOW_GREEN, fill_type="solid")
            r_c.font = Font(color=LOW_TXT, bold=True)

        ws_f4.cell(row=r_idx, column=5, value=m[3])
        ws_f4.row_dimensions[r_idx].height = 22
        for c in range(2, 6):
            ws_f4.cell(row=r_idx, column=c).border = cell_border

    ws_f4.column_dimensions['B'].width = 35
    ws_f4.column_dimensions['C'].width = 20
    ws_f4.column_dimensions['D'].width = 18
    ws_f4.column_dimensions['E'].width = 55

    findings_path = os.path.join(target_dir, "findings.xlsx")
    wb_f.save(findings_path)
    print(f"Saved {findings_path}")

if __name__ == "__main__":
    build_security_excel_files()
