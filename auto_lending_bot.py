import schedule
import time
from pmLendingBot import LendingStakingBot


lendingStaking = LendingStakingBot()

def job():
    print(time.ctime())
    lendingStaking.loop()

job()

schedule.every().hour.at(":00").do(job)
schedule.every().hour.at(":30").do(job)

while True:
    schedule.run_pending()
    time.sleep(1)