from crontab import CronTab
import os

def schedule_monthly_job():
    cron = CronTab(user=True)

   python_path = '/home/student/backend/project/pulse-shift-backend/greensmtaanienv/bin/python3' # The python interpreter path for the project
   script_path = os.path.abspath('api/nutrition.py')  
    command = f'{python_path} {script_path}'

    
    for job in cron.find_command(command): #Removing existing job with the same command to avoid duplicates
        cron.remove(job)

    job = cron.new(command=command, comment='Monthly nutrition job')

    # schedule: in minute, hour, day of month, month, day of week
    # 0 1 1 * * which means at 01:00 AM on day 1 of every month the script will run
    job.setall('0 1 1 * *')

    cron.write()
    print("Monthly cron job scheduled successfully.")

if __name__ == "__main__":
    schedule_monthly_job()
