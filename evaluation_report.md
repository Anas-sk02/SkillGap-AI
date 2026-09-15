# SkillGap AI — Model Evaluation Report

## Model Comparison

| Model | Accuracy | Precision | Recall | F1-Score |
|---|---|---|---|---|
| Random Forest | 0.8844 | 0.9261 | 0.8662 | 0.8952 |
| SVM | 0.8356 | 0.8398 | 0.8794 | 0.8591 |
| Naive Bayes | 0.6887 | 0.7424 | 0.6952 | 0.7180 |

## Deployed Model
**Random Forest** is selected as the production model based on overall F1-score and ability to output calibrated class probabilities via `predict_proba`.

## Dataset
- 8,000 synthetic training rows across all 16 roles (500 samples per role)
- 128 unique technical skills and 36 industry-standard projects
- 80/20 stratified train-test split (random_state=42)
- Labels generated via weighted-skill-coverage rule with Gaussian noise (sigma=0.05)
- Threshold for positive fit label: weighted coverage >= 55%

## Benchmark Notes
- SVM (RBF kernel) performs competitively but lacks interpretability
- Naive Bayes serves as the baseline; its independence assumption limits recall on correlated skill sets
- Random Forest benefits from ensemble averaging, producing stable probability estimates used by the match gauge