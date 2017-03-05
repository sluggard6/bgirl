// @flow

import React, {Component} from 'react';

import {
  StyleSheet,
  View,
  Image,
  Text
} from 'react-native';

import Global from '../utils/global';

export default class ViewChannel extends Component {

  constructor(props) {
    super(props);
  }
  render(){
    return (
      <Image source={{uri:"http://test.rs.vogor.cn/image/2017/02/19/9b23d5427b6086e8.jpg"}} style={styles.container}>
        <View style={styles.text_container}>
          <Text style={styles.text_name}>{this.props.data.name}</Text>
          <Text style={styles.text_des}>{this.props.data.description}</Text>
        </View>
      </Image>
    );
  }
}

var styles = StyleSheet.create({

  container: {
    flexDirection: "column",
    justifyContent: 'center',
    alignItems: 'stretch',
    height: 400/Global.pr,
    borderWidth: 1,
    borderColor: "white",
    marginBottom:20,
  },

  text_container: {
    flexDirection: "column",
    justifyContent: 'flex-end',
    alignItems: 'center',
  },

  text_name: {
    alignItems: 'flex-end',
    fontSize: 30,
  },

  text_des: {
    alignItems: 'flex-end',
    fontSize: 18,
  }
})
