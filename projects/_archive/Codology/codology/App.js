import React from 'react';
import { Button } from 'react-native';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';

import HomeScreen from './screens/HomeScreen';
import HighScoreScreen from './screens/HighScoreScreen';

const Stack = createNativeStackNavigator();

function App() {
  return (
    <NavigationContainer>
      <Stack.Navigator initialRouteName="Home">
        <Stack.Screen
          name="Home"
          component={HomeScreen}
          options={({ navigation }) => ({
            title: 'Codology',
            headerStyle: { backgroundColor: 'darkslateblue' },
            headerTintColor: '#ffffff',
            headerRight: () => (
              <Button
                title="Leaderboard"
                color="#ffffff"
                onPress={() => navigation.navigate('HighScores')}
              />
            ),
          })}
        />
        <Stack.Screen
          name="HighScores"
          component={HighScoreScreen}
          options={{
            title: 'Leaderboard',
            headerStyle: { backgroundColor: 'darkslateblue' },
            headerTintColor: '#ffffff',
          }}
        />
      </Stack.Navigator>
    </NavigationContainer>
  );
}

export default App;
