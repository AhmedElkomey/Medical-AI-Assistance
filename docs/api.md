# Medical AI API Documentation

## Endpoints

### GET /

- **Description**: Root endpoint
- **Response**: Welcome message

### POST /process_document/

- **Description**: Process and validate a medical document
- **Request Body**: JSON containing document data
- **Response**: Success or error message

### POST /query/

- **Description**: Query the RAG system
- **Request Body**: JSON containing the query
- **Response**: Retrieved and reranked documents
