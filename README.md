# Cloudflare Containers Examples

A demonstration project showcasing how to build and deploy containerized applications on Cloudflare Workers using the Containers API. This project features a Hono-based API that orchestrates interactions between Python FastAPI and Go HTTP containers.

## Overview

This project demonstrates:
- **Container Integration**: Deploy and manage multiple container services within Cloudflare Workers
- **Multi-Language Support**: Python FastAPI and Go HTTP services running as containers
- **Durable Objects**: Container services configured as Durable Objects for state management
- **Environment Configuration**: Dynamic environment variable injection into containers

## Architecture

The application consists of:

1. **Main Worker** - Hono-based TypeScript application that routes requests
2. **Python FastAPI Container** - Provides REST API endpoints with Cloudflare location data
3. **Go HTTP Container** - Handles task processing with detailed system information logging

## Project Structure

```
├── src/
│   ├── index.ts              # Main worker entry point
│   └── container-services.ts # Container class definitions
├── containers/
│   ├── python-fastapi/       # Python FastAPI container
│   │   ├── Dockerfile
│   │   ├── requirements.txt
│   │   └── app/main.py
│   └── go-task/             # Go HTTP container
│       ├── Dockerfile
│       ├── go.mod
│       └── main.go
├── package.json
└── wrangler.jsonc           # Cloudflare Workers configuration
```

## Container Services

### Python FastAPI Container
- **Port**: 8081
- **Max Instances**: 3
- **Sleep After**: 1 minute
- **Endpoints**:
  - `GET /` - Basic health check
  - `GET /python-container` - Container info with location data
  - `GET /load-balance` - Full Cloudflare environment details

### Go Task Container
- **Port**: 8080
- **Max Instances**: 1
- **Sleep After**: 1 minute
- **Features**:
  - Comprehensive system logging
  - Environment variable collection
  - System information reporting

## Environment Variables

Both containers receive Cloudflare-specific environment variables:
- `CLOUDFLARE_LOCATION` - Geographic location
- `CLOUDFLARE_COUNTRY_A2` - Country code
- `CLOUDFLARE_DEPLOYMENT_ID` - Deployment identifier
- `CLOUDFLARE_NODE_ID` - Node identifier
- `CLOUDFLARE_PLACEMENT_ID` - Placement identifier
- `CLOUDFLARE_REGION` - Region information

## Getting Started

### Prerequisites
- Node.js 18+
- Wrangler CLI
- Docker (for local container development)

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd cloudflare-containers-examples
```

2. Install dependencies:
```bash
npm install
```

3. Configure Wrangler (if needed):
```bash
npx wrangler login
```

### Development

Run the development server:
```bash
npm run dev
```

### Deployment

Deploy to Cloudflare:
```bash
npm run deploy
```

## Configuration

### Wrangler Configuration

The `wrangler.jsonc` file defines:
- Container images and their Dockerfiles
- Durable Object bindings for container classes
- Maximum instance limits per container
- Database migrations for container classes

### Container Classes

Each container extends the base `Container` class from `@cloudflare/containers`:
- Custom environment variables
- Lifecycle event handlers (`onStart`, `onStop`, `onError`)
- Port and sleep configuration

## Key Features

- **Multi-Container Orchestration**: Manage multiple container types within a single Worker
- **Automatic Scaling**: Containers scale based on demand up to configured limits
- **Geographic Distribution**: Leverage Cloudflare's global network for container deployment
- **Environment Injection**: Dynamic environment variable passing to containers
- **Lifecycle Management**: Container start/stop/error event handling

## API Endpoints

The containers provide various endpoints for testing and monitoring:

**Python FastAPI Container:**
- Health checks and status information
- Cloudflare environment data exposure
- Load balancing demonstration

**Go Task Container:**
- System information logging
- Environment variable reporting
- Process and runtime details

## Technologies Used

- **Runtime**: Cloudflare Workers
- **API Framework**: Hono
- **Containers**: Docker
- **Languages**: TypeScript, Python, Go
- **Python Framework**: FastAPI
- **Build Tool**: Wrangler

## License

This project serves as an example for Cloudflare Containers implementation and is intended for educational and demonstration purposes.
