from urllib.parse import urlparse


# get subdomain name   
def get_subDomain(url):
    try:
        # (name.example.com) -> example.com
        return urlparse(url).netloc
    except:
        return ""
    


# get subdomain name   
def get_DomainName(url):
    try:
        results =  get_subDomain(url).split(".")
        return results[-2] + "." +  results[-1]
    except:
        return ""
    



