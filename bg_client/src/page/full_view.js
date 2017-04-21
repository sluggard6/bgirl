import React, {Component} from 'react';
import {
  Text,
  View,
  Image,
  StyleSheet
} from 'react-native';

import Main from './main'
import Channel from './channel'
import User from './user'
import BgirlTabBar from '../component/bgirl_tab_bar'
import Global from '../utils/global'
import AlertWinow from '../component/windows'
import HitButton from '../component/hit_button'




export default class FullPicView extends Component {

  constructor(props) {
		super(props);
  }

  _doAlert() {
    if(this.props.alert) {
      return (<AlertWinow unLock={this.props.cannel}/>)
    }
    return
  }

  render() {
    return (
      <View style={styles.container}>
        <Image source={{uri: this.props.pic.max}} style={styles.image}/>
        <HitButton
          pic={this.props.pic}
          doAlert={this.props.doAlert}
        />
        {this._doAlert()}
      </View>
    );
  }

}

var styles = StyleSheet.create({

  container: {
    flex: 1,
    flexDirection: "column",
    justifyContent: 'center',
    alignItems: 'center',
    width: Global.size.width,
    height: Global.size.height-(280/Global.pr),
    overflow: 'hidden'
  },
  image: {
    width: Global.size.width - 6,
    height: Global.size.height-(400/Global.pr),
    resizeMode: Image.resizeMode.contain
  },
})
