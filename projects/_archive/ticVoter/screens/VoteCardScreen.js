import { StyleSheet, Text, View, Button } from 'react-native'
import React, { useEffect, useState } from 'react'


// config
import { auth } from "../api_config/firebase";
const CONFIG = require("../api_config/config.json")





const VoteCardScreen = ({ route }) => {

    const user_varified = auth.currentUser.emailVerified
    // STATES
    const [display_date_ticker, setDisplay_data_ticker] = useState('')
    const [display_date_voteCard, setDisplay_data_voteCard] = useState('')




    // DISPLAY_INFO FETCH DATA
    const ticker_info =  (ticker) => {
        fetch(`${CONFIG.base_url}/api/tickers/${ticker}`)
            .then((response) => response.json())
            .then((json) => setDisplay_data_ticker(json))
            .catch((error) => console.error(error))
    }

    const voteCard_info =  (ticker) => {
        fetch(`${CONFIG.base_url}/api/votes/${ticker}`)
            .then((response) => response.json())
            .then((json) => setDisplay_data_voteCard(json))
            .catch((error) => console.error(error))
    }


    


    // POST VOTES
    const vote = async (ticker, opinion) => {
        let response = await fetch(`${CONFIG.base_url}/api/votes/${ticker}/${opinion}`, {
            method: 'POST',
            headers: { Accept: 'application/json', 'Content-Type': 'application/json' },
            body: JSON.stringify({ user: auth.currentUser }),
        });

        let json = await response.json();
        ticker_info(route.params.data.ticker)
        voteCard_info(route.params.data.ticker)
        return json;
    }




    // on render, check if user is logged in or not
    useEffect(
        () => {
            ticker_info(route.params.data.ticker)
            voteCard_info(route.params.data.ticker)
        }, []
    )


    
    return (
        <View style={styles.container}>



            {/* DISPLAY DATA */}
            <Text>{route.params.data.name} | {route.params.data.ticker}</Text>
            <Text>ETF? {route.params.data.is_etf ? "yes" : "no"}</Text>
            <Text>{route.params.data.exchange}</Text>
            <Text>{display_date_ticker.history}</Text>

            <Text>{`${display_date_voteCard.up_vote} : ${display_date_voteCard.down_vote} `}</Text>










            <View style={styles.fixToText}>

                {/* up */}
                <Button
                    title={user_varified ? ' up! ' : 'Please Validate'}
                    onPress={() => vote(route.params.data.ticker, 'up')}
                    color="#00FF00"
                    disabled={!user_varified ? true : false}
                />

                {/* down */}
                <Button
                    title={user_varified ? ' down! ' : 'Email'}
                    onPress={() => vote(route.params.data.ticker, 'down')}
                    color="#FF0000"
                    disabled={!user_varified ? true : false}
                />

            </View>




        </View>
    )
}






const styles = StyleSheet.create(
    {
        container: {
            flex: 1,
            justifyContent: "center",
            alignItems: "center",
        },
        fixToText: {
            flexDirection: 'row',
            justifyContent: 'space-between',
        },
        upButton: {
            flex: 1
        },
        downButton: {
            flex: 1
        },

    }
)






export default VoteCardScreen
