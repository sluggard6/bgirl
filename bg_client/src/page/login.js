import React, { Component } from 'react';

import {
  Image,
  View,
  Text,
  TextInput,
  StyleSheet,
  TouchableOpacity
} from 'react-native';

import RegisterVcode from './register_vcode'
import Global from '../utils/global';

export default class Login extends Component{

  forgetPassword(){
  }

  register(){
    this.props.navigator.push({
      component: RegisterVcode
    })
  }

  render(){
    return (
      <View style={styles.loginContainer}>
        <View style={styles.topBar}>
          <Text sytle={{color: '#fff', fontSize: 40, borderWidth: 1, borderColor:"#fff"}}>登录</Text>
        </View>
        <View style={styles.oauthContainer}>
          <TouchableOpacity>
            <View sytle={styles.oauthBean}>
              <Image source={require('../images/sina.png')} style={styles.oauthImage}/>
              <View style={{alignItems:'center'}}>
                <Text style={styles.oauthText}>微博登录</Text>
              </View>
            </View>
          </TouchableOpacity>
          <TouchableOpacity>
            <View sytle={styles.oauthBean}>
              <Image source={require('../images/QQ.png')} style={styles.oauthImage}/>
              <View style={{alignItems:'center'}}>
                <Text style={styles.oauthText}>QQ登录</Text>
              </View>
            </View>
          </TouchableOpacity>
          <TouchableOpacity>
            <View sytle={styles.oauthBean}>
              <Image source={require('../images/weixin.png')} style={styles.oauthImage}/>
              <View style={{alignItems:'center'}}>
                <Text style={styles.oauthText}>微信登录</Text>
              </View>
            </View>
          </TouchableOpacity>
        </View>
        <View style={{alignItems:'center', padding: 20}}>
          <Text>------------   合作方账号登录   ------------</Text>
        </View>
        <TextInput
          underlineColorAndroid="transparent"
          style={styles.accountInput}
          placeholder='手机号码' />
          <View style={{height:1,backgroundColor:'#f4f4f4'}} />
        <TextInput
          underlineColorAndroid="transparent"
          secureTextEntry={true}
          style={styles.passowrdInput}
          placeholder='密码'
          password={true} />
        <View style={styles.loginButton}>
          <Text style={{color: '#fff'}} >自动登录</Text>
        </View>
        <View style={{flex:1,flexDirection:'row',alignItems: 'flex-end',justifyContent: 'space-between',bottom:20}}>
          <TouchableOpacity onPress={this.forgetPassword.bind(this)}>
            <Text style={styles.viewUnlogin}>
                 无法登录?
            </Text>
          </TouchableOpacity>
          <TouchableOpacity onPress={this.register.bind(this)}>
            <Text style={styles.viewRegister}>
                 新用户
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
    // paddingLeft:10,
    // paddingRight:10,
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
    height: 30,
    resizeMode: Image.resizeMode.contain
  },

  oauthText: {
    paddingTop: 5,
    alignItems: 'center',
    fontSize: 16,
  },

  logoImage:{
    borderRadius: 35,
    height: 90,
    width: 90,
    marginTop: 120,
    alignSelf: 'center',
  },

  accountInput:{
    backgroundColor: '#DFE0E1',
    marginTop: 20,
    height: 40,
    paddingLeft: 20,
    marginLeft: 20,
    marginRight: 20,
    marginBottom: 20,
    fontSize: 16,
    borderRadius: 5,
  },

  passowrdInput:{
    backgroundColor: '#DFE0E1',
    height: 40,
    paddingLeft: 20,
    marginLeft: 20,
    marginRight: 20,
    marginBottom: 20,
    fontSize: 16,
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
    color:'#63B8FF',
    marginLeft:10,
  },

  viewRegister:{
    fontSize:12,
    color:'#63B8FF',
    marginRight:10,
    flexDirection:'row',
    textAlign:'right',
  }
})
