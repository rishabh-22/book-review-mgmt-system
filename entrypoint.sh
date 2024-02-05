#!/bin/bash

# Start server
echo "Starting server"
uvicorn main:app --port 8000