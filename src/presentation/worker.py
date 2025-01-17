import time

import schedule

from src.core import Core


def post_paid_automation_charge():
    print("Starting Job: post_paid_automation_charge")
    core = Core()
    core.charge_debit.charge_debit()


# Listing all jobs
schedule.every().day.at("02:00").do(post_paid_automation_charge)

if __name__ == "__main__":
    print("Starting Jobs")
    while True:
        schedule.run_pending()
        time.sleep(1)
