import schedule
import time
from generation import ResponseGenerationAgent

def retrain_model():
    agent = ResponseGenerationAgent()
    agent.retrain_model()
    print("Model retrained successfully.")

# Schedule retraining daily at 3 AM
schedule.every().day.at("03:00").do(retrain_model)

while True:
    schedule.run_pending()
    time.sleep(1)
