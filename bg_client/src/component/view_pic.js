// @flow

import React, {Component} from 'react';

import {
  StyleSheet,
  View,
  Image,
  Text
} from 'react-native'

import Global from '../utils/global';

export default class ViewPic extends Component {

  constructor(props) {
    super(props);
  }

  render(){
    return (
      <View style={styles.container}>
        <Image
          style={styles.image}
          source={{uri: this.props.pic.max}}
        />
        <Text style={styles.text}>{this.props.component.name}</Text>
      </View>
    );
  }
}

var styles = StyleSheet.create({

  container: {
    flexDirection: "column",
    justifyContent: 'center',
    alignItems: 'center',
  },
  image: {
    width: (Global.size.width-20)/2,
    height: (Global.size.width-20)/3*2,
    borderWidth: 1,
    borderColor: "white"
  },
  text: {
    textAlign: 'center',
    width: (Global.size.width-20)/2-2,
    height: 30,
    backgroundColor: "red",
    fontSize: 18,
    color: "white"
  }
})
