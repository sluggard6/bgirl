import React, {Component} from 'react';
import ScrollableTabView, {DefaultTabBar, } from 'react-native-scrollable-tab-view';
import {
  Image,
  StyleSheet
} from 'react-native';

import Main from './main'
import Channel from './channel'
import User from './user'
import BgirlTabBar from '../component/bgirl_tab_bar'
import Global from '../utils/global'


export default class FullPicView extends Component {

  constructor(props) {
		super(props);
  }

  render() {
    return (
      <Image source={{uri: this.props.pic.max}} style={styles.image}/>
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
    width: Global.size.width,
    height: Global.size.height,
    resizeMode: "contain"
  }
})
