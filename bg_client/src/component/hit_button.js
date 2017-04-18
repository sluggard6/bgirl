// @flow

import React, {Component} from 'react';


import {
  StyleSheet,
  View,
  Image,
  Text,
  TouchableOpacity
} from 'react-native';

import Global from '../utils/global'

export default class HitButton extends Component {

  constructor(props) {
		super(props);
    this.state={
      good: false,
      bad: false
    }
	}

  render() {
    return(
      <View style={styles.bottom}>
        <TouchableOpacity>
          <Image source={require('../images/zan.png')} style={{width: 30, height: 30, resizeMode: Image.resizeMode.contain}}/>
        </TouchableOpacity>
        <Text style={{fontSize: 18, paddingLeft: 20, paddingRight: 20}}>{this.props.pic.good}</Text>
        <TouchableOpacity>
          <Image source={require('../images/cai.png')} style={{width: 30, height: 30, resizeMode: Image.resizeMode.contain}}/>
        </TouchableOpacity>
        <Text style={{fontSize: 18, paddingLeft: 20, paddingRight: 20}}>{this.props.pic.good}</Text>
      </View>
    )
  }

}

var styles = StyleSheet.create({

  bottom: {
    flexDirection: "row",
    justifyContent: 'center',
    alignItems: 'center',
    height: (140/Global.pr), 
    // backgroundColor: "white"
  }
})