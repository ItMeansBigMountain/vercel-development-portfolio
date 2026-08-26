import Generate_Files
from domain import get_DomainName
from spider import Spider


import threading
from queue import Queue


# HOMEPAGE = "https://www.cnn.com"
# HOMEPAGE = "https://www.foxbusiness.com/"
HOMEPAGE = "https://www.youtube.com"


DOMAIN_NAME = get_DomainName(HOMEPAGE)
PROJECT_NAME = f"{DOMAIN_NAME.split('.')[0]}-link-map"


QUEUE_FILE = PROJECT_NAME + "/queue.txt"
CRAWLED_FILE = PROJECT_NAME + "/crawled.txt"
NUMBER_OF_THREADS = 8

queue = Queue()
Spider(PROJECT_NAME, HOMEPAGE, DOMAIN_NAME , exterior_urls=False)






def work():
    while True:
        url = queue.get()
        Spider.crawl_page(threading.current_thread().name, url)
        queue.task_done()


def create_workers():
    # create worker threads 
    for _ in range(0 , NUMBER_OF_THREADS , 1):
        t = threading.Thread(target=work)
        t.daemon = True # (will die when main exits)
        t.start()





def create_jobs():
    # each queued link is a new job
    for link in Generate_Files.file_to_set(QUEUE_FILE):
        queue.put(link)
    queue.join()
    crawl()


def crawl():
    # Check if there are items in the todo list
    queued_links = Generate_Files.file_to_set(QUEUE_FILE)
    if len(queued_links) > 0:
        print(f"Queued links left: {len(Spider.queue)}")
        create_jobs()




create_workers()
crawl()
