// @flow

import React, {Component} from 'react';

import {
  StyleSheet,
  View,
  Image,
  Text,
  TextInput,
  TouchableOpacity,
  TouchableWithoutFeedback
} from 'react-native';
import Global from '../utils/global'
import Application from '../utils/application'
import RegisterPhone from '../page/register_phone'
import Alipay from 'react-native-yunpeng-alipay'
import * as WeChat from 'react-native-wechat'
import Http from '../utils/http'
import ChannelPackage from '../utils/channel_info'
import Download from '../page/download'

export default class AlertWindow extends Component {

  constructor(props) {
    super(props)
    this.state={
      charge: false,
      productId: 0,
    }
  }

  cannel(){
    this.state.charge = false
    this.props.unLock()
  }

  alertPay(productId){
    this.setState({
      charge: true,
      productId: productId
    })
  }

  getWindows() {
    if(Global.isLogin) {
      if(this.props.end) {
        return (
          <DownloadWindow cannel={this.cannel.bind(this)}/>
        )
      }else if(this.state.charge){
        return (
          <ChargeWindow productId={this.state.productId}/>
        )
      }else{
        return(
          <BuyWindow alertPay={this.alertPay.bind(this)}/>
        )
      }    
    }else{
      return(
        <LoginWindow cannel={this.cannel.bind(this)}/>
      )
    }
  }

  render(){
    return(
      <TouchableWithoutFeedback onPress={this.cannel.bind(this)}>
        <View style={styles.container}>
          <View style={styles.view_opacity}/>
          {
            this.getWindows()
          }
        </View>
      </TouchableWithoutFeedback>
    )
  }

}

export class DownloadWindow extends Component {

  goDownload(){
    this.props.cannel()
    Global.navigator.push({
      component: Download
    })
  }

  render(){
    return(
      <View style={styles.window}>
        <Image source={require('../images/renwu.png')} style={styles.renwu}/>
        <View style={[styles.button_container,{height: 200, paddingTop: 10}]}>
          <Text style={{fontSize: 16, marginTop: 20}}>可以直接把妹妹带回家呦!</Text>
          <Text style={{fontSize: 10, color: '#FDA25D', margin: 10}}>进入微信,关注"i昧昧的御花园"公众号,留言[下载]</Text>
          <TouchableOpacity onPress={this.goDownload.bind(this)}>
            <View style={styles.payButton}>
              <Text style={styles.text} >联系客服</Text>
            </View>
          </TouchableOpacity>
          <TouchableOpacity onPress={this.props.cannel}>
            <View style={styles.cannelButton}>
              <Text style={styles.text} >再看看</Text>
            </View>
          </TouchableOpacity>
        </View>
      </View>
    )
  }
}

export class ChargeWindow extends Component {

  alipayPage(productId, amount) {
    Http.httpGet(Application.getUrl(Global.urls.charge)+"?pay_type=alipay_app&channel="+ChannelPackage.CHANNEL,this.alipayCallback.bind(this))

  }

  alipayCallback(responseData){
    Alipay.pay(responseData.url).then(
      function(data){
        console.log(data)
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
    return(
      <View style={styles.window}>
        <Image source={require('../images/renwu.png')} style={styles.renwu}/>
        <View style={styles.button_container}>
          <TouchableOpacity onPress={this.wxPayPage.bind(this)}>
            <View style={[styles.chargeButton,{backgroundColor: '#FB4867'}]}>
              <Image source={require('../images/charge/weixin.png')} style={styles.chargeLogo}/>
              <Text style={styles.text} >微信支付</Text>
            </View>
          </TouchableOpacity>
          <TouchableOpacity onPress={() => this.alipayPage(this.props.productId, Application.getPrice(this.props.productId))}>
            <View style={[styles.chargeButton,{backgroundColor: '#FCA150'}]}>
              <Image source={require('../images/charge/zhifubao.png')} style={styles.chargeLogo}/>
              <Text style={styles.text} >支付宝支付</Text>
            </View>
          </TouchableOpacity>
          <TouchableOpacity onPress={this.props.cannel}>
            <View style={styles.cannelButton}>
              <Text style={styles.text} >再看看</Text>
            </View>
          </TouchableOpacity>
        </View>
      </View>
    )
  }
}

export class BuyWindow extends Component {

  render(){
    return(
      <View style={styles.window}>
        <Image source={require('../images/renwu.png')} style={styles.renwu}/>
        <View style={styles.button_container}>
          <TouchableOpacity onPress={() => this.props.alertPay(2)}>
            <View style={styles.payButton}>
              <Text style={styles.text} >包场一年</Text>
            </View>
          </TouchableOpacity>
          <TouchableOpacity onPress={() => this.props.alertPay(1)}>
            <View style={[styles.payButton,{backgroundColor: '#FDA04F'}]}>
              <Text style={styles.text} >包场一月</Text>
            </View>
          </TouchableOpacity>
          <TouchableOpacity onPress={this.props.cannel}>
            <View style={styles.cannelButton}>
              <Text style={styles.text} >银子不够</Text>
            </View>
          </TouchableOpacity>
        </View>
      </View>
    )
  }

}

export class LoginWindow extends Component {

  constructor(props) {
    super(props)
    this.state={
      uname:"",
      pwd:""
    }
  }


  forgetPassword(){
  }

  register(){
    Global.navigator.push({
      component: RegisterPhone
    })
  }

  goCharge(){
    Global.navigator.push({
      component: Charge
    })
  }



  doLogin() {
    Application.login(this.state.uname, this.state.pwd, this.props.cannel)
  }

  render(){
    let unlogin="<忘记密码"
    let register="注册账号>"
    return(
      <View style={styles.window}>
        <Image source={require('../images/renwu.png')} style={styles.renwu}/>
        <View style={[styles.button_container,{height: 230, paddingTop: 10}]}>
          <View style={styles.inputContainer}>
            <Image source={require('../images/shouji.png')} style={styles.inputLogo}/>
            <TextInput
              onChangeText={(uname) => {
                this.state.uname = uname
              }}
              underlineColorAndroid="transparent"
              style={styles.input}
              placeholder='手机号码' />
              <View style={{height:1,backgroundColor:'#f4f4f4'}} />
          </View>
          <View style={styles.inputContainer}>
            <Image source={require('../images/mima.png')} style={styles.inputLogo}/>
            <TextInput
              onChangeText={(pwd) => {
                this.state.pwd = pwd
              }}
              underlineColorAndroid="transparent"
              secureTextEntry={true}
              style={styles.input}
              placeholder='密码 5-20位数字或字母'
              password={true} />
          </View>
          <TouchableOpacity onPress={this.doLogin.bind(this)}>
            <View style={styles.loginButton}>
              <Text style={styles.text} >登录</Text>
            </View>
          </TouchableOpacity>
          <View style={{flexDirection:'row',justifyContent: 'space-around', marginTop: 20, width: 280}}>
            <TouchableOpacity>
              <Text style={styles.viewUnlogin}>
                  {unlogin}
              </Text>
            </TouchableOpacity>
            <TouchableOpacity onPress={this.register.bind(this)}>
              <Text style={styles.viewRegister}>
                  {register}
              </Text>
            </TouchableOpacity>
          </View>
          <View style={styles.oauthContainer}>
            <TouchableOpacity onPress={Application.unSupport}>
              <Image source={require('../images/sina.png')} style={styles.oauthImage}/>
            </TouchableOpacity>
            <TouchableOpacity onPress={Application.unSupport}>
              <Image source={require('../images/qq.png')} style={styles.oauthImage}/>
            </TouchableOpacity>
            <TouchableOpacity onPress={Application.unSupport}>
              <Image source={require('../images/weixin.png')} style={styles.oauthImage}/>
            </TouchableOpacity>
          </View>
        </View>
      </View>
    )
  }
}

var styles = StyleSheet.create({
  container: {
    flex: 1,
    position: 'absolute',
    alignItems: 'center',
    width: Global.size.width, 
    height: Global.size.height,
    backgroundColor: "transparent"
  },

  view_opacity: {
    width: Global.size.width,
    height: Global.size.height,
    opacity:0.8,
    backgroundColor:'black',
  },

  window:{
    position: 'absolute',
    flexDirection: 'column',
    marginTop: 30,
    alignItems: 'center',
    justifyContent: 'center',
    borderRadius: 5,
    width: 250,
    height: 500, 
    backgroundColor: "transparent"
  },

  renwu: {
    width: 250, 
    height: 150, 
    resizeMode: Image.resizeMode.contain
  },

  button_container: {
    width: 250, 
    height: 150, 
    backgroundColor: "white", 
    borderRadius: 5, 
    alignItems: "center", 
    borderTopWidth: 1, 
    borderColor: "red"
  },

  oauthContainer: {
    height: 60,
    flexDirection: 'row',
    justifyContent: 'space-around',
    alignItems: 'center',
  },

  oauthImage: {
    height: 30,
    resizeMode: Image.resizeMode.contain
  },

  inputLogo: {
    height: 25,
    width: 25,
    marginLeft: 10,
    resizeMode: Image.resizeMode.contain
  },

  inputContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    marginLeft: 5,
    marginRight: 5,
    marginBottom: 5,
    backgroundColor: '#DFE0E1',
    borderRadius: 5,
    height:35
  },

  input:{
    backgroundColor: "transparent",
    height: 35,
    width: 200,
    paddingLeft: 10,
    fontSize: 12,
    borderRadius: 5,
  },

  loginButton:{
    marginLeft: 10,
    marginRight: 10,
    backgroundColor: '#FC4A68',
    height: 35,
    width: 235,
    borderRadius: 5,
    justifyContent: 'center',
    alignItems: 'center',
  },

  payButton:{
    marginLeft: 10,
    marginRight: 10,
    marginTop: 10,
    backgroundColor: '#FC4A68',
    height: 35,
    width: 235,
    borderRadius: 5,
    justifyContent: 'center',
    alignItems: 'center',
  },

  chargeButton: {
    marginLeft: 10,
    marginRight: 10,
    marginTop: 10,
    backgroundColor: '#FC4A68',
    height: 35,
    width: 235,
    borderRadius: 5,
    flexDirection: 'row',
    justifyContent: 'center',
    alignItems: 'center',
  },

  chargeLogo: {
    height: 25,
    width: 25,
    resizeMode: Image.resizeMode.contain
  },

  cannelButton:{
    marginLeft: 10,
    marginRight: 10,
    marginTop: 10,
    backgroundColor: '#C3C3C3',
    height: 40,
    width: 235,
    borderRadius: 5,
    justifyContent: 'center',
    alignItems: 'center',
  },

  viewUnlogin:{
    fontSize:14,
  },

  viewRegister:{
    fontSize:14,
    flexDirection:'row',
    textAlign:'right',
  },

  text:{
    color: "white",
    fontSize: 16
  }
})
