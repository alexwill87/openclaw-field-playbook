---
---
status: complete
audience: both
chapter: 06
last_updated: 2026-04
contributors: [alexwill87, claude-cockpit]
lang: en
---

# 05 -- Accounting Firm

**For whom:** accounting or management consulting firm, 3 to 20 employees
**Setup time:** 2 to 3 weeks
**Difficulty:** Advanced (regulatory constraints)

---

## Context

An accounting firm manages dozens of client files simultaneously. Each file has its tax deadlines, documents to collect, and filings to produce. Staff spend considerable time sorting documents, following up with clients, and verifying compliance.

The firm wants to use OpenClaw to automate repetitive administrative tasks while strictly respecting GDPR and professional secrecy.

---

## Problem

- Sorting received documents (invoices, statements, supporting documents) is manual and time-consuming
- Tax deadlines are tracked in spreadsheets, with risk of oversight
- Reminders to clients for missing documents are sent too late
- Compliance verification (VAT, social charges) relies on individual experience
- New employees don't have structured access to case law and internal procedures

---

## Configuration

### Infrastructure

| Component | Choice | Monthly Cost |
|-----------|--------|--------------|
| Server | Dedicated VPS in France (OVH, Scaleway) | 15-30 EUR |
| OS | Ubuntu 24.04 LTS | -- |
| OpenClaw | On-premise installation | -- |
| Database | PostgreSQL (encryption at rest) | -- |
| Document storage | Encrypted file system (LUKS) | -- |
| Internal communication | Mattermost self-hosted | -- |

**Requirement: hosting in France or within the EU.** Professional secrecy and GDPR require that client data remain within the EU. No API calls to a cloud LLM must contain nominative client data.

### Anonymization Strategy

Before any processing by an LLM:
1. Nominative data (names, SIRET, addresses, specific amounts) are replaced with placeholders
2. The agent works with anonymized data
3. Placeholders are restored in the final result
4. Agent logs never contain nominative data

### Agents

**Sorting Agent:**
- Receives incoming documents (scan, email, upload)
- Classifies by type: invoice / bank statement / supporting document / tax correspondence / other
- Associates with corresponding client file
- Flags incomplete or illegible documents

**Deadline Agent:**
- Maintains the tax calendar for each file
- Sends alerts to staff: D-30, D-15, D-7, D-3
- Generates list of missing documents for each deadline
- Proposes draft client reminder for overdue documents

**Compliance Agent:**
- Verifies filings before submission
- Checks VAT rates applied
- Detects inconsistencies between documents and filings
- Flags attention points without making decisions

---

## Implementation

### Week 1: Secure Infrastructure

1. Provision the VPS in France
2. Configure disk encryption (LUKS)
3. Install PostgreSQL with encryption at rest
4. Install OpenClaw
5. Configure data anonymization (preprocessing pipeline)
6. Test that logs contain no nominative data

### Week 2: Sorting and Deadline Agents

1. Deploy the Sorting Agent with the firm's document categories
2. Test on a sample of 50 real documents (anonymized)
3. Configure the Deadline Agent with the current tax calendar
4. Test alerts at the correct thresholds
5. Train 2 pilot employees

### Week 3: Compliance and Deployment

1. Deploy the Compliance Agent with basic tax rules
2. Test on 10 past filing cases
3. Adjust rules based on feedback from accountants
4. Deploy across the entire firm
5. Document procedures and limitations

---

## Results

After two months of use:

- **85% automated sorting:** 85% of documents are correctly classified and associated with the right file. The remaining 15% are flagged for manual classification
- **Zero missed deadlines:** progressive alerts (D-30 to D-3) have eliminated filing delays
- **Timely client reminders:** clients are reminded about missing documents as soon as the D-15 threshold is reached, instead of last-minute follow-up
- **Systematic compliance verification:** every filing goes through the agent before submission. It does not replace the accountant but detects mechanical errors (wrong rate, inconsistent amount)
- **Confidentiality preserved:** log audit confirms the absence of nominative data in LLM calls

---

## Lessons Learned

1. **Anonymization is non-negotiable.** It is not an option, it is a prerequisite. The anonymization pipeline must be tested and audited before any deployment.

2. **The Compliance Agent assists, it does not certify.** The accountant remains responsible. The agent detects anomalies, the human decides.

3. **Sorting categories must match the firm's categories, not generic categories.** Each firm has its own nomenclature. The prompt must reflect it exactly.

4. **Hosting in France, not just in the EU.** For a French accounting firm, hosting in France simplifies compliance and communication with clients about the security of their data.

5. **Train employees on what the agent does not do.** Training must emphasize limitations: the agent does not make tax decisions, does not sign filings, does not communicate directly with clients.

---

## Regulatory Constraints

### GDPR

- Processing register: document the use of OpenClaw in the firm's GDPR register
- Legal basis: legitimate interest (improvement of internal efficiency) or client consent depending on the case
- Right of access: clients must be able to request what data is processed by the agent
- Retention period: align with accounting obligations (10 years for accounting documents)
- Data processing: if a cloud LLM is used, the provider is a data processor under GDPR

### Professional Secrecy

- No nominative data must be transmitted to a third-party service without prior anonymization
- Access to OpenClaw must be logged and auditable
- An employee who leaves the firm must immediately lose access

### Recommendations of the Order of Chartered Accountants

- Document the use of AI in internal procedures
- Inform clients of the use of AI tools in processing their files
- Maintain human responsibility for all tax or accounting output

---

## Common Mistakes

| Mistake | Consequence | Solution |
|--------|-------------|----------|
| Sending nominative data to the LLM | GDPR and professional secrecy violation | Mandatory anonymization pipeline |
| Agent that "decides" the VAT rate | Tax error engaging the firm's liability | Agent proposes, accountant validates |
| Hosting outside the EU | GDPR non-compliance | VPS in France, EU provider only |
| No audit trail | Impossible to prove compliance | Complete and immutable logs |

---

## Template -- System Prompt for the Sorting Agent

```
You are the document sorting assistant for the [NAME] firm.

Your role is to classify received documents and associate them with client files.

ABSOLUTE RULE: you only process anonymized data. If you detect non-anonymized
nominative data in a document, you report it immediately and do not process it.

Document categories:
1. Purchase invoice
2. Sales invoice
3. Bank statement
4. Pay slip
5. Tax notice
6. Miscellaneous supporting document
7. Tax authority correspondence
8. Non-classifiable document -> flag for manual processing

For each document:
- Identify the category
- Identify the client file (via the client placeholder)
- Verify legibility and completeness
- Flag anomalies (missing amount, illegible date, truncated document)

Output format:
Category: [category]
File: [client placeholder]
Status: complete / incomplete / illegible
Anomalies: [list or "none"]
```

---

## Verification

- [ ] The VPS is hosted in France with disk encryption
- [ ] The anonymization pipeline works on a sample of 20 documents
- [ ] Logs contain no nominative data (audit)
- [ ] The Sorting Agent correctly classifies 80%+ of a sample of 50 documents
- [ ] Deadline alerts trigger at the correct thresholds (D-30, D-15, D-7, D-3)
- [ ] The Compliance Agent detects an intentionally inserted VAT rate error
- [ ] The firm's GDPR register mentions OpenClaw processing

---

*An accounting firm that deploys AI without anonymization takes a legal risk disproportionate to the operational gain. Anonymization is the first step, not the last.*

---
