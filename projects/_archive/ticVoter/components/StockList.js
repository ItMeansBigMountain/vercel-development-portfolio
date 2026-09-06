import { StyleSheet, Text, TouchableOpacity, View, FlatList } from 'react-native'
import React, { useEffect, useState } from 'react'



const StockList = () => {


    // states and fetch data function
    const [isLoading, setLoading] = useState(false);
    const [all_stocks, setStocksData] = useState([])
    const fetchData = () => {
        fetch(`${CONFIG.base_url}/api/build_internal`)
            .then((response) => response.json())
            .then((json) => setStocksData(json))
            .catch((error) => console.error(error))
            .finally(() => setLoading(false));
    }

    // on page render
    useEffect(() => {
        setLoading(true);
        fetchData();
    }, []);


    return (
        <View style={{ padding: 20 }}>
            {isLoading ? <Text>Loading...</Text> :
                (
                    <FlatList
                        data={all_stocks}
                        keyExtractor={({ id }) => id}
                        renderItem={({ item }) => <Text>{item.name}  </Text>}
                    />
                )}
        </View>
    );
};

export default StockList