# German Rent Estimator

Predicts monthly base rent (Kaltmiete) for German apartments using machine learning.

## Business Problem
Renters and landlords need fair price estimates. This app predicts rent from apartment features.

## Dataset
Dataset link : (https://www.kaggle.com/datasets/corrieaar/apartment-rental-offers-in-germany)

Apartment rental offers in Germany (Kaggle, ImmoScout24) — 268,850 listings.
After cleaning junk values: 267,184 rows.

## Approach
- Cleaned data: removed junk rents (€0 and €9,999,999), selected 15 key features.
- Baseline: Linear Regression — MAE €175, R² 0.650
- Main model: LightGBM Regressor — MAE €100, R² 0.864
- Top features: city/district, living space, state.

## Live App
(https://german-rent-estimator-xbdwgrjzta7r2rnxpbtupk.streamlit.app/)

## Demo Video
[Video link — [add after recording]](https://drive.google.com/file/d/1n8XVt3KVlFx0MB9x-lFpx_ZokEF0jLyD/view)

## How to Run
1. `pip install -r requirements.txt`
2. `streamlit run streamlit_app.py`
