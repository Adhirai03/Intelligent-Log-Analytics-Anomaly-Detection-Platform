from explainability.shap_analysis import *

row = 15

print("Prediction:")
print(predict_row(row))

print("\nConfidence:")
print(prediction_probability(row))

print("\nExplanation:")
print(generate_explanation(row))

print("\nTop Features:")
print(get_top_features(row))