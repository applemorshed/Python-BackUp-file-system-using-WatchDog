# Hossain Morshed
# Date: April 12 2020

# ------------Note-----------------
# Make sure destination folder is not exists. if exists remove or delete the destination folder. if destination folder already
# exists shutil can not copy the source folder .


import time
import datetime
import shutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from concurrent.futures import ThreadPoolExecutor

'''
Here I create a Log_note_file function, so that when watchdog find any modification or change,
it keep a log file in same folder as event_log_file_watchdog.txt file, which is easy to track if there is any change.
'''
def log_note_file(data):
    #import datetime
    x = datetime.datetime.now()
    file_obj = open("event_log_file_watchdog.txt", "a")
    file_obj.write("%s - %s\n" % (x.strftime("%m-%d-%Y %H:%M:%S"), data))
    file_obj.close()


'''
This LoggingEventHandler is the Original LoggingEventHandler from WatchDog Module, Below i modified the file
For this programming purpose.
'''


class LoggingEventHandler(FileSystemEventHandler):
    """Logs all the events captured."""

    def on_moved(self, event):
        super(LoggingEventHandler, self).on_moved(event)

        what = 'directory' if event.is_directory else 'file'
        log_info = "Moved %s: from %s to %s" % (what, event.src_path, event.dest_path)
        x = datetime.datetime.now()
        print("%s - %s" % (x.strftime("%m-%d-%Y %H:%M:%S"), log_info))
        log_note_file(log_info)

    def on_created(self, event):
        super(LoggingEventHandler, self).on_created(event)

        what = 'directory' if event.is_directory else 'file'
        log_info = "Created %s: %s" % (what, event.src_path)
        x = datetime.datetime.now()
        print("%s - %s" % (x.strftime("%m-%d-%Y %H:%M:%S"), log_info))
        log_note_file(log_info)

    def on_deleted(self, event):
        super(LoggingEventHandler, self).on_deleted(event)

        what = 'directory' if event.is_directory else 'file'
        log_info = "Deleted %s: %s" % (what, event.src_path)
        x = datetime.datetime.now()
        print("%s - %s" % (x.strftime("%m-%d-%Y %H:%M:%S"), log_info))
        log_note_file(log_info)
        shutil.rmtree(dst)
        shutil.copytree(src, dst)

    def on_modified(self, event):
        super(LoggingEventHandler, self).on_modified(event)

        what = 'directory' if event.is_directory else 'file'
        log_info = "Modified %s: %s" % (what, event.src_path)
        x = datetime.datetime.now()
        print("%s - %s" % (x.strftime("%m-%d-%Y %H:%M:%S"), log_info))
        log_note_file(log_info)
        shutil.rmtree(dst)
        shutil.copytree(src, dst)


class FileBackupManager:

    def __init__(self):
        self.observer = Observer()
        self.FileSystemEventHandler = FileSystemEventHandler()
        self.src = src
        self.dst = dst

    def start(self, src, dst):
        #shutil.rmtree(dst) # if destination file is already exists comment out this line.
        shutil.copytree(src, dst)
        event_handler = LoggingEventHandler()
        self.observer.schedule(event_handler, self.src, recursive=True)
        self.observer.start()


    def stop(self):
        self.observer.stop()
        print("Watchdog/Backup Process Terminated")
        self.observer.join()


src = "/Users/Hossain/Desktop/rwprog" # Source file which we want to make backup.
dst = "/Users/Hossain/Desktop/dst_test" # Location/destination where we want to create backup.
watch = FileBackupManager()
with ThreadPoolExecutor(max_workers=5) as executor:
    executor.submit(watch.start, src, dst)
    # we are creating a switch to terminate watchdog/backup process.
    stop_watchdog = ''
    while stop_watchdog != 'q':
        print("Backup/WatchDog is running behind. To stop Backup process/Watchdog at any time please enter q followed by Enter Button. \n")
        while True:
            stop_watchdog = input("Enter q for quit:\n")
            if stop_watchdog.lower() not in ('q'):
                print("'Invalid entry' please enter q followed by Enter for quite Watchdog/Backup process. \n")
            else:
                break
        executor.submit(watch.stop)
