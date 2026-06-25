from utils.log_analysis import *

df = load_data("data/Event_occurrence_matrix.csv")

print("Total Logs:")
print(get_total_logs(df))

print("\nSuccess Fail:")
print(get_success_fail_counts(df))

print("\nFailure Types:")
print(get_failure_type_distribution(df).head())

print("\nTop Events:")
print(get_top_events(df))