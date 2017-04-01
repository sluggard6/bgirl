// @flow

import React, {Component} from 'react';

import {
  View,
  Text,
  Image,
  TouchableOpacity,
  StyleSheet
} from 'react-native'

import Global from '../utils/global'
import Application from '../utils/application'
import AlertWinow from '../component/windows'

export default class Pay extends Component {

  constructor(props) {
    super(props)
    this.state = {
      alert: false
    }
  }

  doClose() {
    Global.navigator.pop()
  }

  _doAlert() {
    if(this.state.alert) {
      return (<AlertWinow unLock={this.unLock.bind(this)} charge={true}/>)
    }
    return
  }

  lock() {
    this.setState({
      alert: true
    })
  }

  unLock() {
    // this.setState({
    //   alert: false
    // })
    this.state.alert = false
    this.doClose()
  }

  render(){
    return(
      <View style={styles.container}>
        {this._doAlert()}
        <View style={styles.topBar}>
          <Text style={{color: '#fff', fontSize: 20}}>充值</Text>
        </View>
        <View style={styles.balanceBanner}>
          <Text style={styles.text}>账户余额:</Text>
          <View style={{flexDirection: 'row', alignItems: 'center'}}>
            <Image source={require('../images/jinbi.png')} style={{width: 18, height:18, borderWidth: 1, marginLeft: 10, marginRight: 5, resizeMode: Image.resizeMode.contain}}/>
            <Text style={styles.text}>0昧币</Text>
          </View>
        </View>
        <View style={styles.vipBanner}>
          <Text style={[styles.text,{color: 'white'}]}>至尊VIP</Text>
          <Text style={[styles.text,{color: 'white'}]}>享受365天</Text>
          <TouchableOpacity onPress={this.doClose.bind(this)}>
            <Text style={[styles.text,{color: 'white'}]}>点击关闭</Text>
          </TouchableOpacity>
          <TouchableOpacity onPress={this.lock.bind(this)}>
            <Text style={[styles.text,{color: 'white', borderWidth: 1, borderColor: 'white', paddingLeft: 2}]}>¥199</Text>
          </TouchableOpacity>
        </View>
        <View style={styles.vipContext}>
          <Text style={[styles.text,styles.textContext]}>可享受权限</Text>
          <View style={{flexDirection: 'row', alignItems: 'center'}}>
            <Image source={require('../images/xiala1.png')} style={{width: 18, height:18, marginLeft: 10, resizeMode: Image.resizeMode.contain}}/>
            <Text style={[styles.text,styles.textContext]}>订阅有效期内的每期高清图片</Text>
          </View>
          <View style={{flexDirection: 'row', alignItems: 'center'}}>
            <Image source={require('../images/xiala2.png')} style={{width: 18, height:18, marginLeft: 10, resizeMode: Image.resizeMode.contain}}/>
            <Text style={[styles.text,styles.textContext]}>VIP高清视频任意看</Text>
          </View>
          <View style={{flexDirection: 'row', alignItems: 'center'}}>
            <Image source={require('../images/xiala3.png')} style={{width: 18, height:18, marginLeft: 10, resizeMode: Image.resizeMode.contain}}/>
            <Text style={[styles.text,styles.textContext]}>不定期发布的典藏特刊</Text>
          </View>
          <View style={{flexDirection: 'row', alignItems: 'center'}}>
            <Image source={require('../images/xiala4.png')} style={{width: 18, height:18, marginLeft: 10, resizeMode: Image.resizeMode.contain}}/>
            <Text style={[styles.text,styles.textContext]}>优先申请参加线上活动</Text>
          </View>
        </View>
      </View>
    )
  }
}

var styles = StyleSheet.create({

  container: {
    flex: 1,
    flexDirection: 'column',
    justifyContent: 'flex-start',
    // flexWrap: 'nowrap',
    alignItems: 'center',
    // backgroundColor: 'transparent'
    // backgroundColor: '#DFE0E1'
  },

  topBar: {
    justifyContent: 'center',
    alignItems: 'center',
    height: 200/Global.pr,
    width: Global.size.width,
    backgroundColor: '#313840'
  },

  balanceBanner: {
    justifyContent: 'flex-start',
    alignItems: 'center',
    flexDirection: 'row',
    height: 200/Global.pr,
    width: Global.size.width,
    paddingLeft: 20,
    backgroundColor: 'white'
  },

  vipBanner: {
    justifyContent: 'space-between',
    alignItems: 'center',
    flexDirection: 'row',
    height: 200/Global.pr,
    width: Global.size.width,
    paddingLeft: 20,
    paddingRight: 20,
    backgroundColor: '#ff4563'
  },

  vipContext: {
    flexDirection: 'column',
    justifyContent: 'flex-start',
    width: Global.size.width,
    paddingTop: 10,
    backgroundColor: 'white'
  },

  text: {
    fontSize: 18
  },

  textContext: {
    padding: 10
  }

});