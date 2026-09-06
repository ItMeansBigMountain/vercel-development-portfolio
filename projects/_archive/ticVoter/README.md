API ENDPOINT IN /api_config
    change firebase.js api keys as well


npm install @react-navigation/native

expo install react-native-screens react-native-safe-area-context

npm install @react-navigation/native-stack

expo install firebase@8.2.3 

npm i react-native-community/async-storage

npm install moment


RECONFIG FIREBASE API FILE KEYS WITH NEW APP BEFORE DEPLOYMENT
    UNSAFE DB, add security 





CONFIGURATION FILES

    ../api_config/

        /config.json <---- api base url 

        /DataServer.js <----- serves chunked data to scroll view

        /firebase.js <---- firebase account api credentials

StartUP PROCEDURE

    REACT APP

        ../ticVoter

            'npm start' 
    
    REST_API

        ../ticRate_API

            'python manage.py runserver'






todo:

    CLOUD
        upload ticRate_API to cloud
        
        Change config base url to cloud server endpoint


    Ticker Display
        display previous votes




