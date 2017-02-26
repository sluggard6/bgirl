// @flow

import React, {Component} from 'react';

import {
  StyleSheet,
  View,
  Image,
  Text
} from 'react-native';

import Global from '../utils/global'
import ViewPic from './view_pic'

export default class TheTwo extends Component {

  constructor(props) {
    super(props);
    console.log(this.props.data)
  }
  render(){
    return (
      <View style={styles.list_container}>
        <Image source={uri:{this.props.data[0].pic.min}} style={styles.image}/>
        <Image source={uri:{this.props.data[1].pic.min}} style={styles.image}/>
        <Image source={uri:{this.props.data[2].pic.min}} style={styles.image}/>
      </View>
    );
  }
}

var styles = StyleSheet.create({

  container: {
    flex: 1,
    flexDirection: 'column',
    justifyContent: 'flex-start',
    flexWrap: 'nowrap',
    alignItems: 'center',
  },

  list_container: {
    flex: 1,
    flexDirection: 'row',
    justifyContent: 'space-around',
    flexWrap: 'nowrap',
    alignItems: 'center',
    width: Global.size.width
  },

  image: {
    width: (Global.size.width-5)/3,
    height: (Global.size.width-5)/3,
  }
});
