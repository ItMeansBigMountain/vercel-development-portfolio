import React, { useEffect, useState } from 'react'

import {
    Platform, StyleSheet, Text, TextInput, View,
    Dimensions, TouchableOpacity, Button, Alert, Image,
    ImageBackground, StatusBar, Picker
} from 'react-native';


// IMAGE PICKER
import * as ImagePicker from "expo-image-picker"





// app configuration
const CONFIG = require("../config/config.json")







const AddWorkout_Screen = ({ route: { params }, navigation }) => {

    // POSTING VARIABLE STATES
    const [title, set_title] = useState("");
    const [description, set_description] = useState("");
    const [category, set_category] = useState("Abs");
    // const [author, set_author] = useState("");
    // const [email, set_email] = useState("");
    // const [phone, set_phone] = useState("");
    // const [img_uri, set_img_uri] = useState("");
    // const [img, set_img] = useState("");


    // upload image
    const [hasGallary_permissions, set_galleryPermission] = useState(null);
    const [singleFile, setSingleFile] = useState(null);


    // MAKE SURE APP HAS PERMISSIONS TO ACCESS FILES
    useEffect(
        async () => {
            const galleryStatus = await ImagePicker.requestMediaLibraryPermissionsAsync();
            set_galleryPermission(galleryStatus.status === 'granted')
        }, []);


    // SELECT FILE BUTTON FUNCTION
    const selectFile = async () => {
        let result = await ImagePicker.launchImageLibraryAsync(
            {
                // IMAGE PICKING OPTIONS
                mediaTypes: ImagePicker.MediaTypeOptions.All,
                allowsEditing: true,
                aspect: [4, 3],
                quality: 1
            }
        )

        // IF USER CANCELS UPLOAD
        if (!result.cancelled) {
            setSingleFile(result)
        }

        // NO PERMISSIONS
        if (hasGallary_permissions === false) {
            return <Text> No access to files </Text>
        }
    }


    // // FINAL DATA POST TO API
    const submitData = async () => {
        if (singleFile != null) {

            // INIT POST JSON OBJECT
            const fileToUpload = singleFile;

            const data = {
                title: title,
                description: description,
                category: category,
                community_contrib: true,
                img_uri: fileToUpload.uri,

                author: "affan",
                email: "fareed320@gmail.com",
                phone: "6309232300",

            }


            // POST DATA TO API
            let res = await fetch(
                `${CONFIG.base_url}/api/`,
                {
                    method: 'post',
                    body: JSON.stringify(data),
                    headers: {
                        'Accept': 'application/json',
                        'Content-Type': 'application/json'
                    },
                }
            );

            // API RESPONSE 
            let responseJson = await res.json();
            // console.log(responseJson)
            alert(responseJson.res);
            navigation.navigate("Home")
        }

        // If no file selected the show alert
        else {
            alert('Please Select File first');
        }

    };



    return (
        <ImageBackground
            source={require('../assets/camo.png')}
            imageStyle={{ resizeMode: 'stretch' }}
            style={{ width: '100%', height: '100%' }}>


            {/* USER INPUT */}
            <View style={styles.container}>

                {/* title */}
                <Text style={styles.input}>Exercise Details</Text>


                {/* workout name */}
                <View style={styles.inputContainer}>
                    <TextInput style={styles.inputs}
                        placeholder="Workout Title"
                        keyboardType="default"
                        underlineColorAndroid='transparent'
                        onChangeText={(name) => set_title(name)} />
                </View>


                {/* workout desc */}
                <View style={styles.inputContainer}>
                    <TextInput style={styles.inputs}
                        placeholder="Description / Instructions"
                        keyboardType="default"
                        underlineColorAndroid='transparent'
                        onChangeText={(desc) => set_description(desc)} />
                </View>


                {/* CATEGORY */}
                <Picker
                    selectedValue={category}
                    style={{ height: 50, width: 150 }}
                    onValueChange={(itemValue, itemIndex) => set_category(itemValue)}
                >
                    {/* ALL MUSCLE GROUPS CHOICES */}
                    {params.Muscle_list.map(
                        (item, index) => {
                            return <Picker.Item label={item} value={item} key={index} />
                        }
                    )}
                </Picker>



                {/* UPLOAD IMAGE */}
                <TouchableOpacity
                    style={styles.submitButton}
                    activeOpacity={0.5}
                    onPress={selectFile}>
                    <Text style={styles.buttonTextStyle}>Select File</Text>
                </TouchableOpacity>




                {/* DEBUG */}
                {singleFile && <Image source={{ uri: singleFile.uri }} style={{ width: 200, height: 200 }} />}








                {/* user phone  */}
                {/* <View style={styles.inputContainer}>
                    <TextInput style={styles.inputs}
                        placeholder="Phone Number"
                        keyboardType="phone-pad"
                        underlineColorAndroid='transparent'
                        onChangeText={(phone_number) => setMobileNumber({ phone_number })} />
                </View> */}







                {/* SUBMIT DATA!!! */}
                <TouchableOpacity style={styles.submitButtonText} onPress={submitData}>
                    <Text style={styles.signUpText}> Submit! </Text>
                </TouchableOpacity>

            </View>



        </ImageBackground>

    )
}




const styles = StyleSheet.create({
    container: {
        flex: 1,
        justifyContent: 'center',
        alignItems: 'center',
    },
    input: {
        margin: 15,
        fontSize: 40,
        marginBottom: 40,
        color: 'blue'
    },
    submitButton: {
        backgroundColor: '#7a42f4',
        padding: 10,
        margin: 15,
        height: 60,
    },
    submitButtonText: {
        color: '#FFFFFF',
        backgroundColor: '#3462FD',
        width: 350,
        height: 45,
        borderRadius: 10,
        justifyContent: 'center',
        alignItems: 'center'
    },
    signUpText: {
        color: '#FFFFFF',
        alignItems: 'center'
    },
    inputContainer: {
        borderBottomColor: '#05C203',
        backgroundColor: '#FFFFFF',
        borderRadius: 5,
        borderBottomWidth: 1,
        width: 350,
        height: 45,
        marginBottom: 20,
        flexDirection: 'row',
        alignItems: 'center'
    },
    inputs: {
        height: 45,
        marginLeft: 16,
        borderBottomColor: '#FFFFFF',
        flex: 1,
    },

    // TUTORIAL
    buttonTextStyle: {
        color: '#FFFFFF',
        paddingVertical: 10,
        fontSize: 16,
    },
    textStyle: {
        backgroundColor: '#fff',
        fontSize: 15,
        marginTop: 16,
        marginLeft: 35,
        marginRight: 35,
        textAlign: 'center',
    },



})






export default AddWorkout_Screen