import React, { Component } from 'react';

import {
  Image,
  View,
  Text,
  TextInput,
  StyleSheet,
  AsyncStorage,
  TouchableOpacity,
  ToastAndroid
} from 'react-native';

import RegisterPhone,{FindPwdPhone} from './register_phone'
import TabBarView from './tab_bar_view'
import Global from '../utils/global'
import Application from '../utils/application'
import Http from '../utils/http'
import {TextTopBar} from '../component/top_bar'

export default class Login extends Component{

  constructor(props) {
    super(props);
    this.state = {
      uname: "",
      pwd: ""
    }
  }

  componentDidMount() {
    AsyncStorage.getItem('uname').then((uname) => {
      if(uname != null) {
        AsyncStorage.getItem('pwd').then((pwd) => {
          this.setState({
            uname: uname,
            pwd: pwd
          })
        })
      }
    })
  }

  forgetPassword(){
    Global.navigator.push({
      component: FindPwdPhone
    })
  }

  register(){
    Global.navigator.push({
      component: RegisterPhone
    })
  }

  doLogin(){
    Application.login(this.state.uname, this.state.pwd, this.loginCallBack.bind(this))
  }

  loginCallBack() {
    Global.navigator.resetTo({
      component: TabBarView
    })
  }

  render(){
    return (
      <View style={styles.loginContainer}>
        <TextTopBar text={'登   录'}/>
        <View style={styles.oauthContainer}>
          <TouchableOpacity onPress={Application.unSupport}>
            <View sytle={styles.oauthBean}>
              <Image source={require('../images/sina.png')} style={styles.oauthImage}/>
              <View style={{alignItems:'center'}}>
                <Text style={styles.oauthText}>微博登录</Text>
              </View>
            </View>
          </TouchableOpacity>
          <TouchableOpacity onPress={Application.unSupport}>
            <View sytle={styles.oauthBean}>
              <Image source={require('../images/qq.png')} style={styles.oauthImage}/>
              <View style={{alignItems:'center'}}>
                <Text style={styles.oauthText}>QQ登录</Text>
              </View>
            </View>
          </TouchableOpacity>
          <TouchableOpacity onPress={Application.unSupport}>
            <View sytle={styles.oauthBean}>
              <Image source={require('../images/weixin.png')} style={styles.oauthImage}/>
              <View style={{alignItems:'center'}}>
                <Text style={styles.oauthText}>微信登录</Text>
              </View>
            </View>
          </TouchableOpacity>
        </View>
        <View style={{alignItems:'center', padding: 20, marginBottom: 20}}>
          <Text>------------   合作方账号登录   ------------</Text>
        </View>
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
            placeholder='密码'
            password={true} />
        </View>
        <TouchableOpacity onPress={this.doLogin.bind(this)}>
          <View style={styles.loginButton}>
            <Text style={{color: '#fff', fontSize: 15}} >自动登录</Text>
          </View>
        </TouchableOpacity>
        <View style={{flexDirection:'row',justifyContent: 'space-around', marginTop: 20}}>
          <TouchableOpacity onPress={this.forgetPassword.bind(this)}>
            <Text style={styles.viewUnlogin}>
                 无法登录?
            </Text>
          </TouchableOpacity>
          <TouchableOpacity onPress={this.register.bind(this)}>
            <Text style={styles.viewRegister}>
                 注册账号
            </Text>
          </TouchableOpacity>
        </View>
      </View>
    )
  }
}

var styles = StyleSheet.create({
  loginContainer: {
    flex: 1,
    flexDirection: 'column',
    backgroundColor: '#f4f4f4',
  },

  topBar: {
    justifyContent: 'center',
    alignItems: 'center',
    height: 200/Global.pr,
    width: Global.size.width,
    backgroundColor: '#313840'
  },

  topBarText: {
    alignItems: 'center',
    color: '#fff',
  },

  oauthContainer: {
    height: 80,
    flexDirection: 'row',
    justifyContent: 'space-around',
    alignItems: 'center',
    marginTop: 25,
  },

  oauthBean: {
    flexDirection: 'column',
    justifyContent: 'center',
    alignItems: 'center',
  },

  oauthImage: {
    height: 25,
    resizeMode: Image.resizeMode.contain
  },

  oauthText: {
    paddingTop: 5,
    alignItems: 'center',
    fontSize: 14,
  },

  logoImage: {
    borderRadius: 35,
    height: 90,
    width: 90,
    marginTop: 120,
    alignSelf: 'center',
  },

  inputLogo: {
    height: 25,
    marginLeft: 10,
    resizeMode: Image.resizeMode.contain
  },

  inputContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    marginLeft: 20,
    marginRight: 20,
    marginBottom: 20,
    backgroundColor: '#DFE0E1',
    borderRadius: 5,
    height:40
  },

  input:{
    backgroundColor: 'transparent',
    height: 40,
    width: Global.size.width - 80,
    paddingLeft: 10,
    fontSize: 14,
    borderRadius: 5,
  },

  loginButton:{
    marginLeft: 20,
    marginRight: 20,
    backgroundColor: '#FC4A68',
    height: 35,
    borderRadius: 5,
    justifyContent: 'center',
    alignItems: 'center',
  },

  viewUnlogin:{
    fontSize:12,
    marginLeft:10,
  },

  viewRegister:{
    fontSize:12,
    marginRight:10,
    flexDirection:'row',
    textAlign:'right',
  }
})
