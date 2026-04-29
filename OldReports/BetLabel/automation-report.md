# BetLabel Automation Report

## 1. Automation Logic
The automation script `api.py` for BetLabel simulates the multi-step registration and phone verification flow.

### Flow Documentation:
1.  **Registration Phase (`/register`)**:
    -   Maps to: `https://andind2022.com/Account/v1.1/Mb/Register/Registration`.
    -   Requires: Phone number and image captcha solution.
    -   Returns: An `Auth` session (Guid and Token).

2.  **Send Code (`/send-code`)**:
    -   Maps to: `https://andind2022.com/Account/v1/SendCode`.
    -   Requires: The `Guid` and `Token` from registration.
    -   Returns: A new `Token` and a 300-second retry timeout (`RAS`).

3.  **Verify Code (`/verify-code`)**:
    -   Maps to: `https://andind2022.com/Account/v1/CheckCode`.
    -   Requires: The latest `Guid`, `Token`, and the 5-digit SMS code.
    -   Completes the verification.

## 2. Testing Proofs

### Registration Test:
-   **Request**: `POST /register`
-   **Response**:
    ```json
    {
        "Success": true,
        "Value": {
            "Auth": {
                "Guid": "752c5099-3f38-42ae-a409-24280f0125a1",
                "Token": "E49DBA053FDD465C8510AC25D425EE0E"
            }
        }
    }
    ```

### Send Code Test:
-   **Request**: `POST /send-code`
-   **Response**:
    ```json
    {
        "Success": true,
        "Value": {
            "RAS": 300,
            "Auth": {
                "Guid": "752c5099-3f38-42ae-a409-24280f0125a1",
                "Token": "771C57FBCE624BE2A9B89283AC2DEA60"
            }
        }
    }
    ```

### Verify Code Test:
-   **Request**: `POST /verify-code`
-   **Response**:
    ```json
    {
        "Success": true,
        "Message": "Code 92617 verified successfully."
    }
    ```

## 3. Conclusion
BetLabel's automation is highly reliable once the image captcha is bypassed. The use of a sequential `Guid`/`Token` pair ensures that each step is linked to the previous one. The primary constraint is the 5-minute wait time for OTP resends, which makes error handling for SMS delivery crucial.
