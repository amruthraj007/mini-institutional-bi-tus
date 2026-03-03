Student Success & Risk Segmentation Model

Objective: 
Develop a transparent and interpretable composite success score to segment Year 1 students into risk categories for early identification and intervention planning.

This model is designed for demonstration purposes and does not represent a statistically optimised predictive algorithm.

Variables Used:
- GPA (0–4 scale)
- Attendance Rate (0–100 scale)

Both variables were selected to represent academic performance and engagement.

Normalisation:
To ensure balanced weighting, GPA is converted to a 0–100 scale:

GPA (100 Scale) = (gpa / 4) × 100

This aligns GPA with attendance for comparability.

Success Score Formula:

Success Score = 0.5 × GPA (100 scale) + 0.5 × Attendance Rate

Both components are weighted equally to ensure balanced contribution.

Risk Band Classification:

Students are segmented into risk bands based on Success Score:

- Low Risk: ≥ 85
- Medium Risk: 70–84
- High Risk: < 70

Thresholds are heuristic and designed for interpretability.

Model Validation:
Validation was conducted by comparing retention outcomes across risk bands.

Results demonstrate a monotonic relationship:

Low Risk > Medium Risk > High Risk (Retention Rate)

This confirms the model meaningfully differentiates student outcomes.