import { StyleSheet, Text, TouchableOpacity, View, ScrollView } from 'react-native'
import React, { useEffect, useState } from 'react'
var moment = require('moment');


const CONFIG = require("../api_config/config.json")









const WeekExpirationDisplay = () => {

    const [timeRN, setTimeRN] = useState(new Date().toLocaleString())
    const [experation_date, setExperationDate] = useState('')
    const [display_date, setDisplayDate] = useState('')


    const fetchDate = () => {
        fetch(`${CONFIG.base_url}/api/vote_experation_date`)
            .then((response) => response.json())
            .then((json) => {
                setExperationDate(json.date)

                let days_until_experation_date = moment(Date.parse(json.date)).add(7,'days').fromNow()
                setDisplayDate(days_until_experation_date)
                
            })
            .catch((error) => console.error(error))
    }


    // on page render
    useEffect(() => {
        fetchDate();
    }, []);





    return (

        <View style={styles.time_display}>
            <Text style={styles.experation_text}> EXPERATION {experation_date.length > 0 ? display_date : "Connection Error"}  </Text>
        </View>
    )
}


const styles = StyleSheet.create(
    {
        time_display: {
            justifyContent: "center",
            alignItems: "center",
        },
        experation_text: {
            fontWeight: 'bold',
            fontSize: 20
        }
    }
)





export default WeekExpirationDisplay