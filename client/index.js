const express = require("express");
const axios = require("axios");

const app = express();
app.use(express.json());

const port = process.env.PORT || 3100;
const yourApiUrl = process.env.YOUR_API || "http://localhost:8000";

// POST /transaction
app.post("/transaction", (_, res) => {
  // Forward the transaction request to your API without generating an ID
  const body = {};
  console.log(`Request transaction creation (no ID generated)`);

  axios
    .post(`${yourApiUrl}/transaction`, body) // Send an empty body to the API
    .then((yourResponse) => {
      const { id, status } = yourResponse.data;
      console.log(`Transaction ${id} is ${status}`);
      res.status(200).send({ message: "Transaction processed", id, status });
    })
    .catch((e) => {
      console.error("Error while calling your API:", e);
      res.status(500).send({ error: "Failed to process transaction" });
    });
});

// Start the server
app.listen(port, () => {
  console.log(`Client mock is listening on port ${port}`);
});