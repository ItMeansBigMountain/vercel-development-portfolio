// react modules
import { useNavigation  } from '@react-navigation/core';
import React, { useEffect, useState } from 'react'
import { KeyboardAvoidingView, StyleSheet, Text, TextInput, TouchableOpacity, View } from 'react-native'

// // DEVICE INFO
// import DeviceInfo from 'react-native-device-info';
// import { getUniqueId, getManufacturer } from 'react-native-device-info';


// firebase data base
import { auth } from "../api_config/firebase";




const LoginScreen = () => {
  // user input states
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")

  // page navigation stack
  const navigation = useNavigation()



  // on render, check if user is logged in or not
  useEffect(
    () => {
      const unsubscribe = auth.onAuthStateChanged(
        user => {
          // console.log(user)
          if (user) navigation.replace("Home")
        }
      )
      return unsubscribe;
    }, []
  )







  // submit register method()
  const handleSignUp = () => {
    auth
      // ADD USER TO DATABASE
      .createUserWithEmailAndPassword(email, password)
      // SEND EMAIL VARIFICATION
      .then(userCredentials => {
        const user = userCredentials.user;
        user.sendEmailVerification()
        
        console.log(user.email, "email - Registered!")
      })
      .catch(error => { alert(error.message) })




  }

  // submit login method()
  const handleLogin = () => {
    auth
      .signInWithEmailAndPassword(email, password)
      .then(userCredentials => {
        const user = userCredentials.user;
        console.log(user.email, "email - logged in!")
      })
      .catch(error => { alert(error.message) })

  }

  // submit guest login method()
  const handleGuestLogin = () => {
    auth
      .signInAnonymously()
      .then(userCredentials => {
        const user = userCredentials.user;
        console.log(user?.displayName, "ananymous - logged in!")
      })
      .catch(error => { alert(error.message) })
  }






  // submit Device login method()
  // const handleDeviceLogin = () => {

  //   let token = generate_token.createCustomToken("testing_token")
  //   auth
  //     .signInWithCustomToken(token)
  //     .then(userCredentials => {
  //       const user = userCredentials.user;
  //       console.log(user?.displayName, token ,  "device - logged in!")
  //     })
  //     .catch(error => { alert(error.message) })
  // }


  return (
    <KeyboardAvoidingView
      style={styles.container}
      behavior="padding"
    >

      {/* USER INPUT */}
      <View style={styles.inputContainer}>

        {/* INPUT EMAIL */}
        <TextInput
          placeholder='Email'
          value={email}
          onChangeText={text => { setEmail(text) }}
          style={styles.input}
        />

        {/* INPUT PASSWORD */}
        <TextInput
          placeholder='Password'
          value={password}
          onChangeText={text => { setPassword(text) }}
          style={styles.input}
          secureTextEntry
        />
      </View>

      {/* SUBMIT BUTTONS */}
      <View style={styles.buttonContainer}>

        {/* email login */}
        <TouchableOpacity onPress={handleLogin} style={styles.button}>
          <Text style={styles.buttonText}> Login </Text>
        </TouchableOpacity>


        {/* register new account */}
        <TouchableOpacity onPress={handleSignUp} style={[styles.button, styles.buttonOutline]}>
          <Text style={styles.buttonOutlineText}> Register </Text>
        </TouchableOpacity>

        {/* guest login */}
        <TouchableOpacity onPress={handleGuestLogin} style={[styles.button, styles.GuestbuttonOutline]}>
          <Text style={styles.GuestbuttonOutlineText}> Guest! </Text>
        </TouchableOpacity>

        {/* device login */}
        {/* <TouchableOpacity onPress={handleDeviceLogin} style={[styles.button, styles.GuestbuttonOutline]}>
          <Text style={styles.GuestbuttonOutlineText}> Device Login! </Text>
        </TouchableOpacity>*/}


      </View>



    </KeyboardAvoidingView>
  )
}
export default LoginScreen

const styles = StyleSheet.create(
  {
    container: {
      flex: 1,
      justifyContent: "center",
      alignItems: "center",

    },

    inputContainer: {
      width: "80%"
    },
    input: {
      backgroundColor: "white",
      paddingHorizontal: 15,
      paddingVertical: 10,
      borderRadius: 10,
      marginTop: 5
    },
    buttonContainer: {
      width: "60%",
      justifyContent: "center",
      alignItems: "center",
      marginTop: 40
    },
    button: {
      backgroundColor: "#0782F9",
      width: "100%",
      padding: 15,
      borderRadius: 10,
      alignItems: "center",
    },
    buttonOutline: {
      backgroundColor: "white",
      marginTop: 5,
      borderColor: "#0782F9",
      borderWidth: 2
    },
    buttonText: {
      color: "white",
      fontWeight: "700",
      fontSize: 16,
    },
    buttonOutlineText: {
      color: "#0782F9",
      fontWeight: "700",
      fontSize: 16,
    },
    GuestbuttonOutlineText: {
      color: "#00FF00",
      fontWeight: "700",
      fontSize: 16,
    },
    GuestbuttonOutline: {
      backgroundColor: "white",
      marginTop: 5,
      borderColor: "#00FF00",
      borderWidth: 2
    },

  }
)


