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
import {TextTopBar} from '../component/top_bar'

export default class Pay extends Component {

  constructor(props) {
    super(props)
    this.state = {
      alert: false
    }
  }

  // doClose() {
  //   Global.navigator.pop()
  // }

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
    this.setState({
      alert: false
    })
  }

  render(){
    return(
      <View style={styles.container}>
        <TextTopBar text={'充  值'}/>
        <View style={[styles.vipBanner,{backgroundColor:"#FBA150"}]}>
          <Text style={[styles.text,{color: 'white'}]}>包月用户可享受的权限</Text>
          <TouchableOpacity onPress={this.lock.bind(this)}>
            <Text style={[styles.text,{color: 'white', borderWidth: 1, borderColor: 'white', paddingLeft: 2}]}>¥ 39 </Text>
          </TouchableOpacity>
        </View>
        <View style={styles.vipContext}>
          <ProductInfo image={require('../images/pay_icon_1.png')} text={"全馆3000张以上美女任意看,价值299元"}/>
          <ProductInfo image={require('../images/pay_icon_2.png')} text={"每周更新100张,3位美女套图,全年不少于4000张+更新量,价值399元"}/>
          <ProductInfo image={require('../images/pay_icon_3.png')} text={"新订购用户赠送当月主推美女写真海报一份,价值129元"}/>
        </View>
        <View style={styles.vipBanner}>
          <Text style={[styles.text,{color: 'white'}]}>包年用户可享受的权限</Text>
          <TouchableOpacity onPress={this.lock.bind(this)}>
            <Text style={[styles.text,{color: 'white', borderWidth: 1, borderColor: 'white', paddingLeft: 2}]}>¥299</Text>
          </TouchableOpacity>
        </View>
        <View style={styles.vipContext}>
          <ProductInfo image={require('../images/pay_icon_1.png')} text={"全馆3000张以上美女任意看,价值299元"}/>
          <ProductInfo image={require('../images/pay_icon_2.png')} text={"每周更新100张,3位美女套图,全年不少于4000张+更新量,价值399元"}/>
          <ProductInfo image={require('../images/pay_icon_3.png')} text={"新订购用户赠送当月主推美女写真海报一份,价值129元"}/>
          <ProductInfo image={require('../images/pay_icon_4.png')} text={"美女叫床铃声定制赠送,价值29元"}/>
          <ProductInfo image={require('../images/pay_icon_5.png')} text={"每季度线下私拍包名申请资格,价值699元"}/>
          <ProductInfo image={require('../images/pay_icon_6.png')} text={"商城季节特卖会优惠券,价值169元"}/>
          <ProductInfo image={require('../images/pay_icon_7.png')} text={"美女图片下载资格"}/>
        </View>
        {this._doAlert()}
      </View>
    )
  }
}

export class ProductInfo extends Component {

  render() {
    return (
      <View style={{flexDirection: 'row', alignItems: 'center'}}>
        <Image source={this.props.image} style={{width: 25, height:25, marginLeft: 10, resizeMode: Image.resizeMode.contain}}/>
        <Text style={styles.textContext}>{this.props.text}</Text>
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
    height: 150/Global.pr,
    width: Global.size.width,
    marginTop: 10,
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
    fontSize: 22
  },

  textContext: {
    padding: 10
  }

});