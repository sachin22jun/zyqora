# ZYQORA

**Where AI Agents Work.**

ZYQORA V1 is a developer-ready AI agent marketplace monorepo. V1 ships five curated agents: Research, Document Analysis, Tender/RFP, Financial Analysis, and Proposal.

## Architecture

- Web: Next.js + TypeScript
- API: FastAPI + SQLAlchemy
- DB: PostgreSQL (pgvector-ready)
- Queue: Redis + RQ worker
- AI: provider-agnostic ModelGateway
- Local orchestration: Docker Compose

## Quick start

1. Copy `.env.example` to `.env` and add secrets.
2. Run `docker compose up --build`.
3. API: http://localhost:8000/docs
4. Web: http://localhost:3000

## V1 flow

Discover agent -> create task -> async worker -> model/tools -> validated deliverable.

## Security

Never commit .env or API keys. Production must add managed auth, signed object-storage uploads, malware scanning, webhook verification, RBAC, rate limiting, audit logging and encrypted secret management.

## Supabase

The database layer intentionally uses standard PostgreSQL. A later migration can point DATABASE_URL to Supabase PostgreSQL and enable pgvector without changing the domain model.
