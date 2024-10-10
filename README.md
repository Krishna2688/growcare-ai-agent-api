# growcare-ai-agent-api

gcloud builds submit --tag gcr.io/sanctum-2604/growcare-ai-agent-api
gcloud run deploy growcare-ai-agent-api --image gcr.io/sanctum-2604/growcare-ai-agent-api --platform managed

gsutil iam ch user:ckk2k6@gmail.com:roles/storage.legacyBucketReader gs://610021001965.cloudbuild-logs.googleusercontent.com