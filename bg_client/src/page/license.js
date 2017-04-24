// @flow

import React, { Component } from 'react';

import {
  View,
  ScrollView,
  Image,
  Text,
  StyleSheet
} from 'react-native'

import Global from '../utils/global'


export default class License extends Component {


  render() {
    return(
      <View style={styles.container}>
        <Image source={require('../images/mianzebeijing.png')} style={{width: Global.size.width, height: Global.size.height, resizeMode: Image.resizeMode.contain, position: 'absolute', opacity:0.5}} />
        <ScrollView style={{backgroundColor: "transparent"}}>
          <Image source={require('../images/mianzeneirong.png')} style={{width: Global.size.width, height: 3000, resizeMode: Image.resizeMode.contain}} ></Image>
        </ScrollView>
      </View>
    )
  }

}

var styles = StyleSheet.create({

  container: {
    flex: 1,
    flexDirection: "column",
    justifyContent: 'flex-start',
    alignItems: 'center',
    width: Global.size.width,
    height: Global.size.height,
    overflow: 'hidden'
  },

})