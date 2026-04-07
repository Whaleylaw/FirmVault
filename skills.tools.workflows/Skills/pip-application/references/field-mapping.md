# KACP Application Field Mapping

## Form Field to Data Source Mapping

### Section 1: Personal Information

| Form Field | Data Source | JSON Path | Notes |
|------------|-------------|-----------|-------|
| Your Name | `cases/<slug>/<slug>.md` (frontmatter) | `client_name` | Full legal name |
| Home Phone | `cases/<slug>/<slug>.md` (frontmatter) | `client_phone` | Primary contact |
| Work Phone | `cases/<slug>/contacts/` | `[type=employer].phone` | If employed |
| Your Address | `cases/<slug>/<slug>.md` (frontmatter) | `client_address` | Street address |
| City, State, Zip | `cases/<slug>/<slug>.md` (frontmatter) | Parsed from `client_address` | |
| Date of Birth | `cases/<slug>/contacts/` | `[type=client].dob` | MM/DD/YYYY format |
| Social Security No. | `cases/<slug>/contacts/` | `[type=client].ssn` | XXX-XX-XXXX |

### Section 2: Accident Information

| Form Field | Data Source | JSON Path | Notes |
|------------|-------------|-----------|-------|
| Date of Accident | `cases/<slug>/<slug>.md` (frontmatter) | `accident_date` | From case setup |
| Time of Accident | intake | Captured during intake | Optional |
| Place of Accident | intake/police report | Location description | |
| Brief Description | `cases/<slug>/<slug>.md` (frontmatter) | `case_summary` | Short narrative |

### Section 3: Vehicle/Insurance Information

| Form Field | Data Source | JSON Path | Notes |
|------------|-------------|-----------|-------|
| Own Motor Vehicle? | waterfall answers | From waterfall Q1 | Yes/No |
| Insurance Company | `cases/<slug>/claims/` and `## Insurance Claims` section | `pip.pip_insurer` | From waterfall |
| Policy Number | `cases/<slug>/claims/` and `## Insurance Claims` section | `pip.policy_number` | If known |

### Section 4: Injury Information

| Form Field | Data Source | JSON Path | Notes |
|------------|-------------|-----------|-------|
| Describe Your Injury | intake | Injury description | From initial interview |

### Section 5: Medical Treatment

| Form Field | Data Source | JSON Path | Notes |
|------------|-------------|-----------|-------|
| Doctor's Name | `cases/<slug>/contacts/` (provider stubs) and `## Medical Providers` section | `[0].provider_name` | Primary treating |
| Doctor's Address | `cases/<slug>/contacts/` (provider stubs) and `## Medical Providers` section | `[0].address` | |
| Hospital Name | `cases/<slug>/contacts/` (provider stubs) and `## Medical Providers` section | `[type=hospital].provider_name` | If applicable |
| Hospital Address | `cases/<slug>/contacts/` (provider stubs) and `## Medical Providers` section | `[type=hospital].address` | |

### Section 6: Employment Information

| Form Field | Data Source | JSON Path | Notes |
|------------|-------------|-----------|-------|
| Employer Name | `cases/<slug>/contacts/` | `[type=employer].name` | If employed |
| Employer Address | `cases/<slug>/contacts/` | `[type=employer].address` | |
| Occupation | `cases/<slug>/contacts/` | `[type=employer].occupation` | |

## Python Dictionary Structure

```python
field_values = {
    # Personal Info
    "PatientName": "John Smith",
    "HomePhone": "502-555-1234",
    "WorkPhone": "",
    "StreetAddress": "123 Main St",
    "City": "Louisville",
    "State": "KY",
    "Zip": "40202",
    "DateOfBirth": "01/15/1985",
    "SSN": "123-45-6789",
    
    # Accident Info
    "AccidentDate": "12/01/2024",
    "AccidentTime": "3:30 PM",
    "AccidentLocation": "Intersection of Main St and Broadway, Louisville, KY",
    "AccidentDescription": "Rear-ended while stopped at red light",
    
    # Vehicle/Insurance
    "OwnVehicle_Yes": False,
    "OwnVehicle_No": True,
    "InsuranceCompany": "State Farm",
    "PolicyNumber": "POL-12345",
    
    # Injury
    "InjuryDescription": "Neck pain, back pain, headaches following collision",
    
    # Medical
    "DoctorName": "Dr. Smith",
    "DoctorAddress": "123 Medical Way, Louisville, KY 40202",
    "HospitalName": "University Hospital",
    "HospitalAddress": "550 S Jackson St, Louisville, KY 40202",
    
    # Employment
    "EmployerName": "ABC Company",
    "EmployerAddress": "456 Business Blvd, Louisville, KY 40203",
    "Occupation": "Office Manager"
}
```

## Handling Missing Values

### Required Fields (Must Have)
- Client name
- Client phone
- Client address
- Date of birth
- SSN
- Accident date
- PIP carrier

### Optional Fields (Can Leave Blank)
- Work phone (if not employed)
- Time of accident
- Hospital (if no hospital visit)
- Employer info (if not employed)

### Prompting for Missing Required Data

```
To complete the PIP Application, I need:

1. Client's date of birth (MM/DD/YYYY): _______
2. Client's SSN (XXX-XX-XXXX): _______
3. Brief description of injuries: _______

(Time of accident and employer info are optional if not applicable)
```

