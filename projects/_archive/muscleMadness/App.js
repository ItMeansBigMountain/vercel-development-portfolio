import { StyleSheet, Text, View, Button } from 'react-native';
import React, { useEffect, useState } from 'react'

// react navigator
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';


import HomeScreen from './screens/HomeScreen';
import DetailsScreen from './screens/DetailsScreen';
import AddWorkout_Screen from './screens/AddWorkout_Screen';




// screen navigation init stack
const Stack = createNativeStackNavigator();



function App() {

  
  return (
    <NavigationContainer>

      {/* creates a stack of screens to navigate through */}
      <Stack.Navigator>

        {/* HOME SCREEN */}
        <Stack.Screen name="Home" component={HomeScreen}
        />




        {/* WORKOUT DETAILS */}
        <Stack.Screen name="Details" component={DetailsScreen}
          options={({ navigation }) => ({
            headerRight: () => (
              <Button title="testing ..." color="#000000"
                onPress={() => navigation.replace("Home")}
              />
            ),
          })}
        />





        {/* ADD WORKOUT */}
        <Stack.Screen name="ADD WORKOUT" component={AddWorkout_Screen} />




      </Stack.Navigator>

    </NavigationContainer>
  );
}






const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
  },
});
export default App;