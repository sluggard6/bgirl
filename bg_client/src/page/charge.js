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



export default class Charge extends Component{
  alipayPage() {
    Alipay.pay('https://www.alipay.com/cooperate/gateway.do?body=%E6%98%A7%E6%98%A7%E5%85%85%E5%80%BC&seller_id=2088412076973614&service=create_direct_pay_by_user&_input_charset=utf-8&notify_url=http%3A//192.168.1.105/pay/notify/alipay&payment_type=1&total_fee=0.01&partner=2088412076973614&out_trade_no=11&return_url=http%3A//192.168.1.105/pay/11/callback&subject=%E6%94%AF%E4%BB%98%E5%AE%9D%E5%85%85%E5%80%BC&sign=585a64423d488e151cbaf292fa7da659&sign_type=MD5').then(function(data){
                    console.log(data);
                }, function (err) {
                    console.log(err);
                });
  }
  wxPayPage(){

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
          <View style={styles.topBar}>
        <WebView
          style={{width:500,height:400,backgroundColor:'gray'}}
          source={{uri:'http://www.baidu.com',method: 'GET'}}
          javaScriptEnabled={true}
          domStorageEnabled={true}
          scalesPageToFit={false}
          />
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
