// @flow

import React, {Component} from 'react';

import {
  StyleSheet,
  View,
  Image,
  Text
} from 'react-native';

export default class ViewChannel extends Component {

  constructor(props) {
    super(props);
  }
  render(){
    return (
      <Image source={require('../images/min.jpg')}>
        <Text>{this.props.data.title}</Text>
      </Image>
    );
  }
}

var styles = StyleSheet.create({

  container: {
    flex: 1,
    flexDirection: "column",
    justifyContent: 'space-around',
    alignItems: 'center',
    padding: 5,
  }
})
