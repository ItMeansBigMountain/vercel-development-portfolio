// Import the functions you need from the SDKs you need
import firebase from 'firebase';

// import admin_auth from "firebase-admin"
// var serviceAccount = require("./serviceAccountKey.json")
// const generate_token = admin_auth.auth()




// FIREBASE API CONFIGS 
const firebaseConfig = {
  apiKey: "",
  authDomain: "",
  projectId: "",
  storageBucket: "",
  messagingSenderId: "",
  appId: "",
  // credential: admin.credential.cert(serviceAccount)
};


// Initialize Firebase
const app = firebase.initializeApp(firebaseConfig);

// const auth = firebase.auth().signInWithCustomToken
// const auth = firebase.auth().signInAnonymously
// const auth = firebase.auth().signInWithEmailAndPassword
// const auth = firebase.auth().signInWithPhoneNumber
const auth = firebase.auth()





export {auth  };
// export {auth , generate_token};