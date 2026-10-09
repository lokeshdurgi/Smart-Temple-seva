/**
 * Smart Temple Web Frontend - Selenium E2E Automation Test Suite
 * File: selenium-tests/tests/login-tests.js
 * Feature: Authentication & User Login Functionality E2E Tests
 * Target Platform: Web Frontend (Smart Temple Management System)
 */

const { Builder, By, until, Key } = require('selenium-webdriver');
const chrome = require('selenium-webdriver/chrome');
const firefox = require('selenium-webdriver/firefox');
const path = require('path');
const fs = require('fs');

// Configuration Constants
const BASE_URL = process.env.BASE_URL || 'http://localhost:3000';
const LOGIN_URL = `${BASE_URL}/login`;
const DASHBOARD_URL = `${BASE_URL}/dashboard`;
const DEFAULT_TIMEOUT = 10000;

// Test Results Collector for Reporting
const testResults = [];

// Helper Function: Take Screenshot on Failure
async function captureScreenshot(driver, testName) {
    try {
        const image = await driver.takeScreenshot();
        const screenshotDir = path.join(__dirname, '../screenshots');
        if (!fs.existsSync(screenshotDir)) {
            fs.mkdirSync(screenshotDir, { recursive: true });
        }
        const filePath = path.join(screenshotDir, `${testName.replace(/[^a-zA-Z0-9]/g, '_')}_${Date.now()}.png`);
        fs.writeFileSync(filePath, image, 'base64');
        console.log(`  📸 Screenshot saved: ${filePath}`);
    } catch (err) {
        console.error('  ⚠️ Failed to capture screenshot:', err.message);
    }
}

// Helper Function: Setup WebDriver Instance
async function createDriver(browserName = 'chrome', headless = true) {
    let builder = new Builder().forBrowser(browserName);

    if (browserName === 'chrome') {
        const chromeOptions = new chrome.Options();
        if (headless) {
            chromeOptions.addArguments('--headless=new');
        }
        chromeOptions.addArguments(
            '--no-sandbox',
            '--disable-dev-shm-usage',
            '--disable-gpu',
            '--window-size=1920,1080',
            '--ignore-certificate-errors'
        );
        builder.setChromeOptions(chromeOptions);
    } else if (browserName === 'firefox') {
        const firefoxOptions = new firefox.Options();
        if (headless) {
            firefoxOptions.addArguments('-headless');
        }
        builder.setFirefoxOptions(firefoxOptions);
    }

    const driver = await builder.build();
    await driver.manage().setTimeouts({ implicit: 5000, pageLoad: 30000, script: 30000 });
    return driver;
}

// Page Object Model (POM): Login Page Elements & Actions
class LoginPage {
    constructor(driver) {
        this.driver = driver;
        // Locators
        this.emailInput = By.css('input[name="email"], input[type="email"], #email');
        this.passwordInput = By.css('input[name="password"], input[type="password"], #password');
        this.loginButton = By.css('button[type="submit"], #login-btn, .btn-login');
        this.rememberMeCheckbox = By.css('input[name="rememberMe"], #remember-me');
        this.forgotPasswordLink = By.css('a[href*="forgot"], .forgot-password-link');
        this.errorMessage = By.css('.error-message, .alert-danger, #login-error');
        this.successToast = By.css('.toast-success, .alert-success, #login-success');
        this.userProfileDropdown = By.css('.user-profile-menu, #user-dropdown');
        this.logoutButton = By.css('#logout-btn, .logout-link');
        this.mfaCodeInput = By.css('input[name="mfaCode"], #mfa-code');
        this.mfaSubmitButton = By.css('button#mfa-submit, .btn-mfa-submit');
        this.roleSelector = By.css('select[name="role"], #user-role');
        this.showPasswordToggle = By.css('.toggle-password-visibility, #show-password');
        this.captchaInput = By.css('input[name="captcha"], #captcha');
    }

    async navigate() {
        await this.driver.get(LOGIN_URL);
        await this.driver.wait(until.elementLocated(this.emailInput), DEFAULT_TIMEOUT);
    }

    async enterEmail(email) {
        const el = await this.driver.findElement(this.emailInput);
        await el.clear();
        await el.sendKeys(email);
    }

    async enterPassword(password) {
        const el = await this.driver.findElement(this.passwordInput);
        await el.clear();
        await el.sendKeys(password);
    }

    async selectRole(role) {
        try {
            const el = await this.driver.findElement(this.roleSelector);
            await el.sendKeys(role);
        } catch (e) {
            // Optional role selector if not present in basic view
        }
    }

    async clickRememberMe() {
        const el = await this.driver.findElement(this.rememberMeCheckbox);
        if (!(await el.isSelected())) {
            await el.click();
        }
    }

    async submitLogin() {
        const btn = await this.driver.findElement(this.loginButton);
        await btn.click();
    }

    async login(email, password, role = null) {
        await this.enterEmail(email);
        await this.enterPassword(password);
        if (role) await this.selectRole(role);
        await this.submitLogin();
    }

    async getErrorMessage() {
        const el = await this.driver.wait(until.elementLocated(this.errorMessage), DEFAULT_TIMEOUT);
        return await el.getText();
    }

    async isDashboardLoaded() {
        await this.driver.wait(until.urlContains('/dashboard'), DEFAULT_TIMEOUT);
        return (await this.driver.getCurrentUrl()).includes('/dashboard');
    }

    async togglePasswordVisibility() {
        const el = await this.driver.findElement(this.showPasswordToggle);
        await el.click();
    }

    async getPasswordInputType() {
        const el = await this.driver.findElement(this.passwordInput);
        return await el.getAttribute('type');
    }
}

// Helper Test Logger
function recordTestResult(tcId, suite, title, status, executionTimeMs, notes = '') {
    testResults.push({
        tcId,
        suite,
        title,
        status,
        executionTimeMs,
        notes,
        timestamp: new Date().toISOString()
    });
    const statusSymbol = status === 'PASS' ? '✅' : status === 'FAIL' ? '❌' : '⚠️';
    console.log(`[${statusSymbol} ${status}] ${tcId} - ${title} (${executionTimeMs}ms)`);
}

// Automated Test Runner Engine
async function runSeleniumTestSuite() {
    console.log('🚀 Starting Smart Temple Frontend Selenium E2E Test Suite Execution...\n');
    let driver;

    try {
        driver = await createDriver('chrome', true);
        const loginPage = new LoginPage(driver);

        // --- TEST CASE GROUP 1: Standard UI & Render Validation ---
        await (async () => {
            const startTime = Date.now();
            try {
                await loginPage.navigate();
                const title = await driver.getTitle();
                if (title.toLowerCase().includes('temple') || title.toLowerCase().includes('login')) {
                    recordTestResult('TC-LOG-001', 'UI Elements', 'Verify Login Page Title and Load Status', 'PASS', Date.now() - startTime);
                } else {
                    recordTestResult('TC-LOG-001', 'UI Elements', 'Verify Login Page Title and Load Status', 'FAIL', Date.now() - startTime, `Unexpected title: ${title}`);
                }
            } catch (err) {
                recordTestResult('TC-LOG-001', 'UI Elements', 'Verify Login Page Title and Load Status', 'FAIL', Date.now() - startTime, err.message);
            }
        })();

        await (async () => {
            const startTime = Date.now();
            try {
                await loginPage.navigate();
                const emailDisplayed = await driver.findElement(loginPage.emailInput).isDisplayed();
                const passwordDisplayed = await driver.findElement(loginPage.passwordInput).isDisplayed();
                const submitBtnDisplayed = await driver.findElement(loginPage.loginButton).isDisplayed();

                if (emailDisplayed && passwordDisplayed && submitBtnDisplayed) {
                    recordTestResult('TC-LOG-002', 'UI Elements', 'Verify essential login controls visibility', 'PASS', Date.now() - startTime);
                } else {
                    recordTestResult('TC-LOG-002', 'UI Elements', 'Verify essential login controls visibility', 'FAIL', Date.now() - startTime, 'Controls missing');
                }
            } catch (err) {
                recordTestResult('TC-LOG-002', 'UI Elements', 'Verify essential login controls visibility', 'FAIL', Date.now() - startTime, err.message);
            }
        })();

        // --- TEST CASE GROUP 2: Successful Login Scenarios ---
        await (async () => {
            const startTime = Date.now();
            try {
                await loginPage.navigate();
                await loginPage.login('admin@smarttemple.com', 'AdminPass123!');
                const isSuccess = await loginPage.isDashboardLoaded();
                if (isSuccess) {
                    recordTestResult('TC-LOG-003', 'Authentication', 'Successful Admin Login with Valid Credentials', 'PASS', Date.now() - startTime);
                } else {
                    recordTestResult('TC-LOG-003', 'Authentication', 'Successful Admin Login with Valid Credentials', 'FAIL', Date.now() - startTime, 'Dashboard not reached');
                }
            } catch (err) {
                await captureScreenshot(driver, 'TC-LOG-003-Fail');
                recordTestResult('TC-LOG-003', 'Authentication', 'Successful Admin Login with Valid Credentials', 'FAIL', Date.now() - startTime, err.message);
            }
        })();

        await (async () => {
            const startTime = Date.now();
            try {
                await loginPage.navigate();
                await loginPage.login('devotee1@gmail.com', 'DevoteePass2026!');
                const isSuccess = await loginPage.isDashboardLoaded();
                if (isSuccess) {
                    recordTestResult('TC-LOG-004', 'Authentication', 'Successful Devotee User Login', 'PASS', Date.now() - startTime);
                } else {
                    recordTestResult('TC-LOG-004', 'Authentication', 'Successful Devotee User Login', 'FAIL', Date.now() - startTime, 'Dashboard not reached');
                }
            } catch (err) {
                recordTestResult('TC-LOG-004', 'Authentication', 'Successful Devotee User Login', 'FAIL', Date.now() - startTime, err.message);
            }
        })();

        // --- TEST CASE GROUP 3: Invalid Credentials & Input Validation ---
        await (async () => {
            const startTime = Date.now();
            try {
                await loginPage.navigate();
                await loginPage.login('admin@smarttemple.com', 'WrongPassword123');
                const errorText = await loginPage.getErrorMessage();
                if (errorText.toLowerCase().includes('invalid') || errorText.toLowerCase().includes('failed')) {
                    recordTestResult('TC-LOG-005', 'Validation', 'Verify Error Message on Invalid Password', 'PASS', Date.now() - startTime);
                } else {
                    recordTestResult('TC-LOG-005', 'Validation', 'Verify Error Message on Invalid Password', 'FAIL', Date.now() - startTime, `Unexpected msg: ${errorText}`);
                }
            } catch (err) {
                recordTestResult('TC-LOG-005', 'Validation', 'Verify Error Message on Invalid Password', 'FAIL', Date.now() - startTime, err.message);
            }
        })();

        await (async () => {
            const startTime = Date.now();
            try {
                await loginPage.navigate();
                await loginPage.login('nonexistent_user@temple.org', 'Password123!');
                const errorText = await loginPage.getErrorMessage();
                if (errorText.toLowerCase().includes('not found') || errorText.toLowerCase().includes('invalid')) {
                    recordTestResult('TC-LOG-006', 'Validation', 'Verify Error Message on Unregistered Email', 'PASS', Date.now() - startTime);
                } else {
                    recordTestResult('TC-LOG-006', 'Validation', 'Verify Error Message on Unregistered Email', 'FAIL', Date.now() - startTime, `Unexpected msg: ${errorText}`);
                }
            } catch (err) {
                recordTestResult('TC-LOG-006', 'Validation', 'Verify Error Message on Unregistered Email', 'FAIL', Date.now() - startTime, err.message);
            }
        })();

        // --- TEST CASE GROUP 4: Password Masking & Visibility ---
        await (async () => {
            const startTime = Date.now();
            try {
                await loginPage.navigate();
                const initialType = await loginPage.getPasswordInputType();
                if (initialType === 'password') {
                    recordTestResult('TC-LOG-007', 'Security', 'Verify Password Field Masked by Default', 'PASS', Date.now() - startTime);
                } else {
                    recordTestResult('TC-LOG-007', 'Security', 'Verify Password Field Masked by Default', 'FAIL', Date.now() - startTime, `Type is ${initialType}`);
                }
            } catch (err) {
                recordTestResult('TC-LOG-007', 'Security', 'Verify Password Field Masked by Default', 'FAIL', Date.now() - startTime, err.message);
            }
        })();

        // Print Summary Log
        console.log('\n==================================================');
        console.log(` Execution Summary: Total Tests Run: ${testResults.length}`);
        console.log(` Passed: ${testResults.filter(t => t.status === 'PASS').length}`);
        console.log(` Failed: ${testResults.filter(t => t.status === 'FAIL').length}`);
        console.log('==================================================\n');

    } catch (globalErr) {
        console.error('Fatal Suite Failure:', globalErr);
    } finally {
        if (driver) {
            await driver.quit();
        }
    }
}

// Export Module & Allow Direct Execution
module.exports = { LoginPage, runSeleniumTestSuite, testResults };

if (require.main === module) {
    runSeleniumTestSuite();
}
