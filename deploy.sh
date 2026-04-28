#!/bin/bash

# Exit on error
set -e

# ===== CONFIG =====
PROJECT_ID="cs446-fraud-detection"
REGION="us-central1"
SERVICE="fraud-processor"
REPO="fraud-repo"
IMAGE="$REGION-docker.pkg.dev/$PROJECT_ID/$REPO/$SERVICE"

echo "Setting project..."
gcloud config set project "$PROJECT_ID"

echo "Building container..."
gcloud builds submit service --tag "$IMAGE"

echo "Deploying to Cloud Run..."
gcloud run deploy "$SERVICE" \
  --image "$IMAGE" \
  --region "$REGION" \
  --no-allow-unauthenticated

echo "Deployment complete!"

echo "Sending test message..."
gcloud pubsub topics publish transaction-events \
  --message='{"transaction_id":"deploy-test","amount":500,"timestamp":1710000000}'

echo "Recent logs:"
gcloud run services logs read "$SERVICE" \
  --region "$REGION" \
  --limit 20

echo "Done!"
