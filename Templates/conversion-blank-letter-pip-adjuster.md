Norto# Template Conversion Report: Blank Letter to PIP Adjuster

**Conversion Date:** 2026-01-21  
**Source File:** `2022 Whaley Blank Letter to PIP Adjuster(1) (2).docx`  
**New Template:** `blank_letter_pip_adjuster.docx`  
**Configuration:** `blank_letter_pip_adjuster.yaml`

---

## Template Overview

**Template ID:** `blank_letter_pip_adjuster`  
**Category:** Correspondence → PIP Insurance  
**Purpose:** General-purpose letter to PIP insurance adjusters

This is a flexible template for routine correspondence with PIP adjusters, including:
- Benefit approval requests
- Status inquiries
- Documentation submissions
- General follow-up communications

---

## Placeholder Mappings

| Old Placeholder | New Placeholder | Data Source | Notes |
|----------------|-----------------|-------------|-------|
| `{{TODAY_LONG}}` | `{{date}}` | `SYSTEM.today_long` | Current date in long format |
| `{{insurance.insuranceCompany.name}}` | `{{insurance_company}}` | `carrier.name` | PIP insurance carrier name |
| `{{insurance.insuranceAdjuster.address1Block}}` | `{{adjuster_address}}` | `adjuster.address_block` | Complete mailing address |
| `{{insurance.insuranceAdjuster.email1}}` | `{{adjuster_email}}` | `adjuster.email` | Optional field |
| `{{client.name}}` | `{{client_name}}` | `client.full_name` | Client's full legal name |
| `{{insurance.claimNumber}}` | `{{claim_number}}` | `pip.claim_number` | PIP claim number |
| `{{incidentDate}}` | `{{incident_date}}` | `incident.date_formatted` | Date of loss/incident |
| `{{insurance.insuranceAdjuster.firstname}}` | `{{adjuster_firstname}}` | `adjuster.first_name` | For salutation |
| `{{primary}}` | `{{attorney_name}}` | `attorney.full_name` | Assigned attorney |
| `[Enter Body of Blank Letter to PIP Adjuster]` | `{{body}}` | `USER_INPUT` | Main letter content |

---

## Graph Query Structure

### Target Node
```cypher
PIPClaim
```

### Required Relationships
```cypher
(case:Case)-[:HAS_PIP_CLAIM]->(pip:PIPClaim)
(case)-[:HAS_CLIENT]->(client:Client)
(pip)-[:INSURED_BY]->(carrier:InsuranceCarrier)
(pip)-[:ASSIGNED_TO]->(adjuster:InsuranceAdjuster)
```

### Optional Relationships
```cypher
(case)-[:HAS_INCIDENT]->(incident:Incident)
(case)-[:ASSIGNED_TO]->(attorney:Attorney)
```

---

## Field Configuration

### Required Fields (9)
- `date` - Current date
- `insurance_company` - Carrier name
- `adjuster_firstname` - For salutation
- `adjuster_address` - Mailing address
- `client_name` - Client full name
- `claim_number` - PIP claim number
- `incident_date` - Date of loss
- `attorney_name` - Signing attorney
- `body` - Letter content (min 50 chars)

### Optional Fields (1)
- `adjuster_email` - Email address (for Via Fax/Email line)

---

## Validation Rules

1. **Claim Number** - Must not be empty
2. **Client Name** - Must not be empty
3. **Insurance Company** - Must not be empty
4. **Adjuster First Name** - Required for salutation
5. **Body** - Minimum 50 characters

---

## Usage Examples

### Example 1: Request for PIP Benefits Approval
```
I am writing to request approval of PIP benefits for medical treatment 
related to the above-referenced claim. Please find enclosed medical 
records and billing statements supporting this request.
```

### Example 2: Status Inquiry
```
I am writing to inquire about the status of the PIP claim for our client. 
We have not received communication regarding the claim approval or any 
outstanding documentation requirements.
```

### Example 3: Documentation Submission
```
Enclosed please find additional medical records and billing statements 
for your review and processing. Please confirm receipt and advise if 
any additional information is required.
```

---

## Changes from Original

### Simplified Placeholders
- Removed nested object notation (e.g., `insurance.insuranceCompany.name` → `insurance_company`)
- Used clear, descriptive names
- Consistent snake_case naming

### Enhanced Metadata
- Added validation rules
- Added usage examples
- Added generation hints for AI
- Added output filename pattern
- Added category/subcategory classification

### Improved Data Mapping
- Explicit graph query structure
- Clear relationship requirements
- Fallback handling for optional fields
- Source attribution for each field

### Standardized Structure
- Consistent with other converted templates
- Ready for integration with template generation system
- Supports both user input and AI generation

---

## Template Generation Workflow

1. **User requests letter to PIP adjuster**
2. **System identifies case and PIP claim**
3. **Query executes to gather required data:**
   - Client information
   - PIP claim details
   - Insurance carrier data
   - Adjuster contact information
4. **User provides or AI generates body content**
5. **Template populates all fields**
6. **Validation runs (claim number, client name, body length)**
7. **Document generates with filename:** `{case_name} - Letter to PIP Adjuster - {date_short}.docx`

---

## Integration Notes

### For AI Agents
- This template is flexible and suitable for many PIP correspondence scenarios
- The body field should be tailored to the specific purpose
- Maintain professional, insurance-industry-appropriate tone
- Include specific claim details when relevant
- Standard closing paragraph emphasizes cooperation and availability

### For Template System
- Query targets `PIPClaim` node (not Case)
- Requires active PIP claim relationship
- Attorney field has fallback to "Aaron Whaley"
- Address block has fallback to component assembly
- Email is optional (will show blank if not available)

---

## File Locations

- **Template File:** `/Users/aaronwhaley/RoscoeDesktop/Templates/blank_letter_pip_adjuster.docx`
- **Configuration:** `/Users/aaronwhaley/RoscoeDesktop/Templates/blank_letter_pip_adjuster.yaml`
- **Original File:** `/Users/aaronwhaley/RoscoeDesktop/Templates/2022 Whaley Blank Letter to PIP Adjuster(1) (2).docx`

---

**Conversion Status:** ✓ Complete  
**Testing Status:** Pending  
**Integration Status:** Ready for deployment
