import React, { useEffect, useState } from 'react';
import { FlatList, StyleSheet, Text, View, TouchableOpacity, TextInput, Button } from 'react-native';
import { useNavigation } from '@react-navigation/core';



import { fetch_rendered_data } from '../api_config/DataServer';

// const CONFIG = require("../api_config/config.json") 
const CONFIG = require("../api_config/config.json")
const quantity_rendered = CONFIG.qty_rendered




// config
import { auth } from "../api_config/firebase";








// check to halt load requests
let stopFetchMore = true;



// LOADING VIEW
const ListFooterComponent = () => (
    <Text
        style={{
            fontSize: 16,
            fontWeight: 'bold',
            textAlign: 'center',
            padding: 5,
        }}
    >
        Loading...
    </Text>
);




// MAIN COMPONENT
const ScrollLoad = () => {

    // SCREEN STACK
    const navigation = useNavigation()

    // const quantity_rendered = CONFIG.qty_rendered;




    // STATES RENDER LIST
    const [data, setData] = useState([]);
    const [render_index, set_render_index] = useState(0);
    const [loadingMore, setLoadingMore] = useState(false);
    const [search, setSearch] = useState('');
    const [all_stocks, setStocksData] = useState([])
    const build_data = () => {
        fetch( `${CONFIG.base_url}/api/build_internal` )
            .then((response) => response.json())
            .then((json) => setStocksData(json))
            .catch((error) => console.error(error))
    }





    // STATES VOTE CARDS
    const user_varified = auth.currentUser.emailVerified
    const [display_date_ticker, setDisplay_data_ticker] = useState('')
    const [display_date_voteCard, setDisplay_data_voteCard] = useState('')
    // DISPLAY_INFO FETCH DATA
    const ticker_info = (ticker) => {
        fetch(`${CONFIG.base_url}/api/tickers/${ticker}`)
            .then((response) => response.json())
            .then((json) => setDisplay_data_ticker(json))
            .catch((error) => console.error(error))
    }
    const voteCard_info = (ticker) => {
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
        ticker_info( ticker)
        voteCard_info( ticker)
        return json;
    }







    // HOOK : on page render
    useEffect(async () => {
        // RENDER DATA
        updateData()
        build_data()

        // // VOTE CARD
        // ticker_info(item.data.ticker)
        // voteCard_info(item.data.ticker)
    }, []);




    // DATA ARRAY ITEM VIEW
    const renderItem = ({ item }) => {

        return (

            <View style={styles.vote_card}>
                <TouchableOpacity
                    onPress={() => {
                        navigation.navigate("Vote", { data: item })
                    }}
                    style={styles.stock_button}
                    activeOpacity={0.25}
                >
                    <Text title={styles.stock_button_text} >
                        {item.ticker}  : {item.name}
                    </Text>
                </TouchableOpacity>


                <View style={styles.fixToText}>

                    {/* up */}
                    <Button
                        title={user_varified ? ' up! ' : 'Please Validate'}
                        onPress={() => vote(item.ticker, 'up')}
                        color="#00FF00"
                        disabled={!user_varified ? true : false}
                    />

                    {/* down */}
                    <Button
                        title={user_varified ? ' down! ' : 'Email'}
                        onPress={() => vote(item.ticker, 'down')}
                        color="#FF0000"
                        disabled={!user_varified ? true : false}
                    />

                </View>
            </View>

        );
    };


    // UPDATE STATE OF DISPLAY DATA VIA SCROLL
    const updateData = async () => {
        set_render_index(render_index + quantity_rendered)
        // gets data from server.js
        const response = await fetch_rendered_data(quantity_rendered, render_index)
        // check if we got data from DataServer.js
        if (response) setData([...response]);
        else setData(["error", "DataServer.js", "didnt return the promise"])
    };



    // load more unless server resolves done
    const handleOnEndReached = async () => {
        setLoadingMore(true);
        if (!stopFetchMore) {
            const response = await fetch_rendered_data(quantity_rendered, render_index); //fetch
            if (response === 'done') return setLoadingMore(false);
            stopFetchMore = true;
            setData([...data, ...response]); // append to [state list]
            set_render_index(render_index + quantity_rendered) // add 20 to last index
        }
        setLoadingMore(false);
    };





    // SEARCH BAR
    const searchFilterFunction = (text) => {
        // console.log(all_stocks)

        // Check if searched text is not blank
        if (text) {
            const newData = all_stocks.filter(function (item) {
                // console.log(item)

                // Applying filter for the inserted text in search bar
                const itemData =
                    item.name.toUpperCase().includes(text.toUpperCase()) ||
                        item.ticker.toUpperCase().includes(text.toUpperCase())
                        ? item.ticker : ''
                const textData = text.toUpperCase();
                return itemData.indexOf(textData) > -1;
            });
            setData(newData);
            setSearch(text);
        } else {
            // Inserted text is blank
            setSearch(text);
            set_render_index(0)
            updateData()
        }
    };






    return (
        <View>



            {/* SEARCH */}
            <View style={styles.search_bar_container}>
                <TextInput
                    style={styles.textInputStyle}
                    onChangeText={(text) => searchFilterFunction(text)}
                    value={search}
                    underlineColorAndroid="transparent"
                    placeholder="Search Here"
                />
            </View>







            {/* DISPLAY */}
            <FlatList
                data={data}
                keyExtractor={item => data.indexOf(item)}
                renderItem={renderItem}
                onEndReached={handleOnEndReached}
                onEndReachedThreshold={0.01}
                onScrollBeginDrag={() => {
                    stopFetchMore = false;
                }}
                ListFooterComponent={() => loadingMore && <ListFooterComponent />}
            // onScroll={(event) => console.log(event)}
            />




        </View>

    );
}









const styles = StyleSheet.create({

    textInputStyle: {
        height: 50,
        width: "100%",
        borderWidth: 1,
        paddingLeft: 20,
        margin: 50,
        borderColor: '#009688',
        backgroundColor: '#FFFFFF',
    },
    search_bar_container: {
        backgroundColor: '#000000',
        alignItems: 'center',
        justifyContent: 'center',
        marginTop: 25,
        height: 55,
    },



    vote_card: {
        flex: 1,
        margin: 10
    },
    
    stock_button: {
        flex: 2,
        textAlign: 'center',
        fontWeight: 'bold',
        fontSize: 20,
        padding: 15,
        borderBottomColor: '#009688',
        borderBottomWidth: 2,
    },
    stock_button_text: {
        textAlign: 'center',
        fontWeight: 'bold',
        fontSize: 20,
        padding: 15,
        borderBottomColor: '#009688',
        borderBottomWidth: 2,
    },


    fixToText: {
        flex: 3,
        flexDirection: 'row',
        justifyContent: 'space-between',
    },
    upButton: {
        flex: 1
    },
    downButton: {
        flex: 1
    },


});




export default ScrollLoad