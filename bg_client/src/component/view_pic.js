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
    pic = props.pic;
  }

  render(){
    return (
      <View style={styles.container}>
        <Image
          style={styles.image}
          source={{uri: pic.max}}
        />
        <Text>{pic.title}</Text>
      </View>
    );
  }
}

var styles = StyleSheet.create({

  container: {
    flexDirection: "column",
    justifyContent: 'space-around',
    alignItems: 'center',
  },
  image: {
    width: (Global.size.width-20)/2,
    height: (Global.size.width-20)/3*2,
  }
})
