from langchain_core.documents import Document

# ── Policy Documents 
# Realistic but fictional policy documents for demonstration purposes.
# In production these would be embedded in a vector DB (e.g. ChromaDB, FAISS)
# and retrieved via semantic similarity search.

POLICY_DOCUMENTS = [
    Document(
        page_content="""
        POLICY: Continuous Glucose Monitoring (CGM) Devices
        REFERENCE: Medicare LCD L33822 (Adapted)
        CATEGORY: Durable Medical Equipment (DME)

        COVERAGE CRITERIA — ALL of the following must be met:
        1. Patient has a confirmed diagnosis of diabetes mellitus (Type 1 or Type 2).
        2. Patient is currently on insulin therapy (basal, bolus, or twice-daily regimen).
        3. HbA1c is above 7.0% indicating suboptimal glycemic control.
        4. Treating physician documents medical necessity and orders the device.
        5. Patient has been educated on CGM use by a qualified provider.

        SUPPORTING FACTORS (strengthen the case for approval):
        - Physical limitations (e.g. arthritis, neuropathy) preventing reliable fingerstick monitoring.
        - History of hypoglycemic episodes or hypoglycemia unawareness.
        - Prior inconsistent self-monitoring of blood glucose (SMBG).

        EXCLUSION CRITERIA:
        - Patient not on insulin therapy.
        - HbA1c below 7.0% with stable glycemic control.
        - No documented prior attempt at glucose monitoring.

        COVERAGE DURATION: Initial 3-month approval with renewal based on clinical benefit.
        """,
        metadata={"policy_id": "LCD-L33822", "treatment": "CGM", "category": "DME"}
    ),

    Document(
        page_content="""
        POLICY: MRI of the Lumbar Spine
        REFERENCE: AIM Specialty Health Lumbar Spine MRI Guidelines (Adapted)
        CATEGORY: Advanced Imaging

        COVERAGE CRITERIA — at least ONE of the following must be met:
        1. Symptoms persisting beyond 6 weeks despite conservative treatment (physical therapy, NSAIDs).
        2. Presence of red flag symptoms: fever, unexplained weight loss, bowel/bladder dysfunction,
           saddle anesthesia, or progressive neurological deficits.
        3. History of malignancy with new onset back pain.
        4. Recent significant trauma (fall from height, motor vehicle accident).
        5. Clinical suspicion of spinal infection, fracture, or inflammatory arthropathy.

        CONSERVATIVE TREATMENT REQUIRED FIRST:
        - Minimum 4-6 weeks of physical therapy or documented conservative management.
        - Trial of NSAIDs or analgesics unless contraindicated.
        - Physician documentation of treatment failure before imaging is requested.

        EXCLUSION CRITERIA (imaging NOT appropriate when):
        - Symptom duration is less than 6 weeks with no red flags present.
        - No neurological symptoms, no trauma, no systemic illness indicators.
        - Conservative treatment has not been attempted.

        NOTE: Non-specific back pain of less than 6 weeks duration without red flags
        does not meet criteria for advanced lumbar imaging.
        """,
        metadata={"policy_id": "AIM-LSPI-2024", "treatment": "MRI lumbar spine", "category": "Advanced Imaging"}
    ),

    Document(
        page_content="""
        POLICY: Biologic DMARDs for Rheumatoid Arthritis (RA)
        REFERENCE: BCBS Medical Policy MED.00048 — Biologic Agents for RA (Adapted)
        CATEGORY: Specialty Pharmacy / Injectable Biologics

        COVERAGE CRITERIA — ALL of the following must be met:
        1. Confirmed diagnosis of moderate to severe Rheumatoid Arthritis (RA) by a rheumatologist.
        2. Patient has completed an adequate trial of at least ONE conventional DMARD
           (methotrexate preferred) at therapeutic dose for a minimum of 3 months,
           with documented failure, intolerance, or contraindication.
        3. Pre-treatment screening completed and documented:
           a. TB screening (PPD or IGRA test) — negative or treated latent TB required.
           b. Hepatitis B surface antigen and core antibody screening — negative required.
           c. CBC, CMP within 3 months of initiation.
        4. Prescribing physician is a board-certified rheumatologist.

        SPECIFIC TO ADALIMUMAB (Humira):
        - Step therapy required: methotrexate failure must be documented before TNF inhibitor approval.
        - Biosimilar alternatives (adalimumab-adaz, adalimumab-afzb) must be considered first
          unless patient has documented contraindication to biosimilars.

        EXCLUSION CRITERIA:
        - Active serious infection (bacterial, fungal, viral).
        - Active TB or untreated latent TB.
        - Positive hepatitis B surface antigen.
        - No documented failure of conventional DMARD therapy.
        - Missing required pre-treatment labs.

        RENEWAL: Every 6 months with documented clinical response (ACR20 improvement or equivalent).
        """,
        metadata={"policy_id": "BCBS-MED-00048", "treatment": "biologic DMARD", "category": "Specialty Pharmacy"}
    ),
    Document(
        page_content="""
        POLICY: Implantable Cardiac Monitors / Loop Recorders (ILR)
        REFERENCE: CMS Coverage Policy — Cardiac Event Monitors (Adapted)
        CATEGORY: Durable Medical Equipment / Cardiac Monitoring

        COVERAGE CRITERIA — ALL of the following must be met:
        1. Patient has confirmed recurrent unexplained syncope or palpitations not captured by
           standard monitoring (24-hour Holter or 30-day event monitor must be documented as inconclusive).
        2. Structural cardiac disease has been ruled out via echocardiogram or equivalent imaging.
        3. Prescribing physician is a board-certified cardiologist or electrophysiologist.
        4. Physician has documented medical necessity and submitted a formal order.
        5. All non-invasive diagnostic workup has been completed and results are available,
           including tilt table test where vasovagal syncope is suspected.

        PENDING CRITERIA (hold for additional information when):
        - Required diagnostic test results are outstanding but expected within 10 business days.
        - Tilt table test results are pending to rule out vasovagal syncope.
        - Additional specialist consultation is scheduled but not yet completed.

        EXCLUSION CRITERIA:
        - Standard monitoring (Holter, event monitor) has not been attempted first.
        - Structural cardiac abnormality identified on echo without further workup.
        - No documented episodes of syncope or palpitations in the medical record.

        COVERAGE DURATION: Up to 3 years of continuous monitoring with 6-month physician review.
        """,
        metadata={"policy_id": "CMS-CARDIAC-ILR", "treatment": "implantable loop recorder cardiac monitor syncope arrhythmia", "category": "Cardiac Monitoring"}
    ),
]


# ── Simple Keyword-Based Retriever 
# In production: replace with ChromaDB / FAISS vector similarity search.
# For this POC: keyword matching on extracted facts to retrieve the right policy.

def retrieve_policy(extracted_facts: str) -> str:
    """
    Retrieves the most relevant policy document based on keywords
    found in the extracted clinical facts.
    Returns the policy text as a string.
    """
    facts_lower = extracted_facts.lower()

    scores = []
    for doc in POLICY_DOCUMENTS:
        treatment = doc.metadata["treatment"].lower()
        keywords = treatment.split()
        score = sum(1 for kw in keywords if kw in facts_lower)

        # Extra keyword hints per policy
        if doc.metadata["policy_id"] == "LCD-L33822":
            hints = ["cgm", "glucose monitor", "glucose monitoring", "diabetes", "insulin", "hba1c", "fingerstick"]
        elif doc.metadata["policy_id"] == "AIM-LSPI-2024":
            hints = ["mri", "lumbar", "spine", "back pain", "imaging"]
        elif doc.metadata['policy_id'] == 'CMS-CARDIAC-ILR':
            hints = ["ilr", "loop recorder", "syncope", "arrhythmia", "holter", "cardiac", "cardiologist", "tilt table", "palpitation"]
        else:
            hints = ["biologic", "dmard", "adalimumab", "humira", "rheumatoid", "methotrexate", "tnf"]

        score += sum(2 for hint in hints if hint in facts_lower)
        scores.append((score, doc))

    best_doc = max(scores, key=lambda x: x[0])[1]

    return (
        f"RETRIEVED POLICY:\n"
        f"Reference: {best_doc.metadata['policy_id']}\n"
        f"Category: {best_doc.metadata['category']}\n\n"
        f"{best_doc.page_content.strip()}"
    )