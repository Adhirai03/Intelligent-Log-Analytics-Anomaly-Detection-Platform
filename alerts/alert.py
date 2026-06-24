def generate_alert(prediction):

    if prediction == 1:
        print("ALERT: Anomaly Detected!")
    else:
        print("System Normal")