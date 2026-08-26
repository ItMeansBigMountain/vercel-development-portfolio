import os

# create project dir
def create_project_directory(project_name):
    if not os.path.exists(project_name):
        os.makedirs(project_name)
    else: print("DIR ALREADY EXISTS!")


# Create Queue and Crawled Files
def create_data_files(project_name, base_url ):
    queue = project_name + '/queue.txt'
    crawled = project_name + '/crawled.txt'

    # check if waiting list and already scanned website files exist
    if not os.path.isfile(queue):
        write_file(queue, base_url)
    if not os.path.isfile(crawled):
        write_file(crawled, "")

def write_file(filepath , data):
    with open(file=filepath, mode="w") as f:
        f.write(data)


# Add Data To File
def append_data_to_file(filepath , data):
    with open(filepath,"a") as file:
        file.write(data)
        file.write('\n')


# Clear Contents In A File
def clear_file_contents():
    with open(filepath,"w") as file: 
        pass


# Read A File and Add to set
def file_to_set(filename):
    results = set()
    with open(filename, "rt") as f:
        for line in f:
            results.add(line.replace("\n",""))
    return results


# Convert Set into File
def set_to_file(set_of_links , filename):
    with open(filename,"w") as f:
        for x in sorted(set_of_links):
            f.write(x)
            f.write("\n")





