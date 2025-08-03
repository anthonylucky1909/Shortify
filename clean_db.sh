#!/bin/bash

echo "⚠️  WARNING: This will delete MongoDB 'url_shortener' database and Redis DB 0"
read -p "Proceed? (y/n): " confirm
if [[ "$confirm" != "y" ]]; then
  echo "Aborted."
  exit 1
fi

# Drop MongoDB database using mongosh
echo "🧹 Dropping MongoDB database 'url_shortener'..."
mongosh <<EOF
use url_shortener
db.dropDatabase()
EOF

# Flush Redis DB 0
echo "🧹 Flushing Redis DB 0..."
redis-cli -n 0 flushdb

echo "✅ MongoDB and Redis cache cleaned!"

# chmod +x clean_db.sh. -> ./clean_db.sh