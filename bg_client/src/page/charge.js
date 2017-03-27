'use strict';
import React, { Component } from 'react';

import {
  Image,
  View,
  Text,
  TextInput,
  StyleSheet,
  TouchableOpacity,
  WebView,
  ToastAndroid
} from 'react-native';

import Global from '../utils/global';
import Alipay from 'react-native-yunpeng-alipay';
import Http from '../utils/http';
import Application from '../utils/application';
import * as WeChat from 'react-native-wechat';


export default class Charge extends Component{
  alipayPage() {
    Http.httpGet(Application.getUrl(Global.urls.pageIndex),this.alipayCallback.bind(this))

  }
  alipayCallback(responseData){
    console.log(responseData.url);
    Alipay.pay(responseData.url).then(function(data){
                    console.log(data);
                }, function (err) {
                    console.log(err);
                });
  }
  wxPayPage(){
    const result = WeChat.pay({
        partnerId: 'wx11eaa73053dd1666',  // 商家向财付通申请的商家id
        prepayId: '',   // 预支付订单
        nonceStr: '',   // 随机串，防重发
        timeStamp: '',  // 时间戳，防重发
        package: '',    // 商家根据财付通文档填写的数据和签名
        sign: ''        // 商家根据微信开放平台文档对数据做的签名
      }
    );
  }

  render(){
    return (
      <View style={styles.container}>
        <View style={styles.topBar}>
          <Text style={{color: '#fff', fontSize: 20}}>登   录</Text>
        </View>
        <View >
          <View><Text >账户余额：</Text></View>
          <View style={{backgroundColor:'red'}}><Text>至尊VIP</Text></View>
          <View><Text>充值：</Text></View>
          <TouchableOpacity onPress={this.alipayPage.bind(this)}>
            <View style={{flexDirection:'row'}}>
              <Image source={require('../images/charge/money.jpg')}/>
              <Text>支付宝</Text>
            </View>
          </TouchableOpacity>
          <TouchableOpacity onPress={this.wxPayPage.bind(this)}>
            <View style={{flexDirection:'row'}}>
              <Image source={require('../images/charge/money.jpg')}/>
              <Text>微信</Text>
            </View>
          </TouchableOpacity>
          <View><Text>账户余额：</Text></View>
          <View><Text>账户余额：</Text></View>
          <View><Text>账户余额：</Text></View>
          <View style={styles.footer}><Text>充值问题，点此联系客服</Text></View>
        </View>
      </View>

    )
  }
}
var styles = StyleSheet.create({
  container: {
    flex: 1,
    flexDirection: 'column',
    backgroundColor: '#f4f4f4',
  },

  topBar: {
    justifyContent: 'center',
    alignItems: 'center',
    flexDirection: 'row',
    height: 96/Global.pr,
    width: Global.size.width,
    backgroundColor: '#313840'
  },

  footer:{
    justifyContent:'center',
    alignItems: 'center',
    height: 96/Global.pr,
    width: Global.size.width
  }

})
