import React, { Component } from 'react';
import {
    StyleSheet,
    View,
    Image,
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

var styles = StyleSheet.create({

  top_bar: {
    flexWrap: 'nowrap',
    justifyContent: 'center',
    alignItems: 'center',
    height: 200/Global.pr,
    width: Global.size.width,
    backgroundColor: "#333740"
  },

  tob_bar_logo: {
    height: 150/Global.pr,
    width: 150/Global.pr,
    resizeMode: 'contain',
  }

});
