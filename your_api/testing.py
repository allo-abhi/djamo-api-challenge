from fastapi import FastAPI, BackgroundTasks, HTTPException
import uuid
import asyncio
import httpx

app = FastAPI()

# In-memory storage for transactions (temporary)
transactions = {}

@app.post("/transaction")
async def create_transaction(background_tasks: BackgroundTasks, transaction_id: str = None):
    # Generate a unique transaction ID if not provided
    transaction_id = transaction_id or str(uuid.uuid4())
    
    # Check for duplicates to ensure idempotency
    if transaction_id in transactions:
        print(f"Duplicate request detected for transaction {transaction_id}")
        return {"id": transaction_id, "status": "already processed"}
    
    # Mark the transaction as pending
    transactions[transaction_id] = "pending"
    print(f"Marked transaction {transaction_id} as pending")
    
    # Start a background task to handle the third-party call
    background_tasks.add_task(handle_third_party, transaction_id)
    print(f"Started background task for transaction {transaction_id}")
    
    # Respond immediately to the client
    return {"id": transaction_id, "status": "pending"}

# @app.post("/transaction")
# async def create_transaction(background_tasks: BackgroundTasks, transaction_id: str = None):
#     """
#     Handles a new transaction request from the mobile app.
#     - Generates a unique transaction ID if none is provided.
#     - Ensures duplicate requests are handled only once.
#     - Starts a background task to communicate with the third-party service.
#     - Responds immediately to the client for a smooth user experience.
#     """
#     # Generate a unique transaction ID if not provided
#     transaction_id = transaction_id or str(uuid.uuid4())  # Use UUID to avoid collisions
    
#     # Check for duplicates to ensure idempotency
#     if transaction_id in transactions:
#         print(f"Duplicate request detected for transaction {transaction_id}")
#         return {"message": "Transaction already processed", "transaction_id": transaction_id}
    
#     # Mark the transaction as pending
#     transactions[transaction_id] = "pending"
#     print(f"Marked transaction {transaction_id} as pending")
    
#     # Start a background task to handle the third-party call
#     background_tasks.add_task(handle_third_party, transaction_id)
#     print(f"Started background task for transaction {transaction_id}")
    
#     # Respond immediately to the client
#     return {"message": "Transaction received", "transaction_id": transaction_id}

async def handle_third_party(transaction_id: str):
    """
    Handles communication with the third-party service.
    - Sends the transaction details to the third-party service.
    - Implements retries in case of timeouts or failures.
    - Logs each step for debugging purposes.
    """
    print(f"Processing transaction {transaction_id} with the third-party service...")
    
    # Define the URL of the third-party mock service
    third_party_url = "http://thirdpartymock:3000/transaction"
    
    # Prepare the payload for the third-party service
    payload = {
        "id": transaction_id,
        "webhookUrl": "http://your_api:8000/webhook"  # URL where the webhook will be sent
    }
    
    try:
        # Send the POST request to the third-party service
        async with httpx.AsyncClient() as client:
            response = await client.post(third_party_url, json=payload, timeout=10)  # Timeout after 10 seconds
        
        # Check the response status
        if response.status_code == 200:
            print(f"Third-party accepted transaction {transaction_id}")
        else:
            print(f"Third-party failed transaction {transaction_id}: {response.status_code}")
    
    except httpx.TimeoutException:
        # Handle timeout by retrying after a delay
        print(f"Timeout occurred for transaction {transaction_id}. Retrying...")
        await asyncio.sleep(5)
        await handle_third_party(transaction_id)  # Retry the request
    
    except Exception as e:
        # Handle other exceptions (e.g., network errors)
        print(f"Error processing transaction {transaction_id}: {e}")

@app.post("/webhook")
async def handle_webhook(data: dict):
    """
    Handles callbacks from the third-party service via webhook.
    - Updates the transaction state based on the webhook payload.
    - Raises a 404 error if the transaction ID isn't found.
    """
    transaction_id = data.get("id")
    status = data.get("status")
    
    if transaction_id in transactions:
        # Update the transaction state
        transactions[transaction_id] = status
        print(f"Webhook received for transaction {transaction_id}: {status}")
    else:
        raise HTTPException(status_code=404, detail="Transaction not found")

@app.get("/transaction/{transaction_id}")
async def get_transaction_status(transaction_id: str):
    """
    Retrieves the status of a specific transaction.
    - Returns the transaction status if it exists.
    - Raises a 404 error if the transaction ID isn't found.
    """
    if transaction_id in transactions:
        return {"id": transaction_id, "status": transactions[transaction_id]}
    raise HTTPException(status_code=404, detail="Transaction not found")