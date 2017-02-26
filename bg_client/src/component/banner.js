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
      <Image source={{uri:"http://rs.vogor.cn/image/2017/02/19/9b23d5427b6086e8.jpg"}} style={styles.container}>
        <View style={styles.text_container}>
          <Text style={styles.text_name}>{this.props.data[0].des}</Text>
        </View>
      </Image>
    );
  }
}

var styles = StyleSheet.create({

  container: {
    flexDirection: "column",
    justifyContent: 'flex-end',
    alignItems: 'stretch',
    height: 255,
    width: Global.size.width,
    borderWidth: 1,
    borderColor: "white",
    marginBottom:10,
  },

  text_container: {
    flexDirection: "row",
    justifyContent: 'flex-end',
    alignItems: 'center',
    paddingRight: 10,
    height: 60,
    borderWidth: 1,
    opacity:0.5,
    backgroundColor:'#AEAEAF',
    borderColor: "black"
  },

  text_name: {
    alignItems: 'flex-end',
    color: 'white',
    fontSize: 22,
  },

  text_des: {
    alignItems: 'flex-end',
    fontSize: 18,
  }
})
