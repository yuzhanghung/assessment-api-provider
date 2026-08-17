# Assessment API Provider

A **mock assessment API provider** used by the [SecureCheck](#) project to simulate the behavior of an external security assessment service.

> **⚠️ Important:** This is **not a real security assessment engine**. It does not perform actual vulnerability scanning, security analysis, or artifact inspection. Assessment results and status transitions are simulated for development, testing, and demonstration purposes.

## Overview

SecureCheck is designed to demonstrate how an application can integrate with an external assessment provider through APIs, asynchronous status updates, webhooks, and artifact storage.

This repository acts as the **mock external provider** in that architecture.

It simulates the lifecycle of an assessment:

```text
Create Assessment
       ↓
   Submitted
       ↓
    Pending
       ↓
    Running
       ↓
   Completed
       ↓
   Mock Results
```

The provider exposes API endpoints that allow SecureCheck to:

* Create assessments
* Receive uploaded artifact information
* Start assessments
* Track assessment status
* Register webhook endpoints
* Receive asynchronous status callbacks
* Retrieve simulated assessment results

## What This Project Does

This service simulates an external provider that SecureCheck would normally communicate with.

For example:

```text
SecureCheck Dashboard
        │
        │ Create / Start Assessment
        ▼
Assessment API Provider
        │
        │ Simulated processing
        ▼
Assessment Status
        │
        ├── pending
        ├── running
        └── completed
        │
        ▼
Webhook → SecureCheck
```

The processing delay and assessment results are intentionally simulated.

## What This Project Does NOT Do

This provider does **not**:

* Perform real vulnerability scanning
* Analyze uploaded source code for actual vulnerabilities
* Run penetration tests
* Execute malware analysis
* Perform real security assessments
* Generate production-grade security findings
* Guarantee that an artifact is secure or insecure

Any assessment result returned by this service should be treated as **mock/demo data**.

## Why a Mock Provider?

The purpose of this project is to demonstrate the **integration architecture** between SecureCheck and an external assessment provider without depending on a real third-party security scanning service.

This allows the project to demonstrate concepts such as:

* REST API integration
* Authentication
* Asynchronous processing
* Webhooks
* Artifact uploads
* Presigned S3 URLs
* Assessment lifecycle management
* Database persistence
* Background processing
* API-to-API communication

The provider can therefore be replaced by a real assessment service in a production architecture.

## Assessment Lifecycle

When an assessment is started, the provider simulates processing by moving the assessment through several states:

```text
submitted
    ↓
pending
    ↓
running
    ↓
completed
```

When the assessment reaches completion, the provider sends a webhook notification to the registered SecureCheck endpoint.

## Webhooks

The provider supports webhook registration so that SecureCheck can receive asynchronous assessment updates.

Conceptually:

```text
Assessment Provider
       │
       │ assessment status changes
       ▼
Registered Webhook
       │
       ▼
SecureCheck
       │
       ▼
Dashboard updates
```

Webhook requests are signed so that SecureCheck can verify that callbacks originated from the expected provider.

## Artifact Uploads

The provider supports an artifact-upload workflow using **S3-compatible presigned URLs**.

The file itself does not need to pass through the application backend:

```text
SecureCheck
    │
    │ Request presigned URL
    ▼
Assessment API Provider
    │
    │ Presigned URL
    ▼
SecureCheck Browser
    │
    │ Direct upload
    ▼
S3-compatible Storage
```

The provider stores the artifact metadata and uses the uploaded artifact as part of the simulated assessment lifecycle.

> The uploaded artifact is not actually analyzed for security vulnerabilities.

## Technology

The provider is built with technologies including:

* Python
* FastAPI
* SQLAlchemy
* PostgreSQL
* S3-compatible object storage
* Docker

## Local Development

### Requirements

* Python 3.x
* PostgreSQL
* An S3-compatible storage service such as AWS S3 or MinIO

### Run locally

Install dependencies:

```bash
pip install -r requirements.txt
```

Configure the required environment variables in `.env`.

Then start the FastAPI server:

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://localhost:8000
```

FastAPI's interactive API documentation is available at:

```text
http://localhost:8000/docs
```

## Relationship to SecureCheck

This repository is intended to be used together with the SecureCheck application.

SecureCheck acts as the client/application that communicates with this provider, while this repository simulates the external assessment service.

```text
┌──────────────────────┐
│   SecureCheck        │
│                      │
│  Dashboard           │
│  API                 │
│  MCP                 │
└──────────┬───────────┘
           │
           │ API / Webhooks
           ▼
┌──────────────────────┐
│ Assessment API       │
│ Provider             │
│                      │
│ Mock Assessment      │
│ Service              │
└──────────┬───────────┘
           │
           ▼
      S3 Storage
```

## Disclaimer

This project is intended for **software development, architecture demonstration, testing, and educational purposes**.

It should not be used to make real-world security decisions. The assessment results generated by this provider are simulated and **do not represent actual security findings**.

A production implementation would replace this mock provider with a real security assessment engine or third-party security assessment service.
