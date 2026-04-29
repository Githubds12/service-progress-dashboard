# Shop Apotheke Automation & Testing Report

## 1. Scope
Automated testing of the user onboarding flow and prescription readiness.

## 2. Test Scenarios

### Scenario 1: New User Onboarding
- **Goal**: Register a new user and trigger phone verification.
- **Steps**:
  1. Call `register()` with fresh email.
  2. Extract `customerId` from response.
  3. Call `request_phone_otp()`.
- **Expected Result**: User created and SMS sent.

### Scenario 2: Prescription Flow Verification
- **Goal**: Ensure NFC positioning logic is reachable.
- **Steps**:
  1. Call `record_nfc_position()`.
- **Expected Result**: `204 No Content` or `200 OK`.

## 3. Automation Implementation Notes
- **Library**: Python `requests`.
- **Environment**: Tested against production API endpoints.
- **Headers**: Requires unique `x-request-id` per call to avoid idempotency conflicts if implemented server-side.
