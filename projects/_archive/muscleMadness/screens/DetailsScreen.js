import { StyleSheet, Text, TouchableOpacity, View, ScrollView, SafeAreaView , Image } from 'react-native'
import React, { useEffect, useState } from 'react'

// app configuration
const CONFIG = require("../config/config.json")





const DetailsScreen = ({ route: { params } }) => {

    const [data, setData] = useState(false);




    // fetch api json
    const fetch_data = () => {
        // fetch("https://api.chucknorris.io/jokes/random")
        fetch(`${CONFIG.base_url}/api/${params.muscle_group}/${params.community_suggestions}`)
            .then((response) => response.json())
            .then((json) => setData(json))
            .catch((error) => console.error(error))
    }



    useEffect(() => {
        fetch_data()
    }, []);




    return (
        <View>
            {
                data.title ?
                    <View>
                        <Text>{data.title}</Text>
                        <Text>{data.description}</Text>
                        <Image source={{ uri: data.img_uri }} style={{ width: 200, height: 200 }} />
                    </View>
                    :
                    <Text> {data} </Text>
            }
        </View>
    )
}



export default DetailsScreen