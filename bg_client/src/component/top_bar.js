import React, { Component } from 'react';
import {
    StyleSheet,
    View,
    Image,
    Text
} from 'react-native';

import Global from '../utils/global';

export default class TopBar extends Component {

  render(){
    return(
      <View style={styles.top_bar}>
        <Image style={styles.tob_bar_logo} source={require('../images/logo.png')}/>
      </View>
    );
  }
}

export class TextTopBar extends Component {
  render(){
    return(
      <View style={styles.top_bar}>
        <Text style={{color: '#fff', fontSize: 18}}>{this.props.text}</Text>
      </View>
    );
  }
}

var styles = StyleSheet.create({

  top_bar: {
    flexWrap: 'nowrap',
    justifyContent: 'center',
    alignItems: 'center',
    height: 50,
    width: Global.size.width,
    backgroundColor: "#333740"
  },

  tob_bar_logo: {
    height: 40,
    width: 40,
    resizeMode: 'contain',
  }

});
