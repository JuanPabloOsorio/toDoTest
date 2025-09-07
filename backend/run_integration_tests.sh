#!/bin/bash

# Run the integration tests for the API routes
cd "$(dirname "$0")"
python -m pytest test/integration/api -v
