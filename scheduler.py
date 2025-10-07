import asyncio
import threading
import os
import json
from datetime import datetime, timedelta
import pytz
from client import send_message
from config import TIMEZONE, SCHEDULE_FILE, UPLOAD_FOLDER
from logger import add_log

scheduler_running = False

def load_schedules():
    if not os.path.exists(SCHEDULE_FILE):
        with open(SCHEDULE_FILE,"w",encoding="utf-8") as f: 
            json.dump([], f)
        return []
    with open(SCHEDULE_FILE,"r",encoding="utf-8") as f:
        return json.load(f)

async def schedule_task_runner(task):
    tz = pytz.timezone(TIMEZONE)
    while scheduler_running:
        now = datetime.now(tz)
        send_time = None

        if task["type"] == "date":
            send_time = tz.localize(datetime.strptime(task["when"], "%Y-%m-%d %H:%M"))
        elif task["type"] == "cron":
            hh, mm = map(int, task.get("time","00:00").split(":"))
            send_time = now.replace(hour=hh, minute=mm, second=0, microsecond=0)
            if send_time < now:
                send_time += timedelta(days=1)
        else:
            break

        delta = (send_time - now).total_seconds()
        if delta > 0: 
            await asyncio.sleep(delta)

        file_path = task.get("file")
        if file_path: 
            file_path = os.path.join(UPLOAD_FOLDER, file_path)

        await send_message(task["to"], task["message"], file_path)

        if task["type"] == "date":
            break
        await asyncio.sleep(60)

async def run_scheduler_tasks():
    tasks = load_schedules()
    runners = [asyncio.create_task(schedule_task_runner(task)) for task in tasks]
    add_log("✅ Scheduler started.")
    if runners:
        await asyncio.gather(*runners)
    add_log("🛑 Scheduler finished.")

def start_scheduler():
    global scheduler_running
    if scheduler_running:
        return
    scheduler_running = True
    def run_loop():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(run_scheduler_tasks())
    threading.Thread(target=run_loop, daemon=True).start()

def stop_scheduler():
    global scheduler_running
    scheduler_running = False
    add_log("🛑 Stop signal sent.")
