import { StyleSheet, Text, TouchableOpacity, View, ScrollView, SafeAreaView } from 'react-native'
import React, { useEffect, useState } from 'react'
import { useNavigation } from '@react-navigation/core';

import ScrollLoad from '../components/ScrollLoad';
import WeekExpirationDisplay from '../components/WeekExpirationDisplay';
import StockList from '../components/StockList';
import SwipeCardStack from '../components/SwipeCardStack';


import { useIsFocused } from '@react-navigation/native';





const HomeScreen = () => {

  const navigation = useNavigation()
  const isFocused = useIsFocused();

  useEffect(() => {
    console.log(isFocused)
  }, [isFocused]);

  return (
    <SafeAreaView style={{ flex: 1 }}>
      <View style={styles.containerMain}>
        {/* DISPLAY TIME */}
        <WeekExpirationDisplay />


        {/* SWIPING VIEW */}
        <View style={styles.cardView}>
          <SwipeCardStack />
        </View>


      </View>
    </SafeAreaView>
  )
}





const styles = StyleSheet.create(
  {
    container: {
      flex: 1,
      alignItems: 'center',
      justifyContent: 'center',
    },
    time_display: {
      flex: 1,
      backgroundColor: "black",
      justifyContent: "center",
      alignItems: "center",
    },


    cardView: {
      flex: 2,
    }



  }
)






export default HomeScreen
