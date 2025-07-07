README from Djamo:
The goal of this test is to be a work sample. Instead of asking you to solve a quizz, implement fizzbuzz or a binary tree search, we would like you to work on something similar to our work. A very common task at Djamo is to integrate with third parties, and while we try to keep our services highly available, fast and reliable, unfortunately we often face issues with our partners.

However, it is Djamo's mission to bring the best experience to our customers. That means it is our duty to handle cleanly all of these errors, so that from a user perspective it looks like everything went fine. This test will give you a glimpse of the issues we can face with 3rd parties.

You're tasked to developed an API. A mobile application will call your API, and in turn you'll have to call an external service. If the transfer worked, you'll have to notify the mobile application of the success, otherwise, of the failure.

3rd party's constraints
As mentionned before, our partners have a number issues, and this one has its share:

- it does not return immediatly if it worked, or not
- it takes a long time to answer (up to 10s)
- it is supposed to call you back through a webhook -- but sometimes it doesn't
- it has a status check API -- but they explicitely said they could block our services if we request it too often
- it will time out (HTTP 504) from time to time, but sometimes the request actually will go through after a longer time (up to 120s).
Your constraints
Your API is consumed by a mobile application, and the experience needs to feel pleasant for the user. So you need to:

- return a response as fast as possible
- return the success / failure of the transaction as quickly as possible
- Due to poor network connectivity, sometimes the mobile application will re-try to send the same request twice. You must detect it and only handle the request once.

You can start the project easily by running docker-compose up -d. This will start a mock for the 3rd party service and for the client application

My README:
When I started, I was proficient in Python. I had to teach myself JavaScript, get comfortable with containers and Docker, git, learn FastAPI, dive into asynchronous programming, understand how APIs communicate, and debug issues across different layers of a system. 

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
