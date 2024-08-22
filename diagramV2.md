```mermaid
sequenceDiagram
    title Shipping Ships API

    participant Client
    participant Python
    participant JSONServer
    participant Database
    Client->>Python:GET request to "/ships"
    Python->>JSONServer:Run do_GET() method
    JSONServer->>Database: list_ships() fetches data
     Database-->>JSONServer: return ship data
    JSONServer-->>Client: Here's all yer ships (in JSON format)

```
<!--- (HandleRequests parses the URL, determines which resource is being requested, and interacts with the Database to fetch the relevant data.)
-->

<!---
JSONServer->>Database: parse_url fetches data.

Correct Understanding:
The parse_url function only processes and returns the structured URL components so that your server can determine what resource is being requested (e.g., ships) and if any specific filtering (e.g., by ID) should be applied. 

The actual interaction with the database to fetch the ship data occurs in a different function, which, based on your code structure, would typically be in the list_ships() function or its equivalent.)
-->