import React, {Component} from 'react';
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

  componentWillUpdate(nextProps, nextState){
    // console.log(this.props)
    // console.log(nextProps)
    // console.log("---------------------------")
    // console.log(this.state)
    // console.log(nextState)
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
