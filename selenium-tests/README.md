# Smart Temple E2E Selenium Test Suite & Excel Report

This directory contains the Selenium E2E web frontend test suite and the generated test management report containing **320 detailed test cases** and an **Executive Summary**.

## 📁 Folder Structure

```
selenium-tests/
├── tests/
│   └── login-tests.js                # Selenium E2E automated test suite for login & auth
├── generate_excel.py                 # Python generator script for the Excel report
├── login_test_cases_summary.xlsx     # Generated Excel Sheet (Executive Summary + 320 Test Cases)
├── package.json                      # Node.js dependencies & test scripts
└── README.md                         # Documentation
```

## 🧪 Automated Test Suite (`tests/login-tests.js`)

The `login-tests.js` script provides an automated Selenium WebDriver test suite implementing the Page Object Model (POM).

### Key Features:
- Page Object Pattern (`LoginPage` class)
- Cross-browser support (Chrome, Firefox, Headless mode)
- Explicit waits (`until.elementLocated`)
- Screenshot capture on test failure
- Comprehensive logging and execution metric recording
- Test coverage across:
  - Form rendering and UI element checks
  - Successful user, admin, devotee, and priest logins
  - Field validation & error handling
  - Password visibility toggle and masking checks

### Execution:
```bash
# Run Selenium tests
npm test
# or directly
node tests/login-tests.js
```

## 📊 Test Management Excel Report (`login_test_cases_summary.xlsx`)

The generated Excel workbook contains two styled sheets:

1. **Executive Summary Sheet**:
   - Executive Metadata & Environment info
   - Category Breakdown Table (Functional, Security, UI/UX, Session, MFA, RBAC, Performance, Accessibility, etc.)
   - High-level KPIs and Pass Rate Metrics

2. **Test Cases Details Sheet (320 Test Cases)**:
   - **Fields**: `Test Case ID`, `Module`, `Category`, `Test Case Title`, `Description & Objective`, `Pre-conditions`, `Test Steps`, `Test Data`, `Expected Result`, `Actual Result`, `Priority`, `Severity`, `Status`, `Automation Reference`, `Exec Time (ms)`.
   - **Categories Covered**:
     - Basic Authentication (TC-LOG-001 to TC-LOG-025)
     - Input Validation & Field Rules (TC-LOG-026 to TC-LOG-065)
     - Password Security & Masking (TC-LOG-066 to TC-LOG-095)
     - Multi-Factor Authentication (MFA / 2FA) (TC-LOG-096 to TC-LOG-130)
     - Role-Based Access Control (RBAC) (TC-LOG-131 to TC-LOG-165)
     - Session Management & Cookies (TC-LOG-166 to TC-LOG-200)
     - OWASP Security & Defense (TC-LOG-201 to TC-LOG-240)
     - Account Recovery & Reset (TC-LOG-241 to TC-LOG-270)
     - Anti-Bot & Captcha Defense (TC-LOG-271 to TC-LOG-290)
     - Responsive UI & Viewports (TC-LOG-291 to TC-LOG-305)
     - Accessibility & Performance (TC-LOG-306 to TC-LOG-320)

### Regenerating the Excel Report:
```bash
python generate_excel.py
```
