// @flow

import React, {Component} from 'react';

import {
  StyleSheet,
  View,
  Image,
  Text
} from 'react-native';

import Global from '../utils/global'

export default class Banner extends Component {

  constructor(props) {
    super(props);
    console.log(this.props.data)
  }
  render(){
    return (
      <View style={styles.list_container}>
        <ViewPic pic={items[0]} />
        <ViewPic pic={items[1]} />
      </View>
    );
  }
}
