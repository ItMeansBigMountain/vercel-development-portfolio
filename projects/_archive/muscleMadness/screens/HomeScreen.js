import { StyleSheet, Text, TouchableOpacity, View, ScrollView, SafeAreaView } from 'react-native'
import React, { useEffect, useState } from 'react'
import { useNavigation } from '@react-navigation/core';
import { Button } from 'react-native-web';
import CButton from '../components/Cbutton';





// app configuration
const CONFIG = require("../config/config.json")






const HomeScreen = ({ navigation }) => {


    // STATES
    const [Muscle_list, setMuscle_list] = useState([
        'Abs',
        'Arms',
        'Back',
        'butt-hips',
        'Chest',
        'full-body-integrated',
        'legs-calves-and-shins',
        'Neck',
        'Shoulders',
        'legs-thighs',
    ]);
    const [community_suggestions, set_community_suggestions] = useState(false)



    // FETCH API 
    const fetch_data = () => {
        fetch(`${CONFIG.base_url}/api/workout-keys`)
            .then((response) => response.json())
            .then((json) => setMuscle_list(json))
            .catch((error) => console.error(error))
    }

    // ON PAGE RENDER
    useEffect(() => {
        fetch_data()
    }, []);








    // EACH MUSCLE GROUP BUTTON
    function capitalizeFirstLetter(string) {
        return string.charAt(0).toUpperCase() + string.slice(1);
    }
    const renderItem = (item, i) => {
        return (
            <View key={i} style={styles.Button_View}>
                <TouchableOpacity
                    style={styles.text_button}
                    onPress={() => {
                        // passing args to new screen
                        navigation.navigate("Details", {
                            muscle_group: item,
                            community_suggestions: community_suggestions
                        })

                    }}
                >
                    <Text>{capitalizeFirstLetter(item)}</Text>
                </TouchableOpacity>
            </View>
        )
    }

    // PAGE RENDER
    return (
        <View style={{ flex: 1 }}>

            <SafeAreaView >
                <View style={styles.Option_Buttons}>

                    {/* ADD WORKOUT  */}
                    <CButton
                        text={"Add Workout!"}
                        action={
                            () => navigation.navigate("ADD WORKOUT", { Muscle_list: Muscle_list })
                        }
                        bg="red"
                    />


                    {/* TOGGLE COMMUNITY SUGGESTIONS */}
                    {
                        community_suggestions ?
                            <CButton text={"Toggle Community Suggestions [ON] "} action={() => set_community_suggestions(!community_suggestions)} bg="green" />
                            :
                            <CButton text={"Toggle Community Suggestions [OFF]"} action={() => set_community_suggestions(!community_suggestions)} bg="blue" />
                    }
                </View>
            </SafeAreaView>


            {/* LIST OF BUTTONS  */}
            <ScrollView>{Muscle_list.map(renderItem)}</ScrollView>
        </View>
    );
}









const styles = StyleSheet.create({
    Button_View: {
        flex: 1,
        marginBottom: 5
    },
    Option_Buttons: {
        flexDirection: "row",
        justifyContent: "space-around",

    },


    text_button: {
        margin: 4,
        backgroundColor: "orange",
        width: "100%",
        height: 50,
        alignItems: "center",
        justifyContent: "center",
        borderBottomWidth: 2,
        flexWrap: 'wrap',
        flexDirection: 'row',
    },


});


export default HomeScreen