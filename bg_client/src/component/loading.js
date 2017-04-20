// @flow

import React, {Component} from 'react';

import {
  StyleSheet,
  View,
  ActivityIndicator
} from 'react-native';

export default class Loading extends Component{

  render(){
    return(
      <View style={styles.container}>
        <ActivityIndicator size="large"/>
      </View>
    )
  }

}

var styles = StyleSheet.create({

  container: {
    flex: 1,
    flexDirection: 'column',
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: 'transparent'
  },

})