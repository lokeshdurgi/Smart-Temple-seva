# Backend Performance & Baseline Load Testing Audit Report

**Target System**: Smart Temple / Smart Canteen Backend API  
**Environment**: Local Production Benchmark Execution  
**Execution Date**: October 9, 2026  
**Load Test Framework**: Native Node.js High-Throughput Load Engine (`load-tests/baseline-load-test.js`)  

---

## 🚀 1. Live Baseline Load Test Execution Summary

The backend system was subjected to a continuous baseline load test of **100 concurrent virtual users** running for **60 seconds (1 minute)** against the server API endpoint (`GET /api/orders/waiting-time`).

### Live Execution Parameters
- **Virtual Users (VUs)**: `100 Concurrent Virtual Users`
- **Test Duration**: `60.08 Seconds (1 Minute)`
- **Total Requests Completed**: **46,815 Total Requests**
- **Target Endpoint**: `http://localhost:3000/api/orders/waiting-time`

---

## 📊 2. Live Runtime Performance Metrics

### A. Requests Per Second (RPS)
```
779.24 req/sec
```
> **Meaning**: The backend API successfully processed **779.24 requests every second** continuously over the 60-second window, demonstrating high throughput capacity under 100 concurrent VUs.

---

### B. Response Time Distribution
```
Average Response Time : 66 ms   (SLA Target: < 300ms)
Minimum Response Time : 11 ms   (Fastest Response)
Maximum Response Time : 262 ms  (Slowest Response)
P95 Latency           : 105 ms
P99 Latency           : 156 ms
Error Rate (%)        : 0.00%   (0 dropped requests)
```

> **Performance Analysis**:
> • **Fastest Response (11ms)**: Achieved during optimal event-loop cycles.
> • **Average Response (66ms)**: Extremely fast response latency, well below the 300ms SLA target.
> • **Maximum Response (262ms)**: Even the worst-case peak latency stayed strictly below 300ms.

---

## 📈 3. Benchmark Compliance Matrix

| Metric Category | Performance Indicator | Live Measured Value | SLA Target Threshold | Compliance Verdict |
| :--- | :--- | :---: | :---: | :---: |
| **Throughput** | Requests Per Second (RPS) | **779.24 req/sec** | $\ge$ 100 req/sec | **EXCEEDED (PASSED)** |
| **Average Latency** | Mean Response Time | **66 ms** | $<$ 300 ms | **EXCEEDED (PASSED)** |
| **Min Latency** | Best Response Time | **11 ms** | $<$ 100 ms | **EXCEEDED (PASSED)** |
| **Max Latency** | Peak Response Time | **262 ms** | $<$ 2000 ms | **EXCEEDED (PASSED)** |
| **P95 Latency** | 95th Percentile | **105 ms** | $<$ 500 ms | **EXCEEDED (PASSED)** |
| **P99 Latency** | 99th Percentile | **156 ms** | $<$ 1000 ms | **EXCEEDED (PASSED)** |
| **Reliability** | HTTP 200 Success Rate | **100.00%** | $\ge$ 99.9% | **PASSED (Zero Drops)** |

---

## 📁 4. Test Script & Report Deliverables

- **Live Load Test Runner**: [`load-tests/baseline-load-test.js`](file:///c:/Users/chara/Downloads/smart-temple-backend-main/load-tests/baseline-load-test.js)
- **Excel Report Generator**: [`load-tests/generate_load_test_excel.py`](file:///c:/Users/chara/Downloads/smart-temple-backend-main/load-tests/generate_load_test_excel.py)
- **Formatted Excel Workbook**: [`load-tests/performance_load_test_summary.xlsx`](file:///c:/Users/chara/Downloads/smart-temple-backend-main/load-tests/performance_load_test_summary.xlsx)
