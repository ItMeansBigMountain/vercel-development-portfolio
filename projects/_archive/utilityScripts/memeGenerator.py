def memeGeneration(quote):
    #login
    username = ''
    password = ''

    #fetch all memes
    data = requests.get('https://api.imgflip.com/get_memes').json()['data']['memes']
    images = [{'name':image['name'],'url':image['url'],'id':image['id']} for image in data]
    
    
    # print all avail. memes
    # print('\n\nHere is the list of available memes : \n')
    # ctr = 1
    # for img in images:
    #     print(ctr,img['name'])
    #     ctr = ctr+1

    #split discord command into an array
    commands = quote.split()
    text0 = ''
    text1 = ''
    id = random.randint(0,100)
    id = checkFor_BernieSanders(id)

    # choose meme by random
    print('meme id number: {}'.format(id))

    #divide and loop to splitter, start next line's loop from splitter
    splitter = int(len(commands) / 2)   
    # top line
    for i in range(0 , splitter , 1):
        text0 += commands[i] + ' '
    # bottom line
    for x in range(splitter,len(commands) , 1):
        text1 += commands[x] + ' '



    #generated meme
    URL = 'https://api.imgflip.com/caption_image'
    params = {
        'username':username,
        'password':password,
        'template_id':images[id-1]['id'],
        'text0':text0,
        'text1':text1
    }
    response = requests.request('POST',URL,params=params).json()
    print(response)

    imageURL = response['data']['url']
    return imageURL












# comma seperation meme
def memeGeneratiom_CommaSeperation(quote):
    #login
    username = 'oyamaMotivation'
    password = 'YOUR_IMGFLIP_PASSWORD'

    #fetch all memes
    data = requests.get('https://api.imgflip.com/get_memes').json()['data']['memes']
    images = [{'name':image['name'],'url':image['url'],'id':image['id']} for image in data]
    
    
    # print all avail. memes
    # print('\n\nHere is the list of available memes : \n')
    # ctr = 1
    # for img in images:
    #     print(ctr,img['name'])
    #     ctr = ctr+1

    #split discord command into an array
    commands = quote.split(',')
    text0 = ''
    text1 = ''
    id = random.randint(0,100)
    # id = checkFor_BernieSanders(id) #CHECKING FOR BERNIE SANDERS!!!!

    # choose meme by random
    print('meme id number: {}'.format(id))

    #generated meme
    URL = 'https://api.imgflip.com/caption_image'
    params = {
        'username':username,
        'password':password,
        'template_id':images[id-1]['id'],
        'text0':commands[0],
        'text1':commands[1]
    }
    response = requests.request('POST',URL,params=params).json()
    print(response)

    imageURL = response['data']['url']
    return imageURL
# checking for lame memes
def checkFor_BernieSanders(number):
    if number == 14:
        number = random.randint(15 , 100) or random.randint(0,13)
    return number