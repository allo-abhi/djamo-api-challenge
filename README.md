When I started, I was proficient in Python, HTML, CSS, and a little bit of Bash. But this challenge pushed me far beyond what I already knew — it was a first for many things. I had to teach myself JavaScript, get comfortable with containers and Docker, use GitHub (this is actually my first repo!), learn FastAPI, dive into asynchronous programming, understand how APIs communicate, and debug issues across different layers of a system. It wasn’t always easy, but the process taught me how to break down complex problems, read documentation more effectively, and persist through roadblocks.

What I Have So Far:
1. Handles Transaction Requests
The API successfully receives transaction requests from the mobile app and forwards them to the third-party service.
2. Implements Basic Retry Logic
The system retries transactions that time out, showing an understanding of fault tolerance.
3. Processes Webhooks
The /webhook endpoint processes incoming webhooks from the third-party service and updates transaction statuses accordingly.
4. Logs Key Events
The code logs important events like transaction processing, retries, and webhook receipts, providing some visibility into the system’s behavior.
5. Uses Docker Compose for Local Testing
The project is set up with Docker Compose, allowing for easy local testing and integration with mock services.
6. Validates Third-Party Responses
The system checks whether the third-party service accepts or rejects transactions, ensuring basic validation of external calls.
7. Demonstrates Asynchronous Processing
The use of background tasks shows an understanding of asynchronous programming and its importance in building responsive APIs.

Room For Improvement:
1. Missing Webhook Handling for Retried Transactions
If a transaction is retried after a timeout, there’s no guarantee that the webhook will be processed correctly for the retried attempt.
To fix this, I would implement a better retry logic that ensures webhooks for retried transactions are matched to the correct transaction ID and update the status accordingly.
2. No Fallback Mechanism for Missing Webhooks
If the third-party service fails to send a webhook, the transaction remains stuck in the pending state indefinitely.
Adding a fallback mechanism to query the third-party status-check API after a timeout period to determine the final status of the transaction.
3. Lack of Duplicate Checks
Duplicate requests from the mobile app might result in multiple attempts to process the same transaction.
I would implement idempotency by using a unique transaction ID to detect and ignore duplicate requests.
4. Storing Transactions
Currently, transaction states are stored in memory (e.g., Python dictionaries). While this works for local testing.
Have to explore Redis

and more...
