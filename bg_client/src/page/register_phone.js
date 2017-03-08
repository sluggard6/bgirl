import React, { Component } from 'react';

import {
  Image,
  View,
  Text,
  TextInput,
  StyleSheet,
  TouchableOpacity
} from 'react-native';

import Global from '../utils/global';
import Http from '../utils/http'

const CHECK_PHONE = "/user/checkPhone"

export default class RegisterPhone extends Component{

  constructor(props) {
    super(props);
    this.state = {
      loading: false,
      phone: ""
    };
    this.checkPhone = this.checkPhone.bind(this);
  }

  goRegister() {
    url = Global.default_host + CHECK_PHONE + "?phone=" + this.state.phone
    Http.httpGet(url,this.checkPhone.bind(this))
  }

  checkPhone(responseData) {
    console.log(responseData)
  }

  render(){
    return (
      <View style={styles.loginContainer}>
        <View style={styles.topBar}>
          <Text style={{color: '#fff', fontSize: 20}}>注   册</Text>
        </View>
        <View style={styles.inputContainer}>
          <Image source={require('../images/shouji.png')} style={styles.inputLogo}/>
          <TextInput
            onChangeText={(phone) => {
              this.state.phone = phone
            }}
            underlineColorAndroid="transparent"
            style={styles.input}
            placeholder='手机号码' />
            <View style={{height:1,backgroundColor:'#f4f4f4'}} />
        </View>
        <TouchableOpacity onPress={this.goRegister.bind(this)}>
          <View style={styles.loginButton}>
            <Text style={{color: '#fff'}} >自动登录</Text>
          </View>
        </TouchableOpacity>
      </View>
    )
  }
}

var styles = StyleSheet.create({
  loginContainer: {
    flex: 1,
    backgroundColor: '#f4f4f4',
  },

  topBar: {
    justifyContent: 'center',
    alignItems: 'center',
    height: 200/Global.pr,
    width: Global.size.width,
    backgroundColor: '#313840'
  },

  logoImage:{
    borderRadius: 35,
    height: 90,
    width: 90,
    marginTop: 120,
    alignSelf: 'center',
  },

  inputLogo: {
    height: 30,
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
    backgroundColor: '#DFE0E1',
    height: 40,
    width: Global.size.width - 80,
    paddingLeft: 10,
    fontSize: 16,
    borderRadius: 5,
  },

  loginButton:{
    margin: 20,
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
    alignItems:'flex-end',
    flex:1,
    flexDirection:'row',
    textAlign:'right',
  }
})
