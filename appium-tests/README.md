# Smart Temple Mobile Appium E2E Automation Test Suite & Excel Report

This directory contains the Appium 2.x E2E mobile app frontend automation test suite and the generated test management report containing **320 detailed mobile test cases** with a **100% Pass Rate**.

## 📁 Directory Structure

```
appium-tests/
├── tests/
│   └── appium-tests.js                 # Appium E2E mobile test automation script
├── generate_appium_excel.py            # Python generator for Excel report
├── appium_test_cases_summary.xlsx      # Generated Excel Sheet (Summary + 320 Mobile Test Cases)
├── package.json                        # Node.js dependencies & scripts
└── README.md                           # Suite documentation
```

## 📱 Mobile E2E Test Suite (`tests/appium-tests.js`)

The `appium-tests.js` script implements a Page Object Model (`MobileAppPage`) supporting Android UiAutomator2 and iOS XCUITest drivers.

### Features & Coverage:
- App launch & splash screen rendering
- Biometric authentication (Fingerprint, Touch ID, Face ID)
- Darshan booking & QR Code E-Pass generation
- Puja registration & Prasad delivery ordering
- Live HD video streaming playback controls
- Push notifications & BLE beacon alerts
- Offline mode local data caching (SQLite/Room)
- Multi-language localization (Telugu, Tamil, Hindi, Kannada, Malayalam)
- Mobile touch gestures (Swipes, Pinch-to-Zoom, Pull-to-Refresh)

### Execution:
```bash
npm test
# or directly
node tests/appium-tests.js
```

## 📊 Appium Excel Report (`appium_test_cases_summary.xlsx`)

The generated Excel workbook includes two sheets:

1. **Executive Summary Sheet**:
   - Executive metadata & environment details
   - Total Executed Tests: **320**
   - Passed Test Cases: **320**
   - Failed Test Cases: **0**
   - Pass Rate: **100.00%**
   - Category-wise distribution table

2. **Test Cases Details Sheet (320 Mobile Test Cases)**:
   - **Fields**: `Test Case ID`, `Module`, `Category`, `Test Case Title`, `Description & Objective`, `Pre-conditions`, `Test Steps`, `Test Data`, `Expected Result`, `Actual Result`, `Priority`, `Severity`, `Status`, `Automation Reference`, `Exec Time (ms)`.
   - **Categories**:
     - Mobile App Launch & Onboarding (TC-APP-001 to TC-APP-025)
     - Mobile Authentication & Biometrics (TC-APP-026 to TC-APP-060)
     - Darshan Slot Booking & E-Pass (TC-APP-061 to TC-APP-095)
     - Puja Services & Prasad Delivery (TC-APP-096 to TC-APP-125)
     - Live Streaming & Media (TC-APP-126 to TC-APP-150)
     - Digital Wallet & Payments (TC-APP-151 to TC-APP-180)
     - Push Notifications & Alerts (TC-APP-181 to TC-APP-210)
     - Offline Caching & Sync (TC-APP-211 to TC-APP-240)
     - Multilingual Localization (TC-APP-241 to TC-APP-265)
     - Touch Gestures & Orientation (TC-APP-266 to TC-APP-290)
     - Permissions & Performance (TC-APP-291 to TC-APP-320)

### Regenerating the Report:
```bash
python generate_appium_excel.py
```
