# Automation Testing Report - E-GetS

## Test Overview
- **Service**: E-GetS
- **Script**: `api.py`
- **Target Endpoint**: `GET https://uni.e-gets.com/api/user/app/1.3/captcha/send`
- **Goal**: Verify if the SMS trigger endpoint can be automated via simple replay.

## Execution Results

### Attempt 1: Replay with Fresh Timestamp
- **Timestamp**: Current time
- **Signature**: Replayed from HAR
- **Result**: `403 Forbidden`
- **Response**: `{"code":"610000","message":"sign_type miss!"}`
- **Analysis**: The server detected a mismatch between the fresh timestamp and the replayed signature (which is tied to the original timestamp).

### Attempt 2: Exact Replay (Original Timestamp + Signature)
- **Timestamp**: `1777451042173` (from HAR)
- **Signature**: `MDUwMmM4OGMzZWUyNzA4N2YwZDg0ZmFhNzJmYjE2MmJmYzY3Y2M1ZDYzNjM3ZTE0ZGI0MThiN2U5ZDJlMmIyYw==`
- **Result**: `403 Forbidden`
- **Response**: `{"code":"610008","message":"Request timestamp is invalid"}`
- **Analysis**: The server correctly identified that the replayed timestamp is expired (from the past).

## Conclusion
Automation via simple replay is **not possible**. The E-GetS API implements strict timestamp validation and cryptographic signing (S2). To automate this service, the signing algorithm must be reverse-engineered from the Android application to generate valid signatures for current timestamps.
