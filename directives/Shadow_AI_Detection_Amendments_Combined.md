# Shadow AI Detection — Combined Amendments Specification

**Version:** 1.0 (Companion to PRD v4.0 Final)  
**Date:** March 16, 2026  
**Status:** Approved for Implementation  
**Classification:** Confidential — Internal Use Only  
**Scope:** Detailed specifications for Amendments #1 through #8

---

## Document Purpose

This document provides the deep-dive specifications for all 8 PRD amendments. While the PRD v4.0 Final integrates amendment outcomes (user stories, FRs, schema, roadmap) at the summary level, this companion document preserves the full strategic rationale, detailed feature designs, acceptance criteria, open questions, and required-for-acceptance items for each amendment.

Use the PRD v4.0 for the consolidated product view. Use this document for implementation-level detail.

---

## Table of Contents

1. [Amendment Summary Matrix](#1-amendment-summary-matrix)
2. [Amendment #1: Approved AI Catalog and Self-Service Request Portal](#2-amendment-1-approved-ai-catalog-and-self-service-request-portal)
3. [Amendment #2: MCP Server Monitoring — Vector E](#3-amendment-2-mcp-server-monitoring-vector-e)
4. [Amendment #3: AI Cost Intelligence Module](#4-amendment-3-ai-cost-intelligence-module)
5. [Amendment #4: Prompt-Level Data Flow Tracing](#5-amendment-4-prompt-level-data-flow-tracing)
6. [Amendment #5: Enterprise AI Sandbox Environment](#6-amendment-5-enterprise-ai-sandbox-environment)
7. [Amendment #6: SIEM/SOAR Integration and Webhook API](#7-amendment-6-siem-soar-integration-and-webhook-api)
8. [Amendment #7: Employee Education and Policy Nudge Engine](#8-amendment-7-employee-education-and-policy-nudge-engine)
9. [Amendment #8: Offline/Degraded Mode for Local Agents](#9-amendment-8-offline-degraded-mode-for-local-agents)
10. [Cross-Amendment Dependencies](#10-cross-amendment-dependencies)
11. [Consolidated Open Questions](#11-consolidated-open-questions)
12. [Consolidated Required for Acceptance](#12-consolidated-required-for-acceptance)

---

## 1. Amendment Summary Matrix

| # | Amendment | Priority | Sprints | Weeks | User Stories | FRs | DB Tables | Key Deliverable |
|---|---|---|---|---|---|---|---|---|
| 8 | Offline/Degraded Mode | MVP (Q2) | +2.5w to Sprints 2-4 | 2.5 | US-38 to US-40 (3) | FR-72 to FR-77 (6) | 0 new (2 modified) | Zero data loss during network outages |
| 1 | Approved AI Catalog | P1 (Q3) | Sprints 6-9 | 8 | US-8 to US-11 (4) | FR-25 to FR-30 (6) | 4 Firestore | Employee self-service + tiered policy |
| 2 | MCP Vector E | P1 (Q3) | Sprints 10-13 | 8 | US-12 to US-15 (4) | FR-31 to FR-37 (7) | 5 Firestore | Penta-Vector upgrade + MCP threat detection |
| 3 | Cost Intelligence | P1 (Q3-Q4) | Sprints 14-17 | 9 | US-16 to US-20 (5) | FR-38 to FR-44 (7) | 4 Firestore | CFO dashboard + ROI proof |
| 4 | Data Flow Tracing | P1 (Q3-Q4) | Sprints 18-21 | 10 | US-21 to US-25 (5) | FR-45 to FR-51 (7) | 2 Firestore + 2 BigQuery | PII detection + privacy evidence |
| 5 | AI Sandbox | P2 (Q4) | Sprints 22-25 | 9 | US-26 to US-29 (4) | FR-52 to FR-58 (7) | 3 Firestore + 1 BigQuery | Evidence-based tool evaluation |
| 6 | SIEM/SOAR Integration | P2 (Q4) | Sprints 26-28 | 8 | US-30 to US-33 (4) | FR-59 to FR-66 (8) | 4 Firestore + 1 BigQuery | SOC integration + playbooks |
| 7 | Nudge Engine | P1 (Q3-Q4) | Sprints 29-31 | 6 | US-34 to US-37 (4) | FR-67 to FR-71 (5) | 5 Firestore | Behavioral change + AUP compliance |

**Totals:** 33 new user stories, 53 new FRs, 27 new Firestore collections, 4 new BigQuery tables, 60.5 engineering-weeks

---

## 2. Amendment #1: Approved AI Catalog and Self-Service Request Portal

### 2.1 Strategic Rationale

Detection without enablement creates resentment. When the platform bans a tool with no alternative, employees either circumvent controls or lose productivity. This amendment transforms the platform from a surveillance tool into an enablement platform by providing a curated catalog of approved alternatives and a self-service pathway for requesting new tools.

**Key insight:** Healthcare organizations that provided approved AI alternatives saw 89% reductions in unauthorized use. 27% of employees say unapproved tools simply offer better functionality — give them a better approved option and Shadow AI drops organically.

### 2.2 Feature Design

**Approved AI Catalog (Employee-Facing Portal)**

- Grid/list view of all IT-approved AI tools with safety badges
- Categories: Writing, Code, Design, Research, Data Analysis, Customer Support, Translation
- Tier indicators: "Approved for: Public Data", "Approved for: Internal Data", "Approved for: Confidential Data"
- Search and filter by category, tier, and use case
- Each entry includes: tool name, description, safety badge, data tier, use case, link to access

**Self-Service Tool Request Portal**

- Employee submits a URL of the tool they want evaluated
- 60-Second Pre-Screening Engine runs 6 parallel checks: Signature DB lookup, Privacy policy URL check, TLS certificate validation, Known vulnerability check, Data residency lookup, Terms of service AI clause scan
- Risk-based routing: Low Risk → auto-approve for Tier 1 (IT notified), Medium Risk → IT triage queue (48h SLA), High Risk → HITL review required (5-day SLA, sandbox recommended)

**Tiered AI Usage Policy Engine**

- Tier 1 (Public Data): Tools cleared for marketing copy, public research, generic writing
- Tier 2 (Internal Data): Tools cleared for internal docs, meeting notes, project planning
- Tier 3 (Confidential Data): Tools with DPA, SOC 2, and data residency confirmation
- Graduated enforcement: 1st violation = educational nudge (Am.7), 2nd = admin notification, 3rd = HITL escalation
- Each discovered tool auto-mapped to a tier based on its risk score and scope

**Discovery-to-Catalog Conversion**

- One-click convert a discovered Shadow AI tool into an Approved Catalog entry
- Auto-populates metadata from discovery data (name, vendor, risk score, users)
- Admin adds: approved tier, use case description, access instructions, alternative suggestions

### 2.3 User Stories with Acceptance Criteria

**US-8: Approved AI Tool Catalog**
- Employee browses approved tools without admin credentials (SSO access)
- Grid/list toggle with category filter and search
- Each tool displays: name, safety badge, tier level, use case, link
- Minimum 10 approved tools seeded at launch (from common discoveries)

**US-9: Self-Service AI Tool Request**
- Employee submits URL → 60-second pre-screening → risk classification
- Status tracker: Submitted → Screening → Under Review → Approved/Denied
- Denial includes: reason + suggested alternative from catalog
- Pre-screening results visible to admin with full check details

**US-10: Tiered AI Usage Policy Engine**
- Admin defines 3 tiers with required attributes per tier
- Discovered tools auto-mapped to tiers based on risk score
- Violations detected when tool used above its tier clearance
- Graduated enforcement enforced automatically

**US-11: Discovery-to-Catalog Conversion**
- One-click from Discovery table converts tool to Catalog entry
- Auto-populated fields from discovery data
- Admin completes remaining fields (tier, use case, instructions)
- Conversion logged in audit trail

### 2.4 Functional Requirements

| ID | Requirement | Acceptance |
|---|---|---|
| FR-25 | Approved AI Catalog: Employee-facing portal with safety badges, categories, tier indicators, search/filter | Page renders under 2 seconds with 100+ catalog entries |
| FR-26 | Self-Service Request Portal: URL submission triggers 60-second pre-screening with 6 parallel checks | All 6 checks complete under 60 seconds. Risk classification accurate for 90%+ of known tools |
| FR-27 | Auto-Approve Pipeline: Low-risk auto-approved for Tier 1. Medium routed to IT triage. High routed to HITL. | Zero false auto-approvals for Medium/High risk tools |
| FR-28 | Tiered Usage Policy Engine: 3 configurable tiers with graduated enforcement | Tier violation detected within 1 processing cycle (under 5 minutes) |
| FR-29 | Discovery-to-Catalog Conversion: One-click with auto-populated metadata from discovery | Conversion completes in under 10 seconds with all available metadata populated |
| FR-30 | Request Status Tracking: Real-time employee updates via portal and email | Status update delivered within 60 seconds of state change |

### 2.5 Database Schema

| Collection | Key Fields | Notes |
|---|---|---|
| approved_catalog | id, org_id, app_name, vendor, category, tier_level, use_case, safety_badge, access_url, added_by, source_discovery_id (optional) | Employee-facing. No sensitive data. |
| tool_requests | id, org_id, user_id, submitted_url, screening_result (6 check results), risk_classification, status (submitted/screening/review/sandbox/approved/denied), reviewer_id, resolution_note, alternative_id | Full audit trail for each request |
| policy_tiers | id, org_id, tier_level (1/2/3), label, required_attributes (DPA/SOC2/residency/etc), max_data_sensitivity | Admin-configurable per organization |
| policy_violations | id, org_id, user_id, tool_id, tier_violated, data_sensitivity_detected, action_taken (nudge/admin/hitl), violation_count | Links to nudge_events (Am.7) |

### 2.6 Roadmap

| Sprint | Deliverables | Duration |
|---|---|---|
| Sprint 6 | Approved Catalog: Employee Portal UI, catalog CRUD, safety badge system, category/tier engine | 2 weeks |
| Sprint 7 | Pre-Screening Engine: 6-check parallel pipeline, Signature DB integration, risk classification, request workflow | 2 weeks |
| Sprint 8 | Tiered Policy Engine: 3-tier definition, auto-mapping, violation detection, graduated enforcement logic | 2 weeks |
| Sprint 9 | Integration: Discovery-to-Catalog conversion, request status notifications, employee onboarding flow, UAT | 2 weeks |

### 2.7 Open Questions

| # | Question | Owner |
|---|---|---|
| 1 | Privacy policy NLP scanning: build vs buy for automated ToS analysis? | Engineering/Product |
| 2 | Auto-approval liability: if a low-risk auto-approved tool later causes a breach, what is the platform's liability? | Legal |
| 3 | Catalog seeding: should we pre-populate with 50+ globally common tools or start empty? | Product |

---

## 3. Amendment #2: MCP Server Monitoring — Vector E

### 3.1 Strategic Rationale

MCP (Model Context Protocol) represents a new attack surface where AI agents gain operational capabilities through tool and resource access. A single MCP server can grant an AI agent the ability to read files, execute code, query databases, and make API calls — all without appearing in browser monitoring, DNS logs, or OAuth scopes. This amendment upgrades the Quad-Vector model to a Penta-Vector model by adding dedicated MCP protocol monitoring.

**Key insight:** MCP integrations can be created by anyone, run on any developer machine, and grant broad permissions to AI models. 86% of organizations have no visibility into AI data flows through MCP servers.

### 3.2 Detection Mechanisms

**Local MCP Server Detection**

- Process scanning: identify processes listening on localhost ports commonly used by MCP (configurable port list)
- JSON-RPC handshake probe: send MCP initialize request to candidate ports, confirm MCP protocol response
- Config file watching: monitor known MCP config paths (~/.cursor/mcp.json, VS Code settings, JetBrains config) for new server entries
- Trigger: every 60 seconds (process scan) + on-demand (config file inotify watcher)

**Remote MCP Server Detection**

- Cross-vector correlation: DNS sensor (Vector B) flags connections to known MCP hosting domains
- OS agent (Vector D) identifies outbound connections to remote MCP server URLs
- Protocol fingerprinting: distinguish MCP JSON-RPC from generic JSON-RPC by initialize/capabilities handshake pattern

**MCP Manifest Scanner**

- Sends tools/list and resources/list to discovered servers
- Indexes all available tools with descriptions, input schemas, and scope requirements
- Hashes tool descriptions for mutation detection (poisoning indicator)
- Maps tool capabilities to risk categories (file_access, code_execution, api_calls, database_queries)

**MCP Threat Detection**

- Description mutation: compare tool description hashes over time to detect prompt injection via modified tool descriptions
- Privilege escalation chains: correlate MCP tool invocations across time to identify escalation patterns (read → write → execute)
- Anomalous invocation patterns: statistical baseline of tool call frequency/timing to detect automated exploitation
- Credential exposure: flag servers with hardcoded tokens, shared credentials, or overly broad scopes

### 3.3 User Stories with Acceptance Criteria

**US-12: Shadow MCP Server Discovery**
- 95%+ of active local MCP servers detected within 15 minutes
- Remote MCP servers detected via DNS + OS cross-vector correlation
- Each server displays: type (local/remote), transport, tool count, risk score, allowlist status

**US-13: MCP Permission Audit**
- All credentials inventoried with scope analysis
- Stale credentials (90+ days unused) flagged
- Shared accounts (same token on multiple servers) flagged
- Credentials encrypted in storage (Cloud KMS), masked in UI

**US-14: MCP Policy Enforcement**
- Admin manages allowlist of approved MCP packages and remote URLs
- Unauthorized servers trigger immediate alerts
- Policy changes logged in audit trail

**US-15: MCP Threat Detection**
- Tool description mutation detected within 1 processing cycle
- Privilege escalation chain alerts generated with evidence
- Anomalous invocation patterns flagged within 15 minutes of divergence

### 3.4 Functional Requirements

| ID | Requirement | Acceptance |
|---|---|---|
| FR-31 | Local MCP Server Detection: Process scan + JSON-RPC handshake + config file watcher | 95%+ detection within 15 minutes |
| FR-32 | Remote MCP Server Detection: DNS + OS cross-vector + protocol fingerprint | Remote servers detected within 1 DNS scan cycle |
| FR-33 | MCP Manifest Scanner: tools/list, resources/list, description hashing, capability mapping | All exposed tools indexed within 60 seconds of discovery |
| FR-34 | MCP Permission Auditor: Scope analysis, stale credential detection, shared account flagging | Audit completes within 30 seconds per server |
| FR-35 | MCP Allowlist Engine: Admin CRUD for approved packages and URLs, unauthorized alert trigger | Policy enforcement within 1 processing cycle |
| FR-36 | MCP Threat Detector: Mutation detection, escalation chains, anomaly baseline | Mutation detected within 1 processing cycle of change |
| FR-37 | MCP Dashboard Integration: Dedicated MCP Servers section in Discovery tab | Renders under 2 seconds with 50+ servers |

### 3.5 Database Schema

| Collection | Key Fields | Notes |
|---|---|---|
| mcp_servers | id, org_id, server_name, type (local/remote), transport (stdio/sse/streamable-http), host, port, tools_count, risk_score, allowlist_status, first_seen, last_seen | Central MCP inventory |
| mcp_tools | id, server_id, tool_name, description, description_hash, input_schema, capabilities (array), risk_category | Per-tool detail with poisoning detection |
| mcp_credentials | id, server_id, credential_type (api_key/oauth/basic), scope, created_at, last_used, is_shared, is_stale | Encrypted via Cloud KMS |
| mcp_threats | id, server_id, threat_type (mutation/escalation/anomaly/exposure), evidence, severity, detected_at | Links to alerts collection |
| mcp_allowlist | id, org_id, entry_type (package/url), value, added_by, added_at | Admin-managed policy |

### 3.6 Roadmap

| Sprint | Deliverables | Duration |
|---|---|---|
| Sprint 10 | Local MCP Detection: Process scanning, JSON-RPC handshake, config file watcher, OS agent module | 2 weeks |
| Sprint 11 | Remote Detection + Manifest Scanner: Cross-vector correlation, protocol fingerprinting, tools/list indexing, description hashing | 2 weeks |
| Sprint 12 | Permission Auditor + Allowlist: Scope analysis, stale detection, admin allowlist UI, policy enforcement | 2 weeks |
| Sprint 13 | Threat Detection + Dashboard: Mutation detection, escalation chains, anomaly baseline, MCP sub-view in Discovery tab | 2 weeks |

### 3.7 Open Questions

| # | Question | Owner |
|---|---|---|
| 1 | MCP config file paths for all major IDEs (VS Code, Cursor, Windsurf, JetBrains) | Engineering |
| 2 | JSON-RPC fingerprinting to distinguish MCP from generic JSON-RPC services | Engineering |
| 3 | MCP manifest reading and credential auditing: legal implications under UU ITE | Legal |

---

## 4. Amendment #3: AI Cost Intelligence Module

### 4.1 Strategic Rationale

Shadow AI is not just a security problem — it is a financial problem. AI-native app spend surged 393% year-over-year in large enterprises. 34% of employees expense unapproved AI tools on corporate cards. 30-40% of SaaS licenses go unused. This amendment adds financial visibility alongside security visibility, creating a compelling ROI narrative: "We found Rp 85M/year in savings in the first 90 days."

**New buyer persona:** The CFO / Finance Director — typically excluded from security tool purchases but deeply interested in cost optimization.

### 4.2 Feature Design

**AI Spend Dashboard**
- Monthly, quarterly, and annual views of total AI spend
- Breakdowns by: tool, department, status (approved/unapproved), confidence tier (actual/reported/estimated)
- Trend lines and month-over-month comparisons

**3-Tier Cost Estimation**
- Tier 1 (Actual): Pulled from billing API connectors (where available) or uploaded expense data
- Tier 2 (Reported): From Signature DB vendor-published pricing matched against detected user count
- Tier 3 (Estimated): Interpolated from usage patterns and comparable tool pricing

**Duplicate and Overlap Detector**
- Groups tools by category (e.g., 3 different AI writing tools across departments)
- Calculates consolidation savings: "Consolidating to one tool saves Rp 45M/year"
- Suggests the tool with highest approval tier and lowest risk as consolidation target

**Zombie License Detection**
- Flags tools with active licenses but zero detected usage in 30+ days
- Calculates reclaim value per zombie license
- Exports to procurement team for cancellation action

**Expense Data Connector**
- CSV upload of corporate expense data (compatible with Jurnal.id, Accurate, Mekari)
- Automatic merchant-to-tool matching using vendor category codes
- Correlation: "This Rp 2.5M expense on [Merchant] matches [Discovered Tool X] used by 12 employees"

### 4.3 User Stories with Acceptance Criteria

**US-16:** AI Spend Dashboard renders in under 3 seconds. Shows cost by tool, department, and status. Trend chart with monthly granularity. Confidence badges for each cost figure.

**US-17:** Duplicate detector identifies same-category tools across departments. Consolidation recommendation with savings estimate.

**US-18:** Zombie licenses flagged after 30 days of zero usage. Reclaim value calculated based on per-user pricing.

**US-19:** Configurable thresholds at 80% and 100% of budget per tool, department, and org level.

**US-20:** CSV upload processes within 60 seconds for 10,000-row expense files. Merchant matching accuracy above 85%.

### 4.4 Functional Requirements

| ID | Requirement | Acceptance |
|---|---|---|
| FR-38 | AI Spend Dashboard with cost by tool, department, status, and trend chart | Dashboard renders under 3 seconds |
| FR-39 | Signature DB Pricing Layer: per-user pricing for 200+ tools, monthly updated | 80%+ of discovered tools have pricing data |
| FR-40 | Duplicate and Overlap Detector: category grouping, consolidation recommendations | Identifies duplicates within 1 scan cycle |
| FR-41 | License Waste Detector: zombie detection (30+ days), reclaim value calculation | Zombie flagged within 24 hours of threshold |
| FR-42 | AI Spend Alerts: configurable thresholds per tool/department/org | Alert delivered within 10 minutes of threshold breach |
| FR-43 | Expense Data Connector: CSV upload, merchant matching, discovery correlation | Processing under 60 seconds for 10K rows |
| FR-44 | AI Cost Summary in Weekly Report: auto-populated spend overview section | Section included in weekly PDF automatically |

### 4.5 Database Schema

| Collection | Key Fields | Notes |
|---|---|---|
| ai_cost_entries | id, org_id, app_id, confidence_tier (actual/reported/estimated), monthly_cost, currency, user_count, source | Links to discovered_apps |
| cost_thresholds | id, org_id, scope (tool/department/org), scope_id, threshold_80, threshold_100, alert_recipients | Configurable by admin |
| expense_uploads | id, org_id, filename, uploaded_by, row_count, match_count, uploaded_at | CSV import metadata |
| expense_matches | id, org_id, upload_id, merchant_name, amount, matched_app_id, confidence | Links expense to discovery |

### 4.6 Roadmap

| Sprint | Deliverables | Duration |
|---|---|---|
| Sprint 14 | Signature DB Pricing Layer + Cost Estimation Engine (3-tier) | 2 weeks |
| Sprint 15 | AI Spend Dashboard UI + Department/Tool breakdowns + Trend charts | 2.5 weeks |
| Sprint 16 | Duplicate Detector + Zombie License Detection + Alerts | 2.5 weeks |
| Sprint 17 | Expense Connector (CSV) + Weekly Report section + Integration testing | 2 weeks |

---

## 5. Amendment #4: Prompt-Level Data Flow Tracing

### 5.1 Strategic Rationale

This amendment elevates FR-22 (DLP Prompt Monitoring) from a P2 placeholder to a P1 comprehensive specification. The core problem: the platform knows WHICH tools employees use and HOW MUCH they use them, but not WHAT DATA flows through those tools. For a platform promising compliance with UU PDP and OJK, this is a critical gap.

**Privacy-By-Design constraint:** The system NEVER captures actual prompt content. Only structural classification tags (e.g., PII_KTP_DETECTED, FINANCIAL_ACCOUNT_NUMBER) flow to the cloud backend.

### 5.2 Indonesian PII Detection Engine — 10 Categories

| # | Category | Detection Method | Examples |
|---|---|---|---|
| 1 | KTP / NIK (National ID) | 16-digit regex + province code validation + DOB encoding check + female offset | 3201234567890001 |
| 2 | NPWP (Tax ID) | 15/16-digit format validation (old and new formats) | 12.345.678.9-012.000 |
| 3 | Bank Account Numbers | 10-16 digit patterns + BCA/Mandiri/BRI/BNI prefix validation | Bank-specific formats |
| 4 | Phone Numbers | Indonesian mobile prefixes: +62, 08, with carrier validation | +6281234567890 |
| 5 | Email Addresses | Standard email regex with Indonesian domain awareness (.co.id, .go.id) | name@company.co.id |
| 6 | Financial Data | Currency patterns (Rp, IDR) + invoice numbers + transaction amounts | Rp 150,000,000 |
| 7 | BPJS Numbers | 13-digit format (health insurance) + validation | 0001234567890 |
| 8 | Credentials | API key patterns, password-adjacent strings, JWT tokens | sk-proj-abc123... |
| 9 | Source Code | Function signatures, import statements, code block detection | def process_payment() |
| 10 | Internal Documents | Confidential markers, classification headers, internal reference numbers | RAHASIA, INTERNAL-REF |

**All detection runs locally on-device. Only classification tags are transmitted to the cloud.**

### 5.3 User Stories with Acceptance Criteria

**US-21:** Sankey data flow visualization: Users → Tools → Destinations. Color-coded by sensitivity tier. Filterable by department, time range, tool, and data category.

**US-22:** 95%+ detection rate for KTP and NPWP patterns. Under 5% false positive rate. Under 100ms latency impact on user typing.

**US-23:** Each RoPA entry auto-enriched with: observed data categories, daily/weekly volumes, destination server locations (GeoIP), cross-border transfer flags.

**US-24:** Instant alert when PII flows to non-Indonesian server. Art. 56 compliance check includes: destination country, tool vendor jurisdiction, DPA status.

**US-25:** Non-blocking overlay in browser warns employee before sending PII to under-tiered tool. Shows: detected data type, tool tier, suggested alternative.

### 5.4 Functional Requirements

| ID | Requirement | Acceptance |
|---|---|---|
| FR-45 | Indonesian PII Detection Engine: 10 categories, local-execution, regex + structural validation | 95%+ detection, under 5% false positives |
| FR-46 | Data Flow Telemetry Collector: per-interaction metadata tags (no content), user/tool/destination/GeoIP | Zero content leakage to cloud |
| FR-47 | Data Flow Map: interactive Sankey visualization, color-coded by sensitivity, filterable | Renders under 3 seconds for 30-day view |
| FR-48 | Cross-Border Transfer Alert: PII + non-Indonesia destination, Art. 56 compliance check | Alert within 5 minutes of detection |
| FR-49 | In-Browser Employee Warning: non-blocking overlay with tool tier and alternative | Warning displayed within 500ms of PII detection |
| FR-50 | RoPA Evidence Enrichment: auto-populate with observed data categories and destinations | Evidence attached to 100% of active tool entries |
| FR-51 | Admin-Configurable Detection Rules: custom keywords, thresholds, confidential markers | Custom rules active within 1 processing cycle |

### 5.5 Database Schema

| Collection/Table | Key Fields | Storage | Notes |
|---|---|---|---|
| detection_rules | id, org_id, rule_type (regex/keyword/entropy), pattern, sensitivity_tier, enabled | Firestore | Admin-configurable |
| employee_warnings | id, org_id, user_id, tool_id, category_detected, action_taken (dismissed/switched/proceeded), alternative_id | Firestore | Warning interaction tracking |
| data_flow_events | id, org_id, user_id, tool_id, pii_categories (array), destination_ip, destination_country, geo_source, timestamp | BigQuery | Very high volume. NO content. |
| data_flow_aggregates | org_id, tool_id, period (daily/weekly), pii_category_counts, destination_countries, total_interactions | BigQuery | Pre-computed rollups for dashboard |

### 5.6 Roadmap

| Sprint | Deliverables | Duration |
|---|---|---|
| Sprint 18 | PII Detection Engine: 10-category local scanner, regex library, structural validators | 3 weeks |
| Sprint 19 | Data Flow Collector: telemetry pipeline, GeoIP resolution, BigQuery schema, Firestore enrichment | 2.5 weeks |
| Sprint 20 | Sankey Visualization + Cross-Border Alerts: Data Flow Map UI, Art. 56 checker, alert engine | 2.5 weeks |
| Sprint 21 | Employee Warnings + RoPA Integration: In-browser overlay, admin detection rules, RoPA evidence attachment | 2 weeks |

---

## 6. Amendment #5: Enterprise AI Sandbox Environment

### 6.1 Strategic Rationale

Currently, the platform can discover Shadow AI and triage it (approve/ban), but the triage decision is based on metadata alone — risk scores, vendor reputation, and admin judgment. This amendment adds an evidence-based evaluation path: before approving a tool, run it in a monitored sandbox with synthetic data and observe its actual behavior.

### 6.2 Feature Design

**Sandbox Architecture**

- Ephemeral Cloud Run container per trial (Jakarta region)
- Envoy network proxy captures all outbound traffic (destinations, sizes, protocols, API calls)
- Synthetic data engine pre-loads Indonesian test data: Faker (id_ID) + custom KTP/NPWP/bank/BPJS generators
- Penta-Vector sensors (C + D + E) pre-installed inside sandbox
- All telemetry tagged as sandbox_trial for isolation from production data
- Auto-destroy after trial period (configurable: 3, 7, or 14 days)

**7-Section Evaluation Report**

| Section | Content |
|---|---|
| 1. Trial Summary | Tool name, duration, participants, total interactions |
| 2. Network Behavior | All outbound connections, destination countries, data volumes, API call inventory |
| 3. Data Access Patterns | What synthetic data the tool accessed, which categories, how frequently |
| 4. Permission Analysis | OAuth scopes requested, file system access, clipboard access, MCP tools invoked |
| 5. MCP Activity | MCP servers created/connected, tools exposed, credential usage |
| 6. Compliance Assessment | UU PDP data residency check, tier recommendation, DPA status, risk flags |
| 7. Participant Feedback | Structured feedback from trial users: functionality, fit, concerns |

**Composite Behavioral Risk Score:** Weighted aggregate of sections 2-6. Tools scoring below threshold auto-flagged for HITL review.

### 6.3 User Stories with Acceptance Criteria

**US-26:** Admin launches 7-day sandbox trial with one click from Discovery table. Container provisioned within 5 minutes with synthetic data and sensors pre-loaded.

**US-27:** Employee receives invitation link, accesses sandbox via browser, tests tool with realistic synthetic data, submits structured feedback form.

**US-28:** 7-section evaluation report auto-generated within 1 hour of trial end. Includes composite risk score and tier recommendation.

**US-29:** Successful evaluation converts to Approved Catalog entry with report attached. One-click fast track with evidence chain.

### 6.4 Functional Requirements

| ID | Requirement | Acceptance |
|---|---|---|
| FR-52 | Sandbox Provisioner: one-click launch, Cloud Run container, sensor pre-install | Container ready within 5 minutes |
| FR-53 | Synthetic Data Engine: Faker (id_ID), KTP/NPWP/bank generators, pre-loaded corpus | 1,000+ realistic synthetic records per trial |
| FR-54 | Sandbox Network Monitor: Envoy proxy logging all outbound traffic | 100% traffic capture with destination/size/protocol |
| FR-55 | Trial Dashboard: real-time admin view of sandbox activity | Updates every 30 seconds |
| FR-56 | Sandbox Evaluation Report: 7-section PDF with composite risk score | Report generated within 1 hour of trial end |
| FR-57 | Employee Sandbox Portal: browser-based access with feedback form | Access latency under 3 seconds |
| FR-58 | Sandbox-to-Catalog Conversion: one-click fast track with report attached | Conversion under 10 seconds with full evidence chain |

### 6.5 Database Schema

| Collection/Table | Key Fields | Storage | Notes |
|---|---|---|---|
| sandbox_trials | id, org_id, app_id, status (provisioning/active/ended/archived), container_id, duration_days, risk_score, decision | Firestore | Lifecycle management |
| sandbox_participants | id, trial_id, user_id, invited_at, feedback_rating, feedback_text | Firestore | Trial invitations + feedback |
| sandbox_reports | id, trial_id, report_url (GCS), composite_score, tier_recommendation, generated_at | Firestore | Evaluation report metadata |
| sandbox_network_logs | trial_id, timestamp, destination_ip, destination_country, protocol, request_size, response_size | BigQuery | High-volume proxy logs |

### 6.6 Roadmap

| Sprint | Deliverables | Duration |
|---|---|---|
| Sprint 22 | Sandbox Provisioner: Cloud Run + Envoy proxy + auto-destroy + sensor pre-install | 2.5 weeks |
| Sprint 23 | Synthetic Data Engine: Faker (id_ID) + custom generators + pre-loaded corpus | 2 weeks |
| Sprint 24 | Employee Access + Trial Dashboard: browser-based sandbox, invitation flow, real-time monitoring | 2.5 weeks |
| Sprint 25 | Evaluation Report + Catalog Fast Track: 7-section PDF, composite score, one-click conversion | 2 weeks |

---

## 7. Amendment #6: SIEM/SOAR Integration and Webhook API

### 7.1 Strategic Rationale

Shadow AI intelligence is most valuable when it lives alongside all other security signals in the SOC's existing tools — not in a separate dashboard that analysts must remember to check. This amendment creates a bidirectional bridge between the platform and the customer's security ecosystem.

### 7.2 Feature Design — 3 Layers

**Layer 1: Webhook API (Push)**
- 17 event types (see PRD v4.0 Section 10.1 for full list)
- HMAC-SHA256 signed payloads for integrity verification
- Exponential backoff retry (3 attempts over 15 minutes)
- Up to 10 endpoints per organization (Global tier)
- Event filtering: customers subscribe to specific event types per endpoint

**Layer 2: SIEM Connectors (Push)**
- Universal: Syslog (RFC 5424) and ArcSight CEF over TLS
- Google Security Operations (Chronicle): native Pub/Sub subscription
- Splunk: HTTP Event Collector (HEC) + pre-built Splunk app with dashboards
- Elastic Security: Elasticsearch API + Kibana dashboards
- Wazuh: Syslog + custom decoder/rules (Indonesian mid-market focus)
- Microsoft Sentinel: Azure Logic App connector

**Layer 3: SOAR Playbook Templates (Automated Response)**

| ID | Playbook | Trigger | Response Chain |
|---|---|---|---|
| PB-1 | High-Risk Tool Detected | discovery.new_tool (risk=high) | Enrich via Signature DB → Create Jira ticket → Notify SOC → Escalate if over 5 users |
| PB-2 | PII Cross-Border Violation | alert.pii_cross_border | Check Art. 56 → Block network (if auto-block enabled) → Create compliance incident → Notify DPO |
| PB-3 | Unauthorized MCP Server | discovery.mcp_server_found | Check allowlist → Disable process (if auto-remediate enabled) → Create ticket → Notify admin |
| PB-4 | Shadow AI Spend Anomaly | alert.spend_threshold | Pull cost data → Identify tool owner → Create procurement ticket → Notify finance |
| PB-5 | Sensor Offline | system.sensor_offline | Identify host → Attempt restart (if auto-remediate) → Create P1 ticket if fails |
| PB-6 | Employee Policy Violation | alert.policy_violation | Check violation count → 1st: nudge → 2nd: admin → 3rd: HITL escalation |

**Layer 4: REST API (Pull)**
- OAuth 2.0 authentication with role-scoped API keys
- Endpoints: /discoveries, /alerts, /hitl-decisions, /costs, /reports, /mcp-servers
- Pagination, filtering, sorting on all list endpoints
- Rate limit: 1,000 requests/hour per API key
- OpenAPI 3.0 specification published

**Ticketing Integration**
- Jira: REST API + webhook + pre-built issue templates. Bidirectional status sync.
- ServiceNow: REST API + Integration Hub connector. Bidirectional sync.
- Generic: Webhook payload to customer middleware (Zapier, n8n, Make)

### 7.3 User Stories with Acceptance Criteria

**US-30:** Webhook delivers events within 30 seconds of platform event. HMAC verification succeeds on customer side. Retry delivers within 15 minutes on initial failure.

**US-31:** Shadow AI alerts appear in customer SIEM alongside other security events. Pre-built dashboards available for Splunk and Elastic.

**US-32:** SOAR playbooks execute end-to-end within 5 minutes of trigger event. All 6 templates tested in staging before release.

**US-33:** Jira tickets auto-created with: tool name, risk level, affected users, evidence link. Status syncs both directions.

### 7.4 Functional Requirements

| ID | Requirement | Acceptance |
|---|---|---|
| FR-59 | Webhook API: 17 events, HMAC-SHA256, retry, 10 endpoints, event filtering | Delivery within 30 seconds |
| FR-60 | REST API: OAuth 2.0, role-scoped, pagination, 1000 req/hr | 99.9% availability |
| FR-61 | Syslog/CEF Forwarder: RFC 5424, ArcSight CEF, TLS | Compatible with major SIEM platforms |
| FR-62 | Google Security Operations Connector: Pub/Sub integration | Events appear in Chronicle within 60 seconds |
| FR-63 | Splunk Connector: HEC + pre-built app with dashboards | App installable from Splunkbase |
| FR-64 | SOAR Playbook Library: 6 templates (XSOAR, Sentinel, generic JSON) | All playbooks tested end-to-end |
| FR-65 | Jira Bidirectional Integration: auto-create, two-way sync, dedup | Ticket created within 60 seconds |
| FR-66 | Webhook Health Dashboard: per-endpoint metrics, test-fire capability | Health check every 5 minutes |

### 7.5 Database Schema

| Collection/Table | Key Fields | Storage | Notes |
|---|---|---|---|
| webhook_endpoints | id, org_id, url, secret (encrypted), event_filters (array), is_active, health_status | Firestore | Up to 10 per org (Global tier) |
| api_keys | id, org_id, key_hash, role_scope, created_by, last_used, is_active | Firestore | Never store raw key |
| siem_connectors | id, org_id, type (syslog/chronicle/splunk/elastic/wazuh/sentinel), connection_params (encrypted), status | Firestore | Per-platform config |
| ticket_links | id, org_id, alert_id, external_system (jira/servicenow), external_id, external_url, sync_status | Firestore | Bidirectional sync state |
| webhook_deliveries | id, endpoint_id, event_type, payload_hash, status (delivered/failed/retrying), attempts, response_code | BigQuery | 30-day retention |

### 7.6 Roadmap

| Sprint | Deliverables | Duration |
|---|---|---|
| Sprint 26 | Webhook API: 17 event types, HMAC signing, retry logic, event filtering, health dashboard | 3 weeks |
| Sprint 27 | REST API + SIEM Connectors: OAuth 2.0 API, Syslog/CEF forwarder, Chronicle + Splunk connectors | 3 weeks |
| Sprint 28 | SOAR Playbooks + Ticketing: 6 playbook templates, Jira bidirectional integration, Elastic + Wazuh connectors | 2 weeks |

---

## 8. Amendment #7: Employee Education and Policy Nudge Engine

### 8.1 Strategic Rationale

Detection without education creates a resentment loop: employees feel surveilled and penalized, not guided. They do not learn why their behavior was risky, do not know what tools they should use instead, and have no incentive to change. This amendment addresses WHY Shadow AI happens, not just WHAT happened.

**Key insight:** Behavioral science consistently shows that education-at-the-moment-of-action is dramatically more effective than annual training or blanket policy emails.

### 8.2 Nudge Types (7)

| Nudge Type | Channel | Trigger | Content |
|---|---|---|---|
| First-Use Nudge | Email | Employee first detected using ANY AI tool | Welcome message with links to AI AUP and Approved Catalog |
| Shadow AI Alert | Email + Browser | Employee detected using unapproved tool | Non-punitive notification with risk explanation and approved alternatives |
| PII Warning | In-Browser Overlay | PII detected in AI tool input (Am.4) | Real-time warning with data category detected and alternative link |
| Policy Violation | Email | Employee used tool above tier clearance (Am.1) | Graduated: 1st educational, 2nd educational + admin notified, 3rd HITL escalation |
| Tool Approved | Email | Previously shadow tool gets approved via triage/sandbox | Positive reinforcement with catalog link |
| Weekly AI Digest | Email | Weekly (Fridays) | Personal summary: tools used, department score, new catalog additions, safe usage tips |
| Policy Update | Email | Admin publishes new or updated AI usage policy | Distribution with read-receipt: review and acknowledge required |

**Tone principles:** Never punitive ("We noticed" not "You violated"). Always actionable (every nudge includes a next step). Concise (max 150 words email, max 2 sentences overlay). Bilingual (English + Bahasa Indonesia). Branded (organization logo and colors configurable).

### 8.3 AI Acceptable Use Policy Engine

- Rich-text policy editor with versioning in Settings
- Auto-distribution to employees on first AI tool detection
- Click-to-acknowledge with timestamp, IP address, and user agent logging
- Re-distribution on policy version update with new acknowledgement required
- Exportable acknowledgement records for OJK/UU PDP audit evidence
- Default template covering UU PDP and OJK requirements (7 sections)

### 8.4 Department Compliance Scorecard

**Score composition (0 to 100):**

| Factor | Weight | Scoring Logic |
|---|---|---|
| Shadow AI Ratio | 30% | Percentage of AI tools that are in the Approved Catalog |
| AUP Acknowledgement | 20% | Percentage of department employees who acknowledged current AUP version |
| Tier Compliance | 20% | Percentage of interactions where tool tier matched data sensitivity |
| Request Portal Usage | 15% | Ratio of tool requests via portal vs. shadow discoveries |
| Nudge Response Rate | 15% | Percentage of nudges where employee switched to alternative or acknowledged |

**Visibility:** Admin + department heads in Overview tab. Weekly Report leaderboard (top 3 and bottom 3). Departments scoring 90+ for 2 consecutive months earn "Compliance Champion" badge on Employee Portal. Low scores visible to admin only — never public shaming.

### 8.5 Employee "My AI" Portal Page

- My Tools: detected AI tools with status (Approved/Unapproved/Under Review) and "Switch to Alternative" button
- My Compliance Score: personal score with specific improvement actions
- My Policy Status: current AUP version and acknowledgement status
- My Requests: status tracker for submitted tool requests
- Suggest a Tool: quick-form for recommending tools for IT evaluation

**Privacy boundary:** Employees see ONLY their own data. The tone is empowering, not surveillance-oriented.

### 8.6 User Stories with Acceptance Criteria

**US-34:** 7 nudge types auto-triggered. Templates customizable. Bilingual. Frequency caps (1/tool/employee/week). Delivery tracking (sent/opened/clicked/adopted).

**US-35:** Rich-text AUP editor with versioning. Auto-send on first detection. Click-to-acknowledge with audit-grade logging. 95%+ acknowledgement within 30 days.

**US-36:** Monthly score (0-100) based on 5 weighted factors. Dashboard display with trends. Weekly Report leaderboard. Compliance Champion badge for 90+ (2 months).

**US-37:** "My AI" page with personal tools, score, AUP status, requests. Approved alternatives next to unapproved tools. Privacy: employees see only their own data.

### 8.7 Functional Requirements

| ID | Requirement | Acceptance |
|---|---|---|
| FR-67 | Nudge Engine: 7 types, bilingual, frequency-capped, delivery tracked | Nudge delivered within 10 minutes of trigger. Under 3% unsubscribe |
| FR-68 | AUP Engine: editor, versioning, auto-distribution, acknowledgement tracking | 95%+ acknowledgement within 30 days |
| FR-69 | Department Scorecard: 5-factor monthly score, dashboard, leaderboard, badges | Scores calculated monthly. Badge for 90+ (2 months) |
| FR-70 | Employee My AI Page: tools, score, AUP, requests, Suggest a Tool | Renders under 2 seconds. Zero cross-employee data leakage |
| FR-71 | Nudge Analytics Dashboard: effectiveness metrics (delivery, open, click, adoption) | Analytics updated daily |

### 8.8 Database Schema

| Collection | Key Fields | Notes |
|---|---|---|
| nudge_events | id, org_id, user_id, nudge_type, tool_id, channel, template_version, sent_at, opened_at, clicked_at, action_taken, alternative_tool_id | Full interaction tracking |
| aup_versions | id, org_id, version_number, content_html, published_by, published_at, is_current | Policy version history |
| aup_acknowledgements | id, org_id, user_id, version_id, acknowledged_at, ip_address, user_agent | Immutable audit records |
| compliance_scores | id, org_id, department, period, score, factors (5-factor breakdown), trend_vs_prior | Monthly department scores |
| tool_suggestions | id, org_id, user_id, suggested_tool_name, suggested_tool_url, use_case_description, submitted_at, status | Employee recommendations |

### 8.9 Roadmap

| Sprint | Deliverables | Duration |
|---|---|---|
| Sprint 29 | Nudge Engine Core: 7 templates (EN + ID), email pipeline, frequency capping, delivery tracking, admin customization | 2 weeks |
| Sprint 30 | AUP Engine + Scorecard: Policy editor, auto-distribution, acknowledgement, 5-factor score, dashboard widget, leaderboard | 2 weeks |
| Sprint 31 | My AI Page + Analytics: Employee Portal extension, alternative suggestions, Suggest a Tool, nudge effectiveness dashboard | 2 weeks |

---

## 9. Amendment #8: Offline/Degraded Mode for Local Agents

### 9.1 Strategic Rationale

Indonesian mid-market companies outside Jakarta face intermittent connectivity. If the agent silently drops telemetry during outages, Shadow AI goes undetected. If the agent crashes on reconnect, IT teams lose trust in the entire platform. This amendment is the ONLY one prioritized for MVP — without offline resilience, the agent is not production-ready.

### 9.2 Architecture Components

**Local Event Buffer**
- Engine: BoltDB embedded key-value store within Go agent binary
- Encryption: AES-256 at rest (key derived from agent installation secret)
- Compression: LZ4 (approximately 60% size reduction)
- Capacity: 500 MB default (approximately 500K events, approximately 7 days for 500 employees)
- Strategy: Write-ahead — events persisted locally BEFORE cloud transmission
- Cleanup: FIFO for delivered events. Undelivered events never purged.

**Connectivity Health Monitor — 3-Mode State Machine**

| State | Condition | Behavior | Dashboard |
|---|---|---|---|
| ONLINE | Cloud responds under 5s, delivery succeeds | Normal real-time scan + transmit | Green |
| DEGRADED | Latency over 5s OR over 10% drop rate | Batch mode: flush every 60 seconds | Yellow |
| OFFLINE | 3 consecutive health check failures (40s intervals) | Full local buffering, no cloud transmission, local critical alerts | Red |

**Backfill Sync Protocol**
1. Connectivity confirmed via 3 consecutive successful health checks
2. Undelivered events read from buffer in chronological order
3. Transmitted in batches of 100 with 500ms throttle delay
4. Each batch confirmed by Pub/Sub, marked delivered in buffer
5. If connectivity drops during backfill, re-enter OFFLINE mode
6. Dashboard: "Backfill in Progress [X/Y] events"
7. Complete: "Backfill complete. [Y] events recovered."

**Local Critical Alert**
- Triggers: unauthorized MCP server, critical agentic AI detection, PII exfiltration pattern
- Channels: local SMTP, local syslog, local webhook (configurable)
- Latency: under 60 seconds
- Deduplication: matched with cloud alert by event_id after backfill

**Browser Extension Offline Buffer (Vector C)**
- Storage: IndexedDB in employee browser (50 MB max)
- Auto-flushes to Pub/Sub within 5 minutes of reconnection
- PII warnings and in-browser nudges continue functioning fully offline

### 9.3 Affected Agents

| Agent / Vector | Offline Behavior | Local Alert |
|---|---|---|
| DNS Sensor (B) | Logs buffered locally. Signature matching continues against cached DB. | Yes: critical DNS matches |
| OS Agent (D) | Process scanning continues. Events written to local buffer. Heuristics run locally. | Yes: critical agentic AI |
| MCP Scanner (E) | Detection continues. Allowlist checks against cached policy. | Yes: unauthorized MCP |
| Browser Extension (C) | IndexedDB buffer (50 MB). PII scanner and warnings fully offline. | Yes: PII warning overlay |
| PII Scanner (Am.4) | Already local-first by design. No change needed. | N/A (inherently offline) |

### 9.4 User Stories with Acceptance Criteria

**US-38:** Zero events lost during outages of up to 7 days. Backfill completes within 30 minutes for 24-hour outage. Dashboard shows backfill progress.

**US-39:** Per-agent health status (Online/Degraded/Offline) on Integrations tab. Buffer utilization display. Admin alert at OFFLINE over 15 minutes and buffer over 80%.

**US-40:** Critical detections trigger local SMTP/syslog/webhook alerts within 60 seconds. Deduplication with cloud alert after backfill.

### 9.5 Functional Requirements

| ID | Requirement | Acceptance |
|---|---|---|
| FR-72 | Local Event Buffer: BoltDB + AES-256 + LZ4 + write-ahead logging | Zero events lost in 7-day outage |
| FR-73 | Connectivity Health Monitor: 3-mode state machine | Mode transition within 2 minutes |
| FR-74 | Backfill Sync Protocol: throttled batch replay | 24-hour outage backfills in 30 minutes |
| FR-75 | Local Critical Alert: SMTP/syslog/webhook during OFFLINE | Alert within 60 seconds |
| FR-76 | Agent Health Dashboard: status, buffer utilization, uptime chart | Updates within 90 seconds |
| FR-77 | Browser Extension Offline Buffer: IndexedDB (50 MB) with sync | Syncs within 5 minutes of recovery |

### 9.6 Agent Configuration (agent-config.yaml additions)

| Setting | Default | Range | Description |
|---|---|---|---|
| buffer.max_size_mb | 500 | 100-2000 | Maximum local buffer size |
| buffer.encryption_enabled | true | true/false | AES-256 for buffered events |
| buffer.compression | lz4 | lz4/none | Compression algorithm |
| health.check_interval_sec | 40 | 10-60 | Health check ping interval |
| health.offline_threshold_failures | 3 | 2-5 | Failures before OFFLINE mode |
| health.degraded_latency_ms | 5000 | 1000-10000 | Latency threshold for DEGRADED |
| backfill.batch_size | 100 | 10-500 | Events per backfill batch |
| backfill.throttle_ms | 500 | 100-5000 | Delay between batches |
| backfill.stable_checks_required | 3 | 2-5 | Checks before backfill starts |
| local_alert.smtp_server | (empty) | hostname:port | Local SMTP for offline alerts |
| local_alert.syslog_endpoint | (empty) | hostname:port | Local syslog for offline alerts |
| local_alert.webhook_url | (empty) | URL | Local webhook for offline alerts |
| local_alert.critical_triggers | [mcp_unauthorized, agentic_critical, pii_exfiltration] | event type list | What triggers local alerts |

### 9.7 Roadmap (MVP Enhancement)

| Sprint | Deliverables | Duration |
|---|---|---|
| Sprint 2 (Enhancement) | Local Event Buffer: BoltDB, write-ahead logging, AES-256, LZ4, configurable capacity, FIFO cleanup | +1 week |
| Sprint 3 (Enhancement) | Health Monitor + Backfill: 3-mode state machine, health check goroutine, backfill sync, integration test | +1 week |
| Sprint 4 (Enhancement) | Local Alert + Dashboard: SMTP/syslog/webhook dispatch, alert dedup, Integrations tab health, browser IndexedDB | +0.5 week |

**Total: +2.5 weeks added to existing MVP sprints. Not a separate sprint sequence.**

---

## 10. Cross-Amendment Dependencies

Understanding how amendments depend on each other is critical for sprint sequencing.

| Amendment | Hard Dependencies | Soft Dependencies (Enhanced By) |
|---|---|---|
| #8 (Offline) | None (MVP-foundational) | All agents benefit from offline resilience |
| #1 (Catalog) | None (standalone) | Am.7 (nudges link to catalog), Am.5 (sandbox feeds catalog) |
| #2 (MCP/Vector E) | Am.8 (needs offline buffer for MCP events) | Am.1 (MCP tools can enter catalog), Am.6 (MCP events in webhooks) |
| #3 (Cost) | None (standalone) | Am.1 (cost shown per catalog entry), Am.7 (cost in department score) |
| #4 (Data Flow) | None (standalone, local-first) | Am.7 (PII warnings are a nudge type), Am.5 (PII scanning in sandbox) |
| #5 (Sandbox) | Am.1 (sandbox feeds catalog) | Am.2 (MCP sensors in sandbox), Am.4 (PII scanning in sandbox) |
| #6 (SIEM/SOAR) | None (standalone) | All amendments (events from all features feed webhooks) |
| #7 (Nudge) | Am.1 (nudges link to catalog and tiered policy) | Am.4 (PII warnings as nudge type), Am.3 (cost in department score) |

**Parallelism opportunities:** Am.1 and Am.2 can run concurrently. Am.3, Am.4, and Am.7 can overlap. Am.5 and Am.6 can run concurrently. Realistic calendar time with 2 engineering streams: approximately 9 to 12 months.

---

## 11. Consolidated Open Questions

| # | Question | Amendment | Owner | Deadline |
|---|---|---|---|---|
| 1 | Privacy policy NLP scanning: build vs buy | Am.1 | Engineering/Product | Sprint 7 |
| 2 | Auto-approval liability for low-risk tools | Am.1 | Legal | Before Sprint 7 |
| 3 | Catalog seeding strategy (pre-populate vs empty) | Am.1 | Product | Sprint 6 |
| 4 | MCP config file paths for all major IDEs | Am.2 | Engineering | Sprint 10 |
| 5 | JSON-RPC fingerprinting for MCP vs generic | Am.2 | Engineering | Sprint 10 |
| 6 | MCP manifest reading legality under UU ITE | Am.2 | Legal | Before Sprint 10 |
| 7 | Expense CSV schema compatibility (Jurnal.id, Accurate, Mekari) | Am.3 | Product | Sprint 17 |
| 8 | Indonesian PII patterns: KTP female DOB offset, new NPWP format | Am.4 | Engineering | Sprint 18 |
| 9 | On-device PII scanning as employee monitoring (legal) | Am.4 | Legal | Before Sprint 18 |
| 10 | Browser extension typing latency with PII scanner | Am.4 | Engineering | Sprint 18 |
| 11 | Art. 56 jurisdiction database source | Am.4 | Legal/Compliance | Sprint 20 |
| 12 | Sandbox access model: browser-based remote desktop vs URL proxy | Am.5 | Engineering | Sprint 22 |
| 13 | Webhook API versioning strategy | Am.6 | Engineering/Product | Sprint 26 |
| 14 | Nudge email deliverability through Indonesian spam filters | Am.7 | Engineering | Sprint 29 |
| 15 | Employee nudge consent under UU PDP | Am.7 | Legal/HR | Before Sprint 29 |
| 16 | Bahasa Indonesia nudge copy (native copywriter needed) | Am.7 | Marketing/Content | Sprint 29 |
| 17 | Department hierarchy mapping from G-Workspace/M365 | Am.7 | Product/Engineering | Sprint 30 |
| 18 | Compliance score manipulation prevention | Am.7 | Engineering/Product | Sprint 30 |
| 19 | BoltDB vs BadgerDB benchmark on Indonesian hardware | Am.8 | Engineering | Sprint 2 |
| 20 | Buffer capacity modeling for 2,000-employee orgs | Am.8 | Engineering/Product | Sprint 2 |
| 21 | Local SMTP availability in cloud-email-only environments | Am.8 | Product/Engineering | Sprint 4 |
| 22 | Clock synchronization after long outages (NTP validation) | Am.8 | Engineering | Sprint 3 |
| 23 | Browser IndexedDB 50 MB buffer consumption benchmarks | Am.8 | Engineering | Sprint 4 |

---

## 12. Consolidated Required for Acceptance

### Amendment #1 (Catalog)
- Privacy policy NLP scanning decision (build vs buy)
- Auto-approval legal opinion
- Catalog seeding list (initial 10+ tools per category)
- Employee Portal Figma mockups (Catalog, Request, Status)
- Pre-screening check weight calibration data

### Amendment #2 (MCP)
- MCP config file path inventory for VS Code, Cursor, Windsurf, JetBrains
- JSON-RPC fingerprinting test results
- Legal opinion on MCP manifest reading under UU ITE
- MCP Signature DB entries (initial 50+ known MCP packages)
- MCP Dashboard mockup (Discovery tab sub-view)

### Amendment #3 (Cost)
- Signature DB pricing data for top 100 AI tools
- Expense CSV schema (compatible with 3 major Indonesian accounting platforms)
- Cost Dashboard Figma mockups
- Duplicate detection algorithm validation data
- Zombie license threshold calibration (30 vs 60 days)

### Amendment #4 (Data Flow)
- Indonesian PII test dataset (1,000+ synthetic samples across 10 categories)
- KTP/NIK validation spec (province codes, DOB encoding, female offset)
- Legal opinion on on-device PII scanning as employee monitoring
- Art. 56 jurisdiction database source
- Data Flow Map (Sankey) Figma mockup
- Employee warning overlay design (non-blocking)
- PII scanner latency benchmark (under 100ms target)

### Amendment #5 (Sandbox)
- Sandbox access model decision (browser remote desktop vs URL proxy)
- Synthetic data engine specification (what categories, what volume)
- Evaluation Report PDF template design
- Sandbox network architecture diagram (Envoy proxy configuration)
- Cloud Run cost model (per-trial estimate)

### Amendment #6 (SIEM/SOAR)
- Webhook event schema v1 (OpenAPI 3.0 specification)
- CEF field mapping document (for Syslog/CEF forwarder)
- Splunk app package (.spl) with pre-built dashboards
- SOAR playbook test results (all 6 playbooks end-to-end)
- Jira integration test with real Jira Cloud instance
- REST API documentation site

### Amendment #7 (Nudge)
- Professional nudge copy: 7 templates × 2 languages (EN + Bahasa Indonesia)
- Default AI Acceptable Use Policy template (Indonesian-compliant, 7 sections)
- Legal opinion on employee nudge consent under UU PDP
- Department hierarchy mapping strategy (G-Workspace / M365)
- Employee Portal mockups: My AI page, Suggest a Tool form
- Nudge Analytics Dashboard mockup

### Amendment #8 (Offline)
- BoltDB/BadgerDB comparative benchmark on reference Indonesian hardware
- 24-hour outage simulation test with 100% event recovery verification
- Backfill throttle network impact test (10-50 Mbps connections)
- Local alert channel end-to-end test (SMTP, syslog, webhook)
- Browser IndexedDB buffer consumption benchmark (8 hours continuous monitoring)

---

**Document Status:** Final (v1.0)  
**Companion To:** Shadow AI Detection PRD v4.0 Final  
**Classification:** Confidential — Internal Use Only
