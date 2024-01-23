# Real time Insights metric powered by Gemini

![Alt Text](https://github.com/g-emarco/gemini-data-insights/blob/main/static/architecture.png)

## Tech Stack

**Server Side:** LangChain  🦜🔗

**LLM:** Gemini  

**Runtime:** Cloud Functions Gen2

**Message Bus:** Pub/Sub

**Monitoring Dashboard:** Log based metrics and cloud monitoring

## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`GCP_PROJECT`
`GOOGLE_APPLICATION_CREDENTIALS` `LOCAL`

## Run Locally


Clone the project

```bash
  git clone https://github.com/g-emarco/gemini-data-insights.git
```

Go to the project directory

```bash
  cd gemini-data-insights
```

Install dependencies

```bash
  python digest-messages.py
```

NOTE: When running locally make sure `GOOGLE_APPLICATION_CREDENTIALS` is set to a service account with permissions to use VertexAI


## Deployment

CI/CD via Cloud build is available in ```cloudbuild.yaml```

Please replace $PROJECT_ID with your actual Google Cloud project ID.

1. Make sure you enable GCP APIs:

```bash
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable secretmanager.googleapis.com
gcloud services enable artifactregistry.googleapis.com
gcloud services enable vertexai.googleapis.com

```

2. Create a service account `vertex-ai-consumer` with the following roles:




```bash
gcloud iam service-accounts create vertex-ai-consumer \
    --display-name="Vertex AI Consumer"

gcloud projects add-iam-policy-binding PROJECT_ID \
    --member="serviceAccount:vertex-ai-consumer@PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/run.invoker"

gcloud projects add-iam-policy-binding PROJECT_ID \
    --member="serviceAccount:vertex-ai-consumer@PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/serviceusage.serviceUsageConsumer"

gcloud projects add-iam-policy-binding PROJECT_ID \
    --member="serviceAccount:vertex-ai-consumer@PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/ml.admin"

gcloud projects add-iam-policy-binding PROJECT_ID \
    --member="serviceAccount:vertex-ai-consumer@PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/vertexai.admin"

```

Create a Pub/Sub Topic:

```bash
  gcloud pubsub topics create messages
```


Assign the Subscriber role:

```bash
  gcloud pubsub subscriptions add-iam-policy-binding messages-subscription \
  --member=serviceAccount:[SA-EMAIL] \
  --role=roles/pubsub.subscriber
```

Deploy to Cloud Function

```bash
gcloud functions deploy offside-detector \
  --region=us-east1 \
  --source=./offside-detector \
  --trigger-topic=messages \
  --runtime=python311 \
  --gen2 \
  --entry-point=subscribe \
  --service-account=vertex-ai-consumer@$PROJECT_ID.iam.gserviceaccount.com \
  --memory=8Gi \
  --cpu=8
```

## 🚀 About Me
Eden Marco, LLM Lead @ Google Cloud, Tel Aviv🇮🇱

[![linkedin](https://img.shields.io/badge/linkedin-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/eden-marco/) 

[![twitter](https://img.shields.io/badge/twitter-1DA1F2?style=for-the-badge&logo=twitter&logoColor=white)](https://twitter.com/EdenEmarco177)
