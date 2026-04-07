# Gemini File API — invocation pattern

Used by `multimedia-evidence-analysis` Phase 2 when executing via a multimodal sub-agent with `google.generativeai` available. Requires `GOOGLE_API_KEY` in environment.

## Upload, wait, analyze, delete

```python
import os, time
import google.generativeai as genai

genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

# Workspace-relative path — no /workspace/ prefix.
file_path = "cases/<slug>/documents/<category>/<file>.mp4"

uploaded = genai.upload_file(file_path)
while uploaded.state.name == "PROCESSING":
    time.sleep(1)
    uploaded = genai.get_file(uploaded.name)

model = genai.GenerativeModel("gemini-3-pro-preview")
response = model.generate_content([uploaded, ANALYSIS_PROMPT])
print(response.text)

genai.delete_file(uploaded.name)   # optional; auto-deletes after 48h
```

Video files must be under 2GB. For larger files, split first.

## Analysis prompt template

Fill the bracketed fields from Phase 1 context before sending.

```
Analyze this [audio|video] file as legal evidence in a personal injury case.

CASE CONTEXT
- Client: {client_name} ({client_role: plaintiff|defendant})
- Incident: {one-sentence summary from case file}
- Date: {date_of_incident}
- Location: {incident_location from police report}
- Disputed facts: {from complaint/answer if available}
- Known witnesses: {list from report}

PRODUCE

1. Full transcript with [HH:MM:SS] timestamps and exact quotes.

2. Speaker identification informed by the case context above. Do not use
   generic "Speaker A / Speaker B". For each voice, state who it probably is
   and the basis — e.g. "{client_name} — provides DOB matching case file,
   describes back pain consistent with complaint paragraph 12".

3. Visual timeline (video only) — key moments with timestamps and a one-line
   legal significance note each.

4. Comparison to case facts:
   - What in this evidence SUPPORTS the client's version
   - What CONTRADICTS or raises questions
   - What NEW facts are revealed

5. Legal observations: liability, causation, contemporaneous injury
   complaints, helpful evidence, red flags / weaknesses.

6. Frame-extraction candidates (video only) — timestamps worth saving as
   exhibits with a short reason each.

Cite timestamps for every claim. Be objective. Write for an attorney
evaluating evidence for trial.
```
