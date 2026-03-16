# Shadow AI Detection — Product Requirements Document v4.0 (Final)

**Version:** 4.0 (Consolidated: PRD v3.0 + All 8 Amendments)  
**Date:** March 16, 2026  
**Status:** Approved for Implementation  
**Classification:** Confidential — Internal Use Only  
**Platform:** Google Cloud Platform (Jakarta Region — asia-southeast2)

---

## Document Lineage

This PRD v4.0 is the single source of truth. It consolidates and supersedes:

- **Session 1 — PRD v1.0:** Core features, database schema, Next.js tech stack, user flows, compliance framework
- **Session 2 — Executive Summary v1.1 + PRD v1.1:** OJK reporting suite, ISO 42001 module, Agentic AI concept, pricing model, data sovereignty tracker, OJK Semester Report template
- **Session 3 — PRD v1.4 + Architecture v1.4 + HITL Spec:** Quad-Vector model (added Vector D: Endpoint OS), GCP architecture (Dataflow, Firestore, BigQuery), behavioral heuristics engine, HITL audit trail specification, sprint plan, VPC Service Controls
- **Competitive Research:** CloudEagle, Knostic, Portal26, Obsidian, Teramind, Reco analysis; regulatory updates (UU PDP enforcement, Presidential AI Regulation timeline)
- **Amendment #1:** Approved AI Catalog and Self-Service Request Portal
- **Amendment #2:** MCP Server Monitoring (Vector E) — Penta-Vector upgrade
- **Amendment #3:** AI Cost Intelligence Module
- **Amendment #4:** Prompt-Level Data Flow Tracing
- **Amendment #5:** Enterprise AI Sandbox Environment
- **Amendment #6:** SIEM/SOAR Integration and Webhook API
- **Amendment #7:** Employee Education and Policy Nudge Engine
- **Amendment #8:** Offline/Degraded Mode for Local Agents

### Corrections Applied in v4.0

| # | Correction | Details |
|---|---|---|
| 1 | Firestore collection count | Corrected from 35 to **36** (Amendment #7 has 5 collections including tool_suggestions) |
| 2 | User Story total count | Corrected from "37 new" to **33 new** from amendments, **40 total** (7 base + 33 amendment) |
| 3 | Total development weeks | Clarified: **60.5 weeks** amendment work + **13 weeks** MVP = **73.5 total engineering-weeks** (significant parallelism possible) |
| 4 | FR-22 status | Marked as **Superseded by Amendment #4** (FR-45 through FR-51). DLP Prompt Monitoring elevated from P2 to P1 with comprehensive specification. |
| 5 | Sprint count | Clarified: **5 MVP sprints** + **26 amendment sprints** + **2.5 weeks enhancement** to existing MVP sprints |
| 6 | Cloud Functions count | Added missing sandbox-provisioner (Amendment #5). Total: **11 Cloud Functions** |
| 7 | ER relationships | Added missing ORGANIZATIONS to MCP_SERVERS and ORGANIZATIONS to SANDBOX_TRIALS direct relationships |
| 8 | Vector C offline buffer | Added IndexedDB (50 MB) offline buffer for browser extension (Amendment #8) |
| 9 | P1 FR count | Corrected from 39 to **36** (4 base P1 + 6 Am.1 + 7 Am.2 + 7 Am.3 + 7 Am.4 + 5 Am.7) |
| 10 | P2 FR count | Corrected from 14 to **19** (4 base P2 + 7 Am.5 + 8 Am.6) |
| 11 | Annual pricing math | Corrected Basic from Rp 75M to **Rp 90M** ($5,760) and Global from Rp 150M to **Rp 180M** ($11,520). Monthly × 12 = Annual. |

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Context and Background](#2-context-and-background)
3. [Target Audience and Personas](#3-target-audience-and-personas)
4. [The Penta-Vector Discovery Model](#4-the-penta-vector-discovery-model)
5. [User Stories](#5-user-stories)
6. [Functional Requirements](#6-functional-requirements)
7. [Non-Functional Requirements](#7-non-functional-requirements)
8. [HITL Audit Trail Specification](#8-hitl-audit-trail-specification)
9. [Technical Architecture](#9-technical-architecture)
10. [Database Schema](#10-database-schema)
11. [Design and User Experience](#11-design-and-user-experience)
12. [Implementation Roadmap](#12-implementation-roadmap)
13. [Revenue and Pricing Model](#13-revenue-and-pricing-model)
14. [Technical Risks and Mitigations](#14-technical-risks-and-mitigations)
15. [Open Questions](#15-open-questions)
16. [Appendix](#16-appendix)
17. [Required for Acceptance](#17-required-for-acceptance)

---

## 1. Executive Summary

Shadow AI Detection is a "Governance-as-a-Service" platform engineered for the Indonesian mid-market. It addresses the "Compliance Cliff" hitting Indonesian firms on July 1, 2026, by automating the discovery of unauthorized AI tools (Shadow AI) and mapping usage directly to mandatory regulatory reports (OJK and UU PDP).

The platform transforms raw telemetry from browser, network, cloud, OS, and MCP protocol sensors into a defensible audit trail of human-in-the-loop (HITL) oversight, enabling Fintechs to meet the July 31st OJK Semester 1 reporting deadline with zero manual effort.

### 1.1 What Makes This Special

- **The Penta-Vector Engine:** Unlike global competitors that rely solely on browser extensions, this platform monitors Cloud APIs, DNS logs, Browser DOM, OS-level processes, AND MCP Protocol connections — catching Agentic AI and shadow MCP servers that bypass every other detection tool on the market.
- **GCP Sovereignty:** 100% hosted in the GCP Jakarta Region (asia-southeast2), fulfilling UU PDP Article 56 requirements for local data residency with VPC Service Controls for strict data isolation.
- **Audit-Ready Workflows:** Not just a dashboard — a governance engine. Includes a One-Click OJK PDF Generator, mandatory HITL oversight modal for high-risk AI tools, and automated RoPA generation backed by data flow evidence.
- **AI Enablement Platform:** Goes beyond detection to provide an Approved AI Catalog, Self-Service Request Portal, AI Sandbox for tool evaluation, and Employee Nudge Engine — reducing Shadow AI at its root cause by making the official path easier than the shadow path. [Amendment #1, #5, #7]
- **Cost Intelligence:** Tracks what AI tools cost the organization, identifies duplicate subscriptions and zombie licenses, and provides Day-1 ROI proof points for CFO conversations. [Amendment #3]
- **Zero-Loss Resilience:** Local event buffers with write-ahead logging ensure no telemetry is lost during network outages — critical for Indonesian infrastructure outside Jakarta. [Amendment #8]
- **SOC Integration:** 17 webhook event types, REST API, native SIEM connectors (Chronicle, Splunk, Elastic, Wazuh), 6 SOAR playbook templates, and bidirectional ticketing (Jira, ServiceNow) embed Shadow AI intelligence into existing security workflows. [Amendment #6]
- **85% Cost Advantage:** At approximately $5,760/year, priced at a fraction of enterprise alternatives ($50K+/year) while delivering 100% more Indonesian regulatory specificity.

### 1.2 Problem Statement

Indonesian mid-market enterprises (200 to 2,000 employees) face uncontrolled proliferation of unauthorized AI tools. Marketing uses ChatGPT for content, Sales leverages Claude for proposals, Support installs AI browser extensions for auto-replies — all without IT knowledge. This creates three compounding risks:

- **Data Leakage:** Sensitive corporate and customer information flows to unvetted third-party AI models without Data Processing Agreements.
- **Regulatory Non-Compliance:** UU PDP fines of up to 2% of revenue are active. POJK 30/2025 becomes enforceable July 1, 2026. Organizations without automated audit trails face sanctions.
- **Operational Blind Spots:** Existing enterprise tools (CloudEagle, Torii, Portal26) cost $50K+/year, lack Indonesian regulatory templates, and miss endpoint-level and MCP-level AI usage entirely.

### 1.3 Success Criteria

| Metric | Target | Measurement |
|---|---|---|
| Compliance Milestone | All Tier-1 beta partners generate compliant POJK 30/2025 Risk Profile by July 31, 2026 | Report submission verification |
| Detection Efficacy | 98%+ of autonomous agents (Agentic AI) identified within 5 minutes of execution | Heuristic engine benchmarks |
| DPO Time Reduction | RoPA maintenance reduced from 40 hours/month to under 1 hour | Task timer comparison |
| Time-to-First-Discovery | Under 30 minutes from onboarding completion | Platform telemetry |
| Shadow AI Coverage | 95%+ of actual AI usage detected across all five vectors | Red team comparison audit |
| Customer Activation | 50 paying clients by Q4 2026 | Billing system |
| Churn Rate | Under 5% monthly | Subscription analytics |
| Mean Time to Triage | Under 2 hours from detection to governance action | Workflow audit logs |
| Catalog Adoption [Am.1] | 60%+ of employees access the approved catalog monthly | Portal analytics |
| Shadow AI Reduction [Am.1+7] | 50% decrease in new Shadow AI discoveries within 90 days of catalog launch | Discovery trend comparison |
| MCP Server Detection [Am.2] | 95%+ of active MCP servers detected within 15 minutes | Red team audit |
| Cost Savings Identified [Am.3] | Average Rp 100M/year in optimization opportunities per client within 90 days | Consolidation + waste reclaim |
| PII Detection Accuracy [Am.4] | 95%+ detection rate with under 5% false positive rate for KTP and NPWP | Test suite + production sampling |
| Evidence-Backed Decisions [Am.5] | 90%+ of approve/ban decisions have an attached Sandbox Evaluation Report | Decision audit |
| SIEM Connector Usage [Am.6] | 40%+ of organizations connect at least 1 SIEM within 60 days | Connector analytics |
| AUP Acknowledgement [Am.7] | 95%+ of detected AI users acknowledge policy within 30 days | Acknowledgement records |
| Zero-Loss Guarantee [Am.8] | 100% of events recovered after outages of up to 7 days | Backfill completion audit |

---

## 2. Context and Background

### 2.1 Why Now: The Compliance Cliff of 2026

- **OJK Enforcement Deadline:** POJK 30/2025 mandates all FSTI platforms submit biannual AI risk profiles. Semester 1 report due via OJK Sipeduli/Silet portal by July 31, 2026. Regulation fully enforceable July 1, 2026.
- **UU PDP Fines are Active:** Administrative fines up to 2% of annual revenue for organizations failing to maintain accurate Records of Processing Activities. Fully enforced since October 2024. PDP Agency establishment targeted for 2026.
- **Presidential AI Regulation Incoming:** Indonesia's first comprehensive AI regulation (Perpres on AI Ethics and Safety) slated for early 2026 — moving from voluntary guidelines to mandatory governance for high-risk AI systems.
- **ISO 42001 Demand Gap:** Indonesian firms pursuing international contracts are asked for ISO 42001 (AIMS) certification but lack tools to bridge local compliance with global standards.
- **Agentic AI Emergence:** 2026 marks the rise of autonomous AI agents operating without human prompts. Gartner predicts 40% of enterprise applications will feature task-specific AI agents by end of 2026, up from under 5% in 2025.
- **MCP as the New Attack Surface [Am.2]:** Model Context Protocol integrations can be created by anyone, expanding the attack surface beyond enterprise-approved systems. 86% of organizations have no visibility into AI data flows through MCP servers.

### 2.2 Competitive Landscape

| Competitor | Price/Year | ID Compliance | Cloud API | DNS | Browser | Endpoint OS | MCP (Am.2) | Agentic AI | Enablement (Am.1) | Cost Intel (Am.3) |
|---|---|---|---|---|---|---|---|---|---|---|
| CloudEagle | $50K+ | No | Yes | No | Yes | No | No | No | No | Partial |
| Kirin (Knostic) | Enterprise | No | Yes | No | No | Yes | No | Yes | No | No |
| Portal26 | Enterprise | No | No | No | Yes | No | No | No | No | No |
| Obsidian Security | Enterprise | No | No | No | Yes | No | No | No | No | No |
| Teramind | $15K+ | No | Partial | No | Yes | Partial | No | No | No | No |
| Reco.ai | Enterprise | No | Yes | No | No | No | No | No | No | No |
| Nudge Security | $10K+ | No | Yes | No | No | No | Partial | No | No | No |
| **Our Platform** | **~$5.7K** | **Yes** | **Yes** | **Yes** | **Yes** | **Yes** | **Yes** | **Yes** | **Yes** | **Yes** |

Our competitive moat: the only platform combining Penta-Vector discovery, Indonesian regulatory automation, Agentic AI heuristic detection, MCP protocol monitoring, AI enablement catalog, cost intelligence, and mid-market pricing.

### 2.3 Market Intelligence

- **Shadow AI is Pervasive:** Over 60% of enterprise users rely on personal, unmanaged AI tools. Traditional monitoring misses approximately 33% of shadow SaaS because it does not track in-browser activity.
- **Embedded AI is the Hidden Threat:** SaaS platforms (Atlassian, Zendesk, Airtable) are silently embedding AI features — enabling data processing by third-party models without triggering security reviews. One analysis found approximately 70,000 undiscovered AI interactions in just 30 days.
- **Breach Cost Premium:** Shadow AI breaches add an average of $670,000 per incident (IBM). One in five breaches is attributed to shadow AI.
- **AI Spend Surging [Am.3]:** AI-native app spend surged 393% year-over-year in large enterprises. 34% of employees expense unapproved AI tools. 30 to 40% of SaaS licenses go unused.
- **MCP is Exploding [Am.2]:** MCP integrations can grant AI agents powerful operational capabilities. RSA Conference 2026 submissions were dominated by MCP security concerns. The big new risk is prompt injection/context manipulation that steers agents into unsafe tool use.
- **Enablement Beats Prohibition [Am.1]:** Healthcare organizations that provided approved AI alternatives saw 89% reductions in unauthorized use. 27% of employees say unapproved tools simply offer better functionality.

---

## 3. Target Audience and Personas

### Persona A: The Fintech Compliance Officer

- **Context:** Facing the July 1, 2026 deadline for POJK 30/2025 biannual AI risk profile submissions.
- **Pain Point:** Assembles risk reports manually from spreadsheets and emails — 2 to 3 weeks per cycle.
- **Success:** Generate OJK-compliant Semester Risk Profile PDF in under 5 minutes directly from discovery data.

### Persona B: The IT Administrator / Security Officer

- **Context:** Responsible for 500+ employee organization's technology stack and security posture.
- **Pain Point:** Discovers unauthorized AI tools only during annual audits. Zero real-time visibility. Cannot detect CLI-based AI agents, local LLMs, or MCP servers running on developer machines.
- **Success:** Under 30-minute time-to-first-discovery. Continuous monitoring replaces quarterly audits. Full Penta-Vector visibility including MCP.

### Persona C: The Data Protection Officer (DPO)

- **Context:** Legally liable under UU PDP for unmapped data processing activities.
- **Pain Point:** Spends 40+ hours/month maintaining RoPA manually as new AI tools appear weekly. Cannot prove where sensitive data flows.
- **Success:** Automated RoPA maintenance reduces effort to under 1 hour/month. Data flow map [Am.4] shows exactly where PII goes. Evidence-backed RoPA entries, not self-reported guesses.

### Persona D: The CTO of an Exporting Startup

- **Context:** Needs ISO 42001 certification to win contracts in US/EU markets.
- **Pain Point:** No tooling to map AI usage to ISO 42001 Clause 8.1 inventory or produce Statement of Applicability.
- **Success:** ISO 42001 Certification-Ready documentation pack generated from platform data.

### Persona E: The CFO / Finance Director [Am.3]

- **Context:** AI spend is the fastest-growing SaaS line item but entirely invisible to finance.
- **Pain Point:** Departments purchasing AI subscriptions on corporate cards without centralized visibility. Duplicate tools, zombie licenses, usage-based cost surprises.
- **Success:** AI Spend Dashboard shows total cost, duplicates, and waste. Day-1 ROI proof: "We found Rp 85M/year in savings."

### Target Organization Profile

- **Size:** 200 to 2,000 employees (mid-market sweet spot)
- **Industries:** Fintech, Banking, Logistics, E-commerce, Insurtech, SaaS
- **Geography:** Indonesian-headquartered, with growing international operations
- **IT Maturity:** Uses Google Workspace or Microsoft 365, managed Chrome browsers, and Slack/Teams

---

## 4. The Penta-Vector Discovery Model

To ensure comprehensive coverage, the system aggregates data from five distinct sensors — each targeting a different attack surface where Shadow AI enters the organization.

| Vector | Target | Mechanism | What It Catches |
|---|---|---|---|
| A: Cloud API | SaaS integrations (G-Workspace, M365, Slack) | Cloud Functions polling OAuth scopes and service-principal permissions | App-to-App Shadow AI (e.g., AI CRM plugin) that never touches local hardware |
| B: Network DNS | Network traffic on corporate Wi-Fi | GCS ingestion of Firewall/DNS logs matched against AI Signature DB | Personal-account AI usage on non-managed devices connected to corporate network |
| C: Browser Extension | Managed and unmanaged browser profiles | Manifest V3 extension monitoring DOM, network requests, and PII patterns [Am.4] | AI browser sidebars, web-based autonomous agents, embedded SaaS AI features, sensitive data in prompts |
| D: Endpoint OS | Non-browser processes (CLI tools, Python scripts, Local LLMs) | Go-based binary monitoring outbound socket calls, process-to-PID mapping, and behavioral heuristics | Headless Agentic AI (AutoGPT, Aider, Claude Code) running in terminal or as background services |
| E: MCP Protocol [Am.2] | MCP client-server connections (local and remote) | Process scanning + localhost JSON-RPC port probing + manifest collection + config file watching | Shadow MCP servers, over-permissioned tokens, tool poisoning, unvetted community connectors |

### Cross-Vector Correlation and De-Duplication

All sensor telemetry streams into Cloud Dataflow (Apache Beam) for cross-vector correlation:

- **De-Duplication:** Merges telemetry when multiple sensors flag the same AI usage event, preventing duplicate alerts and inflated counts.
- **Behavioral Profiler:** Calculates Heartbeat density (requests per second) to distinguish human typing speed from machine-speed autonomous loops.
- **Chain-of-Thought Patterning:** Identifies Agentic signatures by tracking rapid alternating calls between Completion APIs and Research APIs.
- **Entropy Analysis:** Measures request entropy to detect automated patterns that differ from organic human browsing behavior.
- **MCP Threat Analysis [Am.2]:** Detects tool description mutations (poisoning indicators), privilege escalation chains, and anomalous invocation patterns correlated with OS process data.
- **PII Tag Processing [Am.4]:** Enriches events with data classification tags, GeoIP destination resolution, and UU PDP Art. 56 cross-border transfer detection.
- **Cost Enrichment [Am.3]:** Looks up Signature DB pricing data and applies 3-tier cost estimation (Actual/Reported/Estimated).
- **Policy Checking [Am.1]:** Validates tier compliance, enforces allowlists/blocklists, and triggers auto-approve for low-risk tools.

---

## 5. User Stories

### 5.1 Base PRD User Stories (US-1 through US-7)

| ID | Title | As a... | I want to... | So that... |
|---|---|---|---|---|
| US-1 | Penta-Vector Shadow AI Discovery | IT Admin | Platform scans all 5 vectors automatically | Every AI tool detected within 30 minutes of setup |
| US-2 | Agentic AI Detection via Behavioral Heuristics | Compliance Manager | Platform detects autonomous AI agents via Heartbeat/Entropy heuristics | 98%+ detection within 5 minutes; comply with OJK Banking Guidelines |
| US-3 | Risk Triage and HITL Governance | Security Officer | Review each tool and document human oversight decisions | Every action creates defensible audit trail for OJK compliance |
| US-4 | One-Click OJK Compliance Report | Fintech Compliance Officer | Generate POJK 30/2025 Semester Risk Report in under 5 minutes | Meet July 31 deadline with zero manual compilation |
| US-5 | UU PDP RoPA Automation | DPO | Platform auto-maintains Record of Processing Activities per tool | Comply with UU PDP Art. 35 without manual data entry |
| US-6 | Real-Time Alerting | IT Admin | Immediate email alert for high-risk AI tools | Respond within hours, not weeks |
| US-7 | Weekly Executive Report | IT Management | Automated weekly PDF summarizing Shadow AI footprint | Present compliance status to leadership without manual work |

### 5.2 Amendment User Stories (US-8 through US-40)

**Amendment #1: Approved AI Catalog and Self-Service Request Portal (US-8 to US-11)**

| ID | Title | Summary |
|---|---|---|
| US-8 | Approved AI Tool Catalog | Employee browses vetted tools with safety badges, categories, and tier levels |
| US-9 | Self-Service AI Tool Request | Employee submits URL for 60-second automated pre-screening with risk-based routing |
| US-10 | Tiered AI Usage Policy Engine | Admin defines data sensitivity tiers; tools auto-mapped; violations detected |
| US-11 | Discovery-to-Catalog Conversion | One-click convert discovered Shadow AI tool into Approved Catalog entry |

**Amendment #2: MCP Server Monitoring — Vector E (US-12 to US-15)**

| ID | Title | Summary |
|---|---|---|
| US-12 | Shadow MCP Server Discovery | Detect all local and remote MCP servers with risk scoring |
| US-13 | MCP Permission Audit | Audit credentials, scopes, and tokens; flag over-permissioned configs |
| US-14 | MCP Policy Enforcement | Admin-configurable allowlist; unauthorized servers trigger alerts |
| US-15 | MCP Threat Detection | Detect prompt injection, tool poisoning, anomalous invocations, escalation chains |

**Amendment #3: AI Cost Intelligence Module (US-16 to US-20)**

| ID | Title | Summary |
|---|---|---|
| US-16 | AI Spend Dashboard | CFO sees total AI spend by tool, department, and status with trends |
| US-17 | Duplicate and Overlap Detection | Identify same-category tools across teams; recommend consolidation |
| US-18 | License Waste Detection | Flag zombie licenses (30+ days unused); calculate reclaim value |
| US-19 | AI Spend Alerts | Configurable thresholds at 80% and 100%; prevent budget overruns |
| US-20 | Expense Data Integration | CSV upload correlates expense data with platform discoveries |

**Amendment #4: Prompt-Level Data Flow Tracing (US-21 to US-25)**

| ID | Title | Summary |
|---|---|---|
| US-21 | Data Flow Visibility | DPO sees Sankey diagram: Users to Tools to Destinations, color-coded by sensitivity |
| US-22 | Real-Time PII Leak Detection | Browser extension and OS agent detect sensitive data (10 Indonesian categories) in real-time |
| US-23 | Automated RoPA Evidence | Each RoPA entry auto-enriched with observed data categories, volumes, and destinations |
| US-24 | Cross-Border Data Transfer Monitor | Instant alert when PII flows to non-Indonesian server; Art. 56 compliance check |
| US-25 | Employee In-Browser Warning | Non-blocking overlay warns employee before sending PII to under-tiered tool |

**Amendment #5: Enterprise AI Sandbox Environment (US-26 to US-29)**

| ID | Title | Summary |
|---|---|---|
| US-26 | Sandbox-Based Tool Evaluation | One-click launch 7-day sandbox trial with synthetic data and Penta-Vector monitoring |
| US-27 | Employee Sandbox Access | Requesting employee tests tool with realistic synthetic data; provides structured feedback |
| US-28 | Automated Sandbox Evaluation Report | 7-section behavioral risk report with composite score auto-generated at trial end |
| US-29 | Sandbox-to-Catalog Fast Track | Successful evaluation converts directly to Approved Catalog entry with evidence attached |

**Amendment #6: SIEM/SOAR Integration and Webhook API (US-30 to US-33)**

| ID | Title | Summary |
|---|---|---|
| US-30 | Webhook Event Streaming | Stream all 17 event types to customer endpoints with HMAC signing and retry logic |
| US-31 | SIEM Log Forwarding | Shadow AI alerts appear in SIEM (Chronicle, Splunk, Elastic, Wazuh, Sentinel) alongside other security events |
| US-32 | SOAR Automated Response | 6 pre-built playbooks for common Shadow AI scenarios (XSOAR, Sentinel, generic JSON) |
| US-33 | Ticketing Auto-Creation | Platform alerts auto-create Jira tickets with bidirectional status sync |

**Amendment #7: Employee Education and Policy Nudge Engine (US-34 to US-37)**

| ID | Title | Summary |
|---|---|---|
| US-34 | Automated Nudge Notifications | 7 nudge types auto-triggered; bilingual (English + Bahasa Indonesia); frequency-capped |
| US-35 | AI Acceptable Use Policy Distribution | Rich-text AUP editor with auto-distribution and click-to-acknowledge tracking |
| US-36 | Department Compliance Scorecard | Gamified monthly score (0 to 100) from 5 weighted factors; Compliance Champion badge |
| US-37 | Employee Personal AI Dashboard | "My AI" page: detected tools, personal compliance score, AUP status, tool requests |

**Amendment #8: Offline/Degraded Mode for Local Agents (US-38 to US-40)**

| ID | Title | Summary |
|---|---|---|
| US-38 | Zero-Loss Telemetry During Outages | All events preserved in encrypted local buffer during outages; backfill on recovery |
| US-39 | Agent Health Visibility | Per-agent Online/Degraded/Offline status with buffer utilization and uptime history |
| US-40 | Local Critical Alerting | Critical detections (MCP, Agentic, PII) trigger local SMTP/syslog alerts during offline mode |

---

## 6. Functional Requirements

### 6.1 Complete FR Registry

Total: **77 Functional Requirements** (24 base + 53 from amendments. FR-22 superseded by Amendment #4.)

**P0 — Must-Have (MVP, Q2 2026): 15 FRs (base) + 6 FRs (Am.8)**

| ID | Requirement | Source |
|---|---|---|
| FR-1 | Cloud API Polling: Scan G-Workspace, M365, Slack for OAuth integrations | PRD v3.0 |
| FR-2 | DNS Signature Matching: Ingest firewall/DNS logs against 200+ AI domains | PRD v3.0 |
| FR-3 | Browser Extension Scan: Manifest V3 DOM/network monitoring with PII permissions flagging | PRD v3.0 |
| FR-4 | Agentic AI Detection: Heartbeat density + Entropy + Chain-of-Thought heuristics | PRD v3.0 |
| FR-13 | Endpoint OS Monitor: Go binary for process/socket/PID monitoring of CLI tools and local LLMs | PRD v3.0 |
| FR-5 | OJK PDF Generator: One-click SEOJK 4/2025 Semester Risk Report (Sections A to D) | PRD v3.0 |
| FR-6 | UU PDP RoPA Automation: Auto-populate Art. 35 Records of Processing Activities | PRD v3.0 |
| FR-7 | AI Risk Dashboard: Categorize as Approved/Unapproved/High Risk with triage workflow | PRD v3.0 |
| FR-14 | HITL Oversight Modal: Mandatory justification for high-risk AI; creates audit record | PRD v3.0 |
| FR-8 | Authentication and RBAC: Admin, Viewer, Auditor roles with MFA | PRD v3.0 |
| FR-15 | Multi-Tenant Isolation: Firestore namespace + VPC Service Controls | PRD v3.0 |
| FR-9 | Data Residency Check: Cross-check against UU PDP Art. 56 jurisdiction list | PRD v3.0 |
| FR-10 | PII Jurisdiction Alert: Real-time alert when PII processed in non-approved jurisdiction | PRD v3.0 |
| FR-11 | Email Alerts: Immediate notification for high-risk discoveries | PRD v3.0 |
| FR-12 | Weekly PDF Report: Automated compliance summary every Monday by 8 AM WIB | PRD v3.0 |
| FR-72 | Local Event Buffer: BoltDB + AES-256 + LZ4 + write-ahead logging (500 MB default) | Amendment #8 |
| FR-73 | Connectivity Health Monitor: Online/Degraded/Offline state machine | Amendment #8 |
| FR-74 | Backfill Sync Protocol: Throttled batch replay on recovery | Amendment #8 |
| FR-75 | Local Critical Alert: SMTP/syslog/webhook during offline for critical detections | Amendment #8 |
| FR-76 | Agent Health Dashboard: Per-agent status, buffer utilization, uptime chart | Amendment #8 |
| FR-77 | Browser Extension Offline Buffer: IndexedDB (50 MB) with auto-sync on recovery | Amendment #8 |

**P1 — Should-Have (Q3 2026): 36 FRs (4 base P1 + 32 from Amendments #1, #2, #3, #4, #7)**

| ID | Requirement | Source |
|---|---|---|
| FR-16 | ISO 42001 AIMS Dashboard: Clause 8.1 inventory + Annex A SoA | PRD v3.0 (P1) |
| FR-17 | Embedded SaaS AI Detection: Monitor AI features in approved platforms | PRD v3.0 (P1) |
| FR-18 | Automated Domain Blocking: Firewall integration for banned tools | PRD v3.0 (P1) |
| FR-19 | Data Sovereignty Tracker: Real-time cross-border flow monitoring | PRD v3.0 (P1) |
| FR-25 | Approved AI Catalog: Employee-facing portal with safety badges and tiers | Amendment #1 |
| FR-26 | Self-Service Request Portal: 60-second automated pre-screening (6 parallel checks) | Amendment #1 |
| FR-27 | Auto-Approve Pipeline: Low-risk auto-approved; Medium to triage; High to HITL | Amendment #1 |
| FR-28 | Tiered Usage Policy Engine: Tier 1/2/3 with graduated enforcement | Amendment #1 |
| FR-29 | Discovery-to-Catalog Conversion: One-click with auto-populated metadata | Amendment #1 |
| FR-30 | Request Status Tracking: Real-time employee status updates | Amendment #1 |
| FR-31 | Local MCP Server Detection: Process scanning + JSON-RPC handshake | Amendment #2 |
| FR-32 | Remote MCP Server Detection: Cross-vector DNS + OS + protocol fingerprint | Amendment #2 |
| FR-33 | MCP Manifest Scanner: Index tools, resources, prompts per server | Amendment #2 |
| FR-34 | MCP Permission Auditor: Scope analysis, stale credentials, shared accounts | Amendment #2 |
| FR-35 | MCP Allowlist Engine: Admin-configurable approved packages and URLs | Amendment #2 |
| FR-36 | MCP Threat Detector: Anomaly detection, description mutations, escalation chains | Amendment #2 |
| FR-37 | MCP Dashboard Integration: Dedicated MCP Servers section in Discovery tab | Amendment #2 |
| FR-38 | AI Spend Dashboard: Cost by tool, department, status with trend chart | Amendment #3 |
| FR-39 | Signature DB Pricing Layer: Per-user pricing for 200+ tools, monthly updated | Amendment #3 |
| FR-40 | Duplicate and Overlap Detector: Category grouping, consolidation recommendations | Amendment #3 |
| FR-41 | License Waste Detector: Zombie licenses (30+ days), reclaim value calculation | Amendment #3 |
| FR-42 | AI Spend Alerts: Configurable thresholds per tool/department/org | Amendment #3 |
| FR-43 | Expense Data Connector: CSV upload, vendor matching, correlation with discoveries | Amendment #3 |
| FR-44 | AI Cost Summary in Weekly Report: Spend overview section auto-populated | Amendment #3 |
| FR-45 | Indonesian PII Detection Engine: 10 data categories, local-execution, regex + structural validation | Amendment #4 |
| FR-46 | Data Flow Telemetry Collector: Per-interaction metadata tags (no content), user/tool/destination | Amendment #4 |
| FR-47 | Data Flow Map: Interactive Sankey visualization, color-coded by sensitivity | Amendment #4 |
| FR-48 | Cross-Border Transfer Alert: PII + non-Indonesia destination detection | Amendment #4 |
| FR-49 | In-Browser Employee Warning: Non-blocking overlay with suggested alternative | Amendment #4 |
| FR-50 | RoPA Evidence Enrichment: Auto-populate with observed data categories and destinations | Amendment #4 |
| FR-51 | Admin-Configurable Detection Rules: Custom keywords, thresholds, confidential markers | Amendment #4 |
| FR-67 | Nudge Engine: 7 types, bilingual, frequency-capped, delivery tracked | Amendment #7 |
| FR-68 | AI Acceptable Use Policy Engine: Editor, auto-distribution, acknowledgement tracking | Amendment #7 |
| FR-69 | Department Compliance Scorecard: 5-factor monthly score, leaderboard, badges | Amendment #7 |
| FR-70 | Employee My AI Portal Page: Personal tools, score, AUP status, Suggest a Tool | Amendment #7 |
| FR-71 | Nudge Analytics Dashboard: Effectiveness metrics (delivery, open, click, adoption rates) | Amendment #7 |

**P1 — Superseded**

| ID | Original | Status |
|---|---|---|
| FR-22 | DLP Prompt Monitoring (PRD v3.0 P2) | **SUPERSEDED** by Amendment #4 (FR-45 through FR-51). Elevated from P2 to P1 with comprehensive specification. |

**P2 — Nice-to-Have (Q4 2026): 19 FRs (4 base P2 + 7 Am.5 + 8 Am.6)**

| ID | Requirement | Source |
|---|---|---|
| FR-20 | EU AI Act Risk Classification: Auto-label high-risk use cases | PRD v3.0 |
| FR-21 | NIST AI RMF Mapping: Cross-reference with gap analysis | PRD v3.0 |
| FR-23 | Bahasa Indonesia Localization: Full UI translation | PRD v3.0 |
| FR-24 | White-Label Consultant Portal: Multi-org management for DPO firms | PRD v3.0 |
| FR-52 | Sandbox Provisioner: One-click Cloud Run container launch with sensors | Amendment #5 |
| FR-53 | Synthetic Data Engine: Indonesian-localized Faker + KTP/NPWP generators | Amendment #5 |
| FR-54 | Sandbox Network Monitor: Envoy proxy logging all outbound traffic | Amendment #5 |
| FR-55 | Trial Dashboard: Real-time admin view of sandbox activity | Amendment #5 |
| FR-56 | Sandbox Evaluation Report: 7-section auto-generated PDF with risk score | Amendment #5 |
| FR-57 | Employee Sandbox Portal: Browser-based access with feedback form | Amendment #5 |
| FR-58 | Sandbox-to-Catalog Conversion: One-click fast track with report attached | Amendment #5 |
| FR-59 | Webhook API: 17 event types, HMAC-SHA256, retry, 10 endpoints | Amendment #6 |
| FR-60 | REST API: OAuth 2.0, role-scoped, pagination, 1000 req/hr | Amendment #6 |
| FR-61 | Syslog/CEF Forwarder: RFC 5424 and ArcSight CEF over TLS | Amendment #6 |
| FR-62 | Google Security Operations Connector: Pub/Sub integration | Amendment #6 |
| FR-63 | Splunk Connector: HEC + pre-built app with dashboards | Amendment #6 |
| FR-64 | SOAR Playbook Library: 6 templates (XSOAR, Sentinel, JSON) | Amendment #6 |
| FR-65 | Jira Bidirectional Integration: Auto-create, two-way sync, dedup | Amendment #6 |
| FR-66 | Webhook Health Dashboard: Per-endpoint metrics, test-fire capability | Amendment #6 |

---

## 7. Non-Functional Requirements

### Security

- **Encryption at Rest:** AES-256 via Google Cloud KMS with field-level encryption for PII metadata
- **Encryption in Transit:** TLS 1.3 for all API communications and sensor telemetry
- **Local Buffer Encryption:** AES-256 with agent-derived key [Am.8]
- **VPC Service Controls:** Security perimeter around Firestore, GCS, BigQuery, and Dataflow
- **Penetration Testing:** Quarterly third-party penetration tests

### Multi-Tenancy

- **Data Isolation:** Firestore namespace logic with firm_id root collection. Security Rules enforce boundaries.
- **Zero Cross-Tenant Leakage:** Validated via automated isolation tests

### Performance

- **Telemetry Latency:** Cloud Dataflow processing under 5-minute end-to-end latency
- **Dashboard Load:** Under 3 seconds for full render with 10,000+ discovered tools
- **Pre-Screening [Am.1]:** Under 60 seconds for 6-check automated tool assessment
- **PII Detection [Am.4]:** Under 100ms latency impact on user typing
- **Concurrent Users:** 50 concurrent admin sessions per organization

### Data Sovereignty

- **Jakarta Region Pinning:** Every compute and storage resource in asia-southeast2
- **UU PDP Art. 56:** All data processing complies with local residency requirements
- **Audit Logging:** All actions logged with immutable timestamps. 3-year retention.
- **Privacy-By-Design [Am.4]:** PII scanner runs locally on device. Only classification tags transmitted to cloud. Prompt content NEVER captured.

### Compliance Certifiability

- **SNI 27001:** Architecture designed to be certifiable
- **SOC 2 Type I:** Certification process initiated Q4 2026

---

## 8. HITL Audit Trail Specification

### Data Model

| Field | Type | Description |
|---|---|---|
| audit_id | String (UUID) | Unique identifier for the audit event |
| agent_id | String | Reference to the detected Agent/Tool ID |
| supervisor_id | String | User ID of the assigned human reviewer |
| risk_category | Enum | High, Medium, Low (mapped from EU AI Act risk triage) |
| decision | Enum | APPROVED, BLOCKED, RESTRICTED, PENDING |
| justification | Text | Human-entered reasoning |
| review_timestamp | Timestamp | ISO 8601 UTC |
| evidence_snapshot | Map | Snapshot of heuristic evidence (Heartbeat density, Entropy score) at time of review |

### OJK PDF Mapping Logic

- **Section 3.1 — High-Risk AI Inventory:** All tools where risk_category equals High. OJK requires proof these tools are not operating autonomously.
- **Section 3.2 — Oversight Documentation:** If hitl_logs exists and decision is APPROVED: "Verified and Supervised by [Name] on [Date]." If no log exists: "Alert: Unsupervised High-Risk Activity Detected."
- **Compliance Verification:** review_timestamp compared against detected_at to prove human intervention within 24 to 48 hours (OJK Best Practice 2026)

---

## 9. Technical Architecture

Full architecture specification is maintained in the companion document: **Shadow_AI_Detection_Architecture_v2.md**

### Summary

- **Platform:** GCP Jakarta Region (asia-southeast2), fully serverless
- **Sensors:** Penta-Vector (Cloud API + DNS + Browser + OS + MCP)
- **Processing:** Cloud Dataflow (Apache Beam) with 8-stage pipeline
- **Storage:** Firestore (36 collections, multi-tenant) + BigQuery (6 tables, 3-year retention) + AI Signature DB (200+ entries, weekly updated)
- **Application:** Next.js on Cloud Run + 11 Cloud Functions + Better Auth (SSO + RBAC)
- **Integration [Am.6]:** Webhook API (17 events) + REST API + SIEM Connectors + SOAR Playbooks + Jira
- **Resilience [Am.8]:** Local BoltDB buffer + 3-mode health monitor + backfill sync + local critical alerts

---

## 10. Database Schema

### Firestore Collections (36 total)

| Group | Collections | Count |
|---|---|---|
| PRD v3.0 Core | organizations, users, integrations, discovered_apps, hitl_logs, alerts, audit_log, compliance_reports, signature_db | 9 |
| Amendment #1 (Catalog) | approved_catalog, tool_requests, policy_tiers, policy_violations | 4 |
| Amendment #2 (MCP) | mcp_servers, mcp_tools, mcp_credentials, mcp_threats, mcp_allowlist | 5 |
| Amendment #3 (Cost) | ai_cost_entries, cost_thresholds, expense_uploads, expense_matches | 4 |
| Amendment #4 (Data Flow) | detection_rules, employee_warnings | 2 |
| Amendment #5 (Sandbox) | sandbox_trials, sandbox_participants, sandbox_reports | 3 |
| Amendment #6 (Integration) | webhook_endpoints, api_keys, siem_connectors, ticket_links | 4 |
| Amendment #7 (Nudge) | nudge_events, aup_versions, aup_acknowledgements, compliance_scores, tool_suggestions | 5 |

### BigQuery Tables (6 total)

| Table | Purpose | Volume |
|---|---|---|
| sensor_hits | All sensor telemetry (raw processed events) | High |
| hitl_decisions | Complete HITL audit trail with evidence | Medium |
| data_flow_events [Am.4] | Classification tags per interaction (NO content) | Very High |
| data_flow_aggregates [Am.4] | Pre-computed daily/weekly rollups | Medium |
| sandbox_network_logs [Am.5] | Sandbox proxy traffic logs | High (per trial) |
| webhook_deliveries [Am.6] | Webhook delivery tracking (30-day retention) | High |

---

## 11. Design and User Experience

### Admin Dashboard Tabs

| Tab | Content | Amendments |
|---|---|---|
| Overview | Total tools, risk distribution, compliance status, financial impact, enablement metrics, department leaderboard, agent health, HITL pending | Am.1, Am.3, Am.7, Am.8 |
| Discovery | Filterable table (Name, Vector A-E, Risk, Status, Users, Residency, Cost). MCP sub-view. Sandbox launch. Catalog conversion. | Am.2, Am.5, Am.1 |
| HITL Audit | All human-in-the-loop decisions with evidence viewer | PRD v3.0 |
| Costs [Am.3] | Spend dashboard, overlap analysis, zombie licenses, expense correlation | Amendment #3 |
| Data Flows [Am.4] | Sankey diagram (Users to Tools to Destinations), cross-border monitoring | Amendment #4 |
| Catalog [Am.1] | Admin catalog management, request pipeline metrics | Amendment #1 |
| Integrations | Per-sensor health, buffer utilization, SIEM/SOAR status, webhook health | Am.6, Am.8 |
| Reports | OJK Semester, RoPA, Weekly PDF, ISO 42001 (future) | PRD v3.0 |
| Settings | Org profile, RBAC, policy tiers, MCP allowlist, AUP editor, webhooks, API keys, SIEM config, nudge templates, detection rules | All |

### Employee Portal Pages [Am.1 + Am.7]

| Page | Content |
|---|---|
| Catalog | Approved tools with safety badges, categories, tier indicators, search/filter |
| Request a Tool | URL submission, 60-second pre-screening, status tracker |
| My AI [Am.7] | Personal detected tools, compliance score, AUP status, requests, Suggest a Tool |

### Governance Lifecycle

DISCOVERED > REVIEW > SANDBOX_ACTIVE [Am.5] > SANDBOX_COMPLETE [Am.5] > APPROVED (+ Catalog [Am.1]) / BANNED / RESTRICTED

---

## 12. Implementation Roadmap

### MVP Sprint Plan (Q2 2026)

| Sprint | Deliverables | Duration |
|---|---|---|
| Sprint 1 | GCP Infrastructure: Terraform, Firestore multi-tenant, VPC, KMS, Jakarta pinning | 2 weeks |
| Sprint 2 | Sensor Alpha: Browser Extension (MV3) + DNS Ingestor + Cloud API OAuth. **+ Local Event Buffer [Am.8]** | 3 weeks + 1w |
| Sprint 3 | Heuristic Engine: Dataflow pipeline, Heartbeat/Entropy, de-duplication, OS Agent MVP. **+ Health Monitor + Backfill [Am.8]** | 3 weeks + 1w |
| Sprint 4 | Reporting Suite: OJK PDF, HITL Modal, RoPA, email alerts, weekly report. **+ Local Critical Alert + Dashboard Health [Am.8]** | 3 weeks + 0.5w |
| Sprint 5 | Integration and Beta Launch: Dashboard UI, RBAC auth, onboarding wizard, beta deployment | 2 weeks |

**MVP Total: approximately 15.5 weeks (13 base + 2.5 Am.8)**

### Post-MVP Amendment Sprints

| Sprints | Amendment | Duration | Target |
|---|---|---|---|
| 6-9 | #1: Approved Catalog + Request Portal + Tiered Policy | 8 weeks | Q3 2026 |
| 10-13 | #2: MCP Vector E (Scanner + Allowlist + Threats + Dashboard) | 8 weeks | Q3 2026 |
| 14-17 | #3: Cost Intelligence (Spend Dashboard + Overlap + Waste + Expense) | 9 weeks | Q3-Q4 2026 |
| 18-21 | #4: Data Flow Tracing (PII Engine + Telemetry + Map + Warnings) | 10 weeks | Q3-Q4 2026 |
| 22-25 | #5: AI Sandbox (Provisioner + Synthetic Data + Trial + Reports) | 9 weeks | Q4 2026 |
| 26-28 | #6: SIEM/SOAR (Webhook + REST API + Connectors + Playbooks + Jira) | 8 weeks | Q4 2026 |
| 29-31 | #7: Nudge Engine (Nudges + AUP + Scorecard + My AI + Analytics) | 6 weeks | Q3-Q4 2026 |

**Total: 5 MVP sprints + 26 amendment sprints + 2.5 weeks enhancement = 73.5 engineering-weeks**

Note: Amendments have significant parallelism opportunities. Am.1 and Am.2 can run concurrently with separate teams. Am.3, Am.4, and Am.7 can overlap. Realistic calendar time with 2 engineering streams: approximately 9 to 12 months.

### Phase Roadmap Summary

| Dimension | Q2 2026 (MVP) | Q3 2026 (Growth) | Q4 2026 (Scale) |
|---|---|---|---|
| Discovery | Penta-Vector (A+B+C+D) + Heuristics + Offline Mode [Am.8] | + Vector E MCP [Am.2] + Embedded SaaS AI + Domain Blocking | + DLP Prompt Monitoring [Am.4] |
| Compliance | OJK POJK 30/2025 + RoPA + HITL | + Data Flow Tracing [Am.4] + Sovereignty Tracker | + ISO 42001 + EU AI Act + NIST |
| Enablement | (Not in scope) | + Approved Catalog [Am.1] + Nudge Engine [Am.7] | + AI Sandbox [Am.5] + Localization |
| Cost Intel | (Not in scope) | + Spend Dashboard + Overlap Detector [Am.3] | + License Waste + Expense Connector [Am.3] |
| Integration | (Not in scope) | (Not in scope) | + Webhook/REST API + SIEM + SOAR + Jira [Am.6] |
| Business | 5 Beta Fintech Clients | 20 Paying Clients | 50 Clients + Self-Serve Billing |

**Critical Milestone:** July 1, 2026 — "Day Zero" POJK 30/2025 enforcement. First submission deadline: July 31, 2026.

---

## 13. Revenue and Pricing Model

| Attribute | Basic Tier (ID Compliance) | Global Tier (ISO 42001) |
|---|---|---|
| Monthly Price | Rp 7,500,000/mo (~$480) | Rp 15,000,000/mo (~$960) |
| Annual Price | Rp 90,000,000/yr (~$5,760) | Rp 180,000,000/yr (~$11,520) |
| Discovery | Penta-Vector (A+B+C+D+E) | Penta-Vector + Embedded SaaS AI |
| OJK Reporting | Included (One-Click PDF) | Included |
| UU PDP RoPA | Included | Included |
| HITL Audit Trail | Included | Included |
| Approved Catalog [Am.1] | Included (up to 500 employees) | Included (up to 2,000 employees) |
| Nudge Engine [Am.7] | Included (English only) | Included (Bilingual + Custom branding) |
| AI Spend Dashboard [Am.3] | Overview + tool-level costs + alerts | + Overlap/Waste/Expense + billing API connectors |
| Data Flow Map [Am.4] | Included | Included |
| Sandbox [Am.5] | 2 concurrent trials | 10 concurrent trials |
| SIEM/SOAR [Am.6] | Webhook (3 endpoints) + REST API (read) + Syslog + Jira | Webhook (10) + REST (full) + All SIEM connectors + SOAR + ServiceNow |
| ISO 42001 / EU AI Act | Not included | Included |
| Domain Blocking | Not included | Included |
| Employee Limit | Up to 500 | Up to 2,000 |
| Support | Email (48h SLA) | Priority (4h SLA) + onboarding call |

---

## 14. Technical Risks and Mitigations

| Risk | Impact | Mitigation |
|---|---|---|
| SaaS API rate limits / breaking changes | Scan delays for Cloud API vector | Retry queues; version-lock API calls; monitor deprecation |
| Chrome Enterprise MDM required for Vector C | Browser monitoring unavailable for non-managed environments | Graceful 4-vector degradation; document MDM prerequisite |
| OS Agent deployment friction (Vector D) | Low endpoint monitoring adoption | Docker one-click installer; Bahasa Indonesia docs |
| Signature DB freshness | Missed new tools | Weekly updates + community submission + Unknown classification |
| Cloud Dataflow scaling | Processing latency exceeds 5-min NFR | Auto-scaling workers; edge pre-aggregation; latency alerting |
| UU PDP implementing regulation still in draft | Compliance requirements may shift | Configurable template engine; 30-day update commitment |
| Presidential AI Regulation (Perpres) | New mandatory requirements | Monitoring plan; modular compliance modules |
| Heuristic false positives [Am.2] | Alert fatigue; admin trust loss | Tunable thresholds per org; confidence scoring |
| MCP protocol evolution [Am.2] | Scanner may miss new MCP transport types | Track MCP spec changes; monthly scanner updates |
| Indonesian network reliability [Am.8] | Data loss during outages | Local BoltDB buffer; 3-mode health monitor; backfill sync |
| Employee nudge fatigue [Am.7] | Employees ignore nudges | Frequency caps; A/B test messaging; measure adoption rates |

---

## 15. Open Questions

### Business and Strategy

| # | Question | Owner | Deadline |
|---|---|---|---|
| 1 | Final product name (placeholder [Project Name] in all docs) | Founders | May 2026 |
| 2 | Pricing validation via customer discovery interviews | Product/Sales | May 2026 |
| 3 | Beta partner LOIs (5 Fintech partners) | Business Dev | April 2026 |
| 4 | Financial projections (12-month revenue, CAC, LTV) | Finance | May 2026 |

### Legal and Compliance

| # | Question | Owner | Deadline |
|---|---|---|---|
| 5 | Legal opinion: OS Agent process monitoring under Indonesian labor law | Legal | April 2026 |
| 6 | Legal opinion: DNS metadata extraction vs UU PDP data minimization | Legal | April 2026 |
| 7 | Legal opinion: MCP manifest reading and credential auditing vs UU ITE | Legal | Before Sprint 10 |
| 8 | Legal opinion: On-device PII scanning as employee monitoring | Legal | Before Sprint 18 |
| 9 | Legal opinion: Auto-approval liability for Low-risk tools [Am.1] | Legal | Before Sprint 7 |
| 10 | Legal opinion: Employee nudge consent under UU PDP [Am.7] | Legal/HR | Before Sprint 29 |
| 11 | Art. 56 jurisdiction database source for cross-border transfers [Am.4] | Legal/Compliance | Sprint 20 |
| 12 | Presidential AI Regulation monitoring plan | Compliance | Ongoing |

### Technical

| # | Question | Owner | Deadline |
|---|---|---|---|
| 13 | BoltDB vs BadgerDB benchmark on Indonesian reference hardware [Am.8] | Engineering | Sprint 2 |
| 14 | MCP config file paths for all major IDEs (VS Code, Cursor, Windsurf, JetBrains) [Am.2] | Engineering | Sprint 10 |
| 15 | JSON-RPC fingerprinting to distinguish MCP from generic JSON-RPC [Am.2] | Engineering | Sprint 10 |
| 16 | Browser extension typing latency with PII scanner active [Am.4] | Engineering | Sprint 18 |
| 17 | Privacy policy NLP scanning: build vs buy [Am.1] | Engineering/Product | Sprint 7 |
| 18 | Indonesian PII patterns: KTP female DOB offset, new NPWP format [Am.4] | Engineering | Sprint 18 |
| 19 | Webhook API versioning strategy [Am.6] | Engineering/Product | Sprint 26 |
| 20 | Sandbox access model: browser-based remote desktop vs URL proxy [Am.5] | Engineering | Sprint 22 |
| 21 | Department hierarchy mapping from G-Workspace/M365 org structure [Am.7] | Product/Engineering | Sprint 30 |

---

## 16. Appendix

### 16.1 Regulatory Reference Index

| Regulation | Description |
|---|---|
| UU PDP (Law No. 27/2022) | Indonesia Personal Data Protection Law. Fully enforced since Oct 17, 2024. Fines up to 2% of revenue. RPP PDP still in draft. |
| POJK 30/2025 | OJK biannual AI risk profile mandate. Effective July 1, 2026. S1 report due July 31, 2026. |
| SEOJK 4/2025 | Report template (Lampiran II Bagian C): 4 sections (Operational, Legal, Strategic, Action Plan). |
| SNI 27001 | Indonesian ISO 27001 equivalent for information security management. |
| ISO 42001 | International AI Management Systems standard. Clause 8.1 inventory, Annex A SoA. |
| SE Menkominfo 9/2023 | Circular on AI Ethics. Only general regulatory guidance for business AI use in Indonesia as of 2026. |
| Perpres on AI | Forthcoming Presidential Regulation on AI Ethics and Safety. Expected 2026. |

### 16.2 Document Statistics

| Metric | Count |
|---|---|
| User Stories | 40 total (7 base + 33 from 8 amendments) |
| Functional Requirements | 77 total (24 base + 53 from amendments; FR-22 superseded) |
| Firestore Collections | 36 |
| BigQuery Tables | 6 |
| Cloud Functions | 11 |
| Cloud Run Services | 3 |
| Webhook Event Types [Am.6] | 17 |
| SOAR Playbook Templates [Am.6] | 6 |
| PII Detection Categories [Am.4] | 10 |
| Nudge Types [Am.7] | 7 |
| MVP Sprints | 5 (+ 2.5 weeks Am.8 enhancement) |
| Amendment Sprints | 26 |
| Total Engineering-Weeks | ~73.5 (significant parallelism possible) |

---

## 17. Required for Acceptance

### Business

- Final product name confirmed
- Pricing validation from customer discovery
- 5 beta partner LOIs signed
- 12-month financial projections

### Legal

- Legal opinions on: OS Agent monitoring, DNS metadata extraction, MCP manifest reading, on-device PII scanning, auto-approval liability, employee nudge consent
- DPA templates for G-Workspace, M365, Slack
- Privacy Policy and Terms of Service
- Default AI Acceptable Use Policy template (Indonesian-compliant)
- Art. 56 jurisdiction source for cross-border assessments

### Technical

- GCP Dataflow and Firestore quota confirmation (Jakarta region)
- OS Agent format decision (Docker vs native Go binary)
- BoltDB/BadgerDB benchmark on reference hardware
- Heuristic calibration for Indonesian usage patterns
- Signature DB v1 (200+ domains with pricing data)
- Indonesian PII test dataset (1,000+ synthetic samples)
- KTP/NIK validation spec (province codes, DOB encoding, female offset)
- Webhook event schema v1 (OpenAPI 3.0)
- CEF field mapping document
- Splunk app package (.spl)
- SOAR playbook test results (6 playbooks)
- Universal expense CSV schema (compatible with Jurnal.id, Accurate, Mekari)

### Design

- Figma mockups: Dashboard (all tabs), Discovery, HITL Modal, Reports, Settings
- Figma mockups: Employee Portal (Catalog, Request, My AI)
- Figma mockups: Data Flow Map (Sankey), Cost Dashboard, Sandbox Trial Dashboard
- HITL Modal interaction design
- Onboarding wizard wireframes
- Employee nudge and warning overlay designs
- Sandbox Evaluation Report PDF template

---

**Document Status:** Final (v4.0)  
**This PRD is the definitive guide for the Shadow AI Detection platform.**
