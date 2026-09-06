import React, { useEffect, useState } from 'react';
import { StyleSheet, Text, View, Dimensions, Image, Animated, PanResponder } from 'react-native';
import { useNavigation } from '@react-navigation/core';
import { useIsFocused } from '@react-navigation/native';
import { fetch_rendered_data } from '../api_config/DataServer';

import { auth } from "../api_config/firebase";




const SCREEN_HEIGHT = Dimensions.get('window').height
const SCREEN_WIDTH = Dimensions.get('window').width
const CONFIG = require("../api_config/config.json")
const quantity_rendered = CONFIG.qty_rendered



// const Content = [
//   { id: "1", uri: require('../assets/genius_1.jpg') },
//   { id: "2", uri: require('../assets/genius_2.png') },
//   { id: "3", uri: require('../assets/genius_3.jpg') },
//   { id: "4", uri: require('../assets/genius_4.png') },
//   { id: "5", uri: require('../assets/genius_5.jpg') },
//   { id: "6", uri: require('../assets/genius_7.jpg') },
//   { id: "7", uri: require('../assets/genius_8.jpg') },
//   { id: "8", uri: require('../assets/genius_9.jpg') },
//   { id: "9", uri: require('../assets/genius_10.jpg') },
//   { id: "10", uri: require('../assets/genius_11.jpg') },
// ]



export default class SwipeCardStack extends React.Component {

  constructor() {
    super()

    this.position = new Animated.ValueXY()
    this.state = {
      currentIndex: 0,
      render_index: 0,
      loadingMore: false,
      search: "",
      all_stocks: [],
      data: [],
      display_images: [],
      // display_date_ticker: '',
      // display_date_voteCard: '',
    }

    this.rotate = this.position.x.interpolate({
      inputRange: [-SCREEN_WIDTH / 2, 0, SCREEN_WIDTH / 2],
      outputRange: ['-30deg', '0deg', '10deg'],
      extrapolate: 'clamp'
    })

    this.rotateAndTranslate = {
      transform: [{
        rotate: this.rotate
      },
      ...this.position.getTranslateTransform()
      ]
    }

    this.likeOpacity = this.position.x.interpolate({
      inputRange: [-SCREEN_WIDTH / 2, 0, SCREEN_WIDTH / 2],
      outputRange: [0, 0, 1],
      extrapolate: 'clamp'
    })
    this.dislikeOpacity = this.position.x.interpolate({
      inputRange: [-SCREEN_WIDTH / 2, 0, SCREEN_WIDTH / 2],
      outputRange: [1, 0, 0],
      extrapolate: 'clamp'
    })

    this.nextCardOpacity = this.position.x.interpolate({
      inputRange: [-SCREEN_WIDTH / 2, 0, SCREEN_WIDTH / 2],
      outputRange: [1, 0, 1],
      extrapolate: 'clamp'
    })
    this.nextCardScale = this.position.x.interpolate({
      inputRange: [-SCREEN_WIDTH / 2, 0, SCREEN_WIDTH / 2],
      outputRange: [1, 0.8, 1],
      extrapolate: 'clamp'
    })

  }



  // populate content data
  Content = () => {
    let arr = []
    for (var i = 0; i < this.state.data.length; i++) {
      let t = this.state.data[i].ticker

      fetch(`${CONFIG.base_url}/api/tickers/${this.state.data[i].ticker}/meme`)
        .then((response) => response.json())
        .then((json) => {
          this.setState({
            display_images: [...this.state.display_images, { id: this.state.display_images.length, uri: json, ticker: t }]
          })
          // console.log(this.state.data[i])
          // console.log(this.state.display_images[i])
          // console.log(this.state.data)
        })
        .catch((error) => console.error(error))


      // TODO : get content array filled with images that will correlate to this.state.data[i]
      // console.log( this.state.data[i].name)
    }
  }


  // fetch stock market data
  build_data = () => {
    fetch(`${CONFIG.base_url}/api/build_internal`)
      .then((response) => response.json())
      .then((json) => { this.state.all_stocks.push(json) })
      .catch((error) => console.error(error))
  }
  updateData = async () => {
    let count = this.state.render_index
    this.setState({ render_index: count + quantity_rendered })
    // gets data from server.js
    const response = await fetch_rendered_data(quantity_rendered, this.render_index)
    // check if we got data from DataServer.js

    if (response) this.setState({ data: [...response] })
    else setData(["error", "DataServer.js", "didnt return the promise"])
  };



  // handle voting methods
  vote = async (ticker, opinion) => {
    if (auth.currentUser.emailVerified == false) return alert("Vote doesn't count until you verify email!")
    let response = await fetch(`${CONFIG.base_url}/api/votes/${ticker}/${opinion}`, {
      method: 'POST',
      headers: { Accept: 'application/json', 'Content-Type': 'application/json' },
      body: JSON.stringify({ user: auth.currentUser }),
    });

    let json = await response.json();
    // this.ticker_info(ticker)
    // this.voteCard_info(ticker)
    return json;
  }

  ticker_info = (ticker) => {
    fetch(`${CONFIG.base_url}/api/tickers/${ticker}`)
      .then((response) => response.json())
      .then((json) => setDisplay_data_ticker(json))
      .catch((error) => console.error(error))
  }

  voteCard_info = (ticker) => {
    fetch(`${CONFIG.base_url}/api/votes/${ticker}`)
      .then((response) => response.json())
      .then((json) => setDisplay_data_voteCard(json))
      .catch((error) => console.error(error))
  }






  // REACT CLASS COMPONENT FUNCTIONS
  componentDidMount() {
    // console.log("useEffect???")
    // this.build_data()
    // this.updateData()

  }

  UNSAFE_componentWillMount() {
    this.PanResponder = PanResponder.create({

      onStartShouldSetPanResponder: (evt, gestureState) => true,
      onPanResponderMove: (evt, gestureState) => {

        this.position.setValue({ x: gestureState.dx, y: gestureState.dy })
      },
      onPanResponderRelease: (evt, gestureState) => {

        // LIKE
        if (gestureState.dx > 120) {
          Animated.spring(this.position, {
            toValue: { x: SCREEN_WIDTH + 100, y: gestureState.dy },
            useNativeDriver: true
          }).start(() => {
            //VOTE FUNCTION
            let t = this.state.display_images[this.state.currentIndex].ticker
            this.vote(t, "up")
            //VOTE FUNCTION
            this.setState({ currentIndex: this.state.currentIndex + 1 }, () => {
              this.position.setValue({ x: 0, y: 0 })
            })

          })
        }

        // DISLIKE
        else if (gestureState.dx < -120) {
          Animated.spring(this.position, {
            toValue: { x: -SCREEN_WIDTH - 100, y: gestureState.dy },
            useNativeDriver: true
          }).start(() => {
            //VOTE FUNCTION
            let t = this.state.display_images[this.state.currentIndex].ticker
            this.vote(t, "down")

            this.setState({ currentIndex: this.state.currentIndex + 1 }, () => {
              this.position.setValue({ x: 0, y: 0 })
            })
          })
        }

        // in place movement
        else {
          Animated.spring(this.position, {
            toValue: { x: 0, y: 0 },
            friction: 4,
            useNativeDriver: true
          }).start()
        }
      }
    })

    this.build_data()
    this.updateData()
  }

  renderContent = () => {
    if (this.state.display_images.length == 0) this.Content()
    return this.state.display_images.map((item, i) => {
      const ticker_displayJSON = this.state.data[i]
      // console.log(this.state.display_images)
      // console.log("----------------------")

      if (i < this.state.currentIndex) {
        // use states to become ticker_info & voteCard_info returns and return them here
        return <Text>DISPLAY this.state.data[] API STATS </Text>
      }
      // top card
      else if (i == this.state.currentIndex) {

        return (
          <Animated.View
            {...this.PanResponder.panHandlers}
            key={i} style={[this.rotateAndTranslate, { height: SCREEN_HEIGHT - 120, width: SCREEN_WIDTH, padding: 10, position: 'absolute' }]}>
            <Animated.View style={{ opacity: this.likeOpacity, transform: [{ rotate: '-30deg' }], position: 'absolute', top: 50, left: 40, zIndex: 1000 }}>
              <Text style={{ borderWidth: 1, borderColor: 'green', color: 'green', fontSize: 32, fontWeight: '800', padding: 10 }}>LIKE</Text>

            </Animated.View>

            <Animated.View style={{ opacity: this.dislikeOpacity, transform: [{ rotate: '30deg' }], position: 'absolute', top: 50, right: 40, zIndex: 1000 }}>
              <Text style={{ borderWidth: 1, borderColor: 'red', color: 'red', fontSize: 32, fontWeight: '800', padding: 10 }}>NOPE</Text>

            </Animated.View>

            <Image
              style={{ flex: 1, height: null, width: null, resizeMode: 'cover', borderRadius: 20 }}
              source={{ uri: item.uri }} />


          </Animated.View>
        )
      }
      // the rest
      else {
        return (
          <Animated.View

            key={i} style={[{
              opacity: this.nextCardOpacity,
              transform: [{ scale: this.nextCardScale }],
              height: SCREEN_HEIGHT - 120, width: SCREEN_WIDTH, padding: 10, position: 'absolute'
            }]}>
            <Animated.View style={{ opacity: 0, transform: [{ rotate: '-30deg' }], position: 'absolute', top: 50, left: 40, zIndex: 1000 }}>
              <Text style={{ borderWidth: 1, borderColor: 'green', color: 'green', fontSize: 32, fontWeight: '800', padding: 10 }}>LIKE</Text>

            </Animated.View>

            <Animated.View style={{ opacity: 0, transform: [{ rotate: '30deg' }], position: 'absolute', top: 50, right: 40, zIndex: 1000 }}>
              <Text style={{ borderWidth: 1, borderColor: 'red', color: 'red', fontSize: 32, fontWeight: '800', padding: 10 }}>NOPE</Text>

            </Animated.View>

            <Image
              style={{ flex: 1, height: null, width: null, resizeMode: 'cover', borderRadius: 20 }}
              source={{ uri: item.uri }} />

          </Animated.View>
        )
      }
    }).reverse()
  }

  render() {
    return (
      <View style={{ flex: 1 }}>
        <View style={{ height: 60 }}>

        </View>
        <View style={{ flex: 1 }}>
          {this.renderContent()}
        </View>
        <View style={{ height: 60 }}>

        </View>


      </View>

    );
  }
}