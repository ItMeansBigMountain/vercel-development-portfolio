// react modules
import { useNavigation } from '@react-navigation/core';
import React, { useEffect, useState } from 'react'
import { KeyboardAvoidingView, Pressable, StyleSheet, Text, TextInput, View } from 'react-native'


import AsyncStorage from '@react-native-async-storage/async-storage';



// // DEVICE INFO
// import DeviceInfo from 'react-native-device-info';
// import { getUniqueId, getManufacturer } from 'react-native-device-info';


const API_URL = 'https://codology-api.vercel.app/api';




const LoginScreen = () => {
    // user input states
    const [email, setEmail] = useState('');
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [firstname, setFirstName] = useState('');
    const [lastname, setLastName] = useState('');
    const [phonenumber, setPhoneNumber] = useState('');


    // Logging in functionality states
    const [isError, setIsError] = useState(false);
    const [message, setMessage] = useState('');
    const [isLogin, setIsLogin] = useState(true);


    // Setting login function
    const onChangeHandler = () => {
        setIsLogin(!isLogin);
        setMessage('');
    };

    const onLoggedIn = token => {
        fetch(`${API_URL}/private`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`,
            },
        })
            .then(async res => {
                try {
                    const jsonRes = await res.json();
                    if (res.status === 200) {
                        setMessage(jsonRes.message);

                        // Save the token to AsyncStorage
                        await AsyncStorage.setItem('userToken', token);

                        // Navigate to the main screen 
                        navigation.navigate('Home');

                    }
                } catch (err) {
                    console.log(err);
                };
            })
            .catch(err => {
                console.log(err);
            });
    }




    // User Login submition 
    const onSubmitHandler = () => {
        const payload = {
            email,
            username,
            password,
            firstname,
            lastname,
            phonenumber,
        };
        fetch(`${API_URL}/${isLogin ? 'login' : 'signup'}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(payload),
        })
            .then(async res => {
                try {
                    const jsonRes = await res.json();
                    if (res.status !== 200) {
                        setIsError(true);
                        setMessage(jsonRes.message);
                    } else {
                        onLoggedIn(jsonRes.token);
                        setIsError(false);
                        setMessage(jsonRes.message);
                    }
                } catch (err) {
                    console.log(err);
                };
            })
            .catch(err => {
                console.log(err);
            });
    };





    // Error handling
    const getMessage = () => {
        const status = isError ? `Error: ` : `Success: `;
        return status + message;
    }




    // page navigation stack
    const navigation = useNavigation()





    // on render, check if user is logged in or not
    useEffect(() => {
        const checkToken = async () => {
            const token = await AsyncStorage.getItem('userToken');
            if (token) {
                navigation.replace('Home'); // Navigate to the Home screen if the token exists
            }
        };
        checkToken();
    }, []);



    return (
        <KeyboardAvoidingView
            style={styles.container}
            behavior="padding"
        >

            <View style={styles.card}>
                <Text style={styles.heading}>{isLogin ? 'Login' : 'Signup'}</Text>
                <View style={styles.form}>
                    <View style={styles.inputs}>
                        <TextInput style={styles.input} placeholder="Email" autoCapitalize="none" onChangeText={setEmail}></TextInput>
                        {!isLogin && <TextInput style={styles.input} placeholder="Username" onChangeText={setUsername}></TextInput>}
                        {!isLogin && <TextInput style={styles.input} placeholder="First Name" onChangeText={setFirstName}></TextInput>}
                        {!isLogin && <TextInput style={styles.input} placeholder="Last Name" onChangeText={setLastName}></TextInput>}
                        {!isLogin && <TextInput style={styles.input} placeholder="Phone Number" onChangeText={setPhoneNumber}></TextInput>}
                        <TextInput secureTextEntry={true} style={styles.input} placeholder="Password" onChangeText={setPassword}></TextInput>
                        <Text style={[styles.message, { color: isError ? 'red' : 'green' }]}>{message ? getMessage() : null}</Text>
                        <Pressable style={styles.button} onPress={onSubmitHandler}>
                            <Text style={styles.buttonText}>Done</Text>
                        </Pressable>
                        <Pressable style={styles.buttonAlt} onPress={onChangeHandler}>
                            <Text style={styles.buttonAltText}>{isLogin ? 'Sign Up' : 'Log In'}</Text>
                        </Pressable>
                    </View>
                </View>
            </View>


        </KeyboardAvoidingView>
    )
}
export default LoginScreen












const styles = StyleSheet.create({
    image: {
        flex: 1,
        width: '100%',
        alignItems: 'center',
    },
    card: {
        flex: 1,
        backgroundColor: 'rgba(255, 255, 255, 0.4)',
        width: '80%',
        marginTop: '40%',
        borderRadius: 20,
        maxHeight: 380,
        paddingBottom: '30%',
    },
    heading: {
        fontSize: 30,
        fontWeight: 'bold',
        marginLeft: '10%',
        marginTop: '5%',
        marginBottom: '30%',
        color: 'black',
    },
    form: {
        flex: 1,
        justifyContent: 'space-between',
        paddingBottom: '5%',
    },
    inputs: {
        width: '100%',
        flex: 1,
        alignItems: 'center',
        justifyContent: 'center',
        paddingTop: '10%',
    },
    input: {
        width: '80%',
        borderBottomWidth: 1,
        borderBottomColor: 'black',
        paddingTop: 10,
        fontSize: 16,
        minHeight: 40,
    },
    button: {
        width: '80%',
        backgroundColor: 'black',
        height: 40,
        borderRadius: 50,
        justifyContent: 'center',
        alignItems: 'center',
        marginVertical: 5,
    },
    buttonText: {
        color: 'white',
        fontSize: 16,
        fontWeight: '400'
    },
    buttonAlt: {
        width: '80%',
        borderWidth: 1,
        height: 40,
        borderRadius: 50,
        borderColor: 'black',
        justifyContent: 'center',
        alignItems: 'center',
        marginVertical: 5,
    },
    buttonAltText: {
        color: 'black',
        fontSize: 16,
        fontWeight: '400',
    },
    message: {
        fontSize: 16,
        marginVertical: '5%',
    },
});