# SkillGap AI — Model Evaluation Report

## Model Comparison

| Model | Accuracy | Precision | Recall | F1-Score |
|---|---|---|---|---|
| Random Forest | 0.9060 | 0.9267 | 0.9036 | 0.9150 |
| SVM | 0.9120 | 0.9126 | 0.9321 | 0.9223 |
| Naive Bayes | 0.8020 | 0.8267 | 0.8179 | 0.8223 |

## Deployed Model
**Random Forest** is selected as the production model based on overall F1-score and ability to output calibrated class probabilities via `predict_proba`.

## Dataset
- 2,500 synthetic training rows across 4 roles
- 80/20 stratified train-test split (random_state=42)
- Labels generated via weighted-skill-coverage rule with Gaussian noise (sigma=0.05)
- Threshold for positive fit label: weighted coverage >= 55%

## Benchmark Notes
- SVM (RBF kernel) performs competitively but lacks interpretability
- Naive Bayes serves as the baseline; its independence assumption limits recall on correlated skill sets
- Random Forest benefits from ensemble averaging, producing stable probability estimates used by the match gauge