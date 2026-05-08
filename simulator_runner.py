import schedule
import time
from utils.data_simulator import run_simulation

# Schedule simulation every 5 minutes
schedule.every(5).minutes.do(run_simulation)

if __name__ == "__main__":
    print("Starting data simulator...")
    while True:
        schedule.run_pending()
        time.sleep(1)
