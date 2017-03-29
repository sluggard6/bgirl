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
import Charge from '../page/charge'

export default class AlertWindow extends Component {


  cannel(){
    Application.cannel()
    this.props.unLock()
  }

  render(){
    console.log("--------------Alert Window------------------")
    if(Global.isLogin) {
      return(
        <BuyWindow cannel={this.cannel.bind(this)}/>
      )
    }else{
      return(
        <LoginWindow cannel={this.cannel.bind(this)}/>
      )
    }
  }

}

export class BuyWindow extends Component {

  render(){
    return(
      <TouchableWithoutFeedback onPress={this.props.cannel}>
        <View style={styles.container}>
          <View style={styles.buyWindow}>
            <TouchableOpacity>
              <View style={styles.payButton}>
                <Text style={{color: '#fff'}} >包场一年</Text>
              </View>
            </TouchableOpacity>
            <TouchableOpacity onPress={this.props.cannel}>
              <View style={styles.cannelButton}>
                <Text style={{color: '#fff'}} >银子不够</Text>
              </View>
            </TouchableOpacity>
          </View>
        </View>
      </TouchableWithoutFeedback>

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
    console.log("--------------Login Window------------------")
    return(
      <TouchableWithoutFeedback onPress={this.props.cannel}>
        <View style={styles.container}>
          <View style={styles.window}>
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
                <Text style={{color: '#fff'}} >登录</Text>
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
                <Image source={require('../images/QQ.png')} style={styles.oauthImage}/>
              </TouchableOpacity>
              <TouchableOpacity onPress={Application.unSupport}>
                <Image source={require('../images/weixin.png')} style={styles.oauthImage}/>
              </TouchableOpacity>
            </View>
          </View>
        </View>
      </TouchableWithoutFeedback>
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
    backgroundColor: "transparent",
  },

  window:{
    flexDirection: 'column',
    marginTop: 150,
    paddingTop:10,
    alignItems: 'center',
    zIndex: 99,
    backgroundColor: "white",
    borderRadius: 5,
    borderWidth: 1,
    width: 300,
    height: 280
  },

  buyWindow:{
    flexDirection: 'column',
    marginTop: 150,
    paddingTop:10,
    alignItems: 'center',
    zIndex: 99,
    backgroundColor: "white",
    borderRadius: 5,
    borderWidth: 1,
    width: 300,
    height: 200
  },

  oauthContainer: {
    height: 80,
    flexDirection: 'row',
    justifyContent: 'space-around',
    alignItems: 'center',
  },

  oauthImage: {
    height: 30,
    resizeMode: Image.resizeMode.contain
  },

  inputLogo: {
    height: 30,
    width: 30,
    marginLeft: 10,
    resizeMode: Image.resizeMode.contain
  },

  inputContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    marginLeft: 10,
    marginRight: 10,
    marginBottom: 10,
    backgroundColor: '#DFE0E1',
    borderRadius: 5,
    height:40
  },

  input:{
    backgroundColor: '#DFE0E1',
    height: 40,
    width: 250,
    paddingLeft: 10,
    fontSize: 16,
    borderRadius: 5,
  },

  loginButton:{
    marginLeft: 10,
    marginRight: 10,
    backgroundColor: '#FC4A68',
    height: 35,
    width: 290,
    borderRadius: 5,
    justifyContent: 'center',
    alignItems: 'center',
  },

  payButton:{
    marginLeft: 10,
    marginRight: 10,
    marginTop: 25,
    backgroundColor: '#FC4A68',
    height: 35,
    width: 290,
    borderRadius: 5,
    justifyContent: 'center',
    alignItems: 'center',
  },

  cannelButton:{
    marginLeft: 10,
    marginRight: 10,
    marginTop: 25,
    backgroundColor: '#C3C3C3',
    height: 35,
    width: 290,
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
  }
})
