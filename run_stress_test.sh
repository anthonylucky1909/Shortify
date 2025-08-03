#!/bin/bash

# Create output folder if it doesn't exist
mkdir -p results

# Define test parameters
USERS=50
SPAWN_RATE=500
RUNTIME="3m"
HOST="http://localhost"
CSV_PATH="results/loadtest"
LOCUST_FILE="locustfile.py"

echo "🚀 Starting high-scale Locust test..."
echo "Users: $USERS, Spawn Rate: $SPAWN_RATE/sec, Duration: $RUNTIME"

# Run Locust in headless mode
locust -f $LOCUST_FILE \
  --headless \
  -u $USERS \
  -r $SPAWN_RATE \
  --run-time $RUNTIME \
  --host $HOST \
  --csv=$CSV_PATH

echo "✅ Load test finished. Results saved to:"
echo "  $CSV_PATH_stats.csv"
echo "  $CSV_PATH_failures.csv"
