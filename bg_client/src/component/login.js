// @flow

import React, {Component} from 'react';

import {
  StyleSheet,
  View,
  Image,
  Text,
  TouchableOpacity
} from 'react-native';

export default class LoginWindow extends Component {

  constructor(props) {
    super(props)
  }

  render(){
    return(
      <View style={styles.window}>
        <Text style={{alignItems: 'center', fontSize: 20, color: "red"}}>我是弹窗啦啦啦</Text>
      </View>
    )
  }
}

var styles = StyleSheet.create({
  window:{
    position: 'absolute',
    marginTop: 150,
    alignItems: 'center',
    zIndex: 99,
    borderWidth: 1,
    width: 300,
    height: 400
  }
})
