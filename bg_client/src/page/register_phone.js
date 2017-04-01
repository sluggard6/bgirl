import React, { Component } from 'react';

import {
  Image,
  View,
  Text,
  TextInput,
  StyleSheet,
  TouchableOpacity,
  ToastAndroid
} from 'react-native';

import Global from '../utils/global';
import Application from '../utils/application'
import Http from '../utils/http'
import Register from './register'


export default class RegisterPhone extends Component{

  constructor(props) {
    super(props);
    this.state = {
      loading: false,
      checked: true,
      phone: ""
    };
    this.checkPhone = this.checkPhone.bind(this);
  }

  goRegister() {
    if(!this.state.checked) {
      ToastAndroid.show("请先阅读并同意《用户服务条款》", ToastAndroid.SHORT)
      return
    }
    url = Application.getUrl(Global.urls.checkPhone) + "?phone=" + this.state.phone
    Http.httpGet(url,this.checkPhone.bind(this))
  }

  checkPhone(res) {
    if(res.success == true) {
      this.props.navigator.push({
        component: Register,
        params: {
          phone: this.state.phone
        }
      })
    }else{
      ToastAndroid.show(res.message, ToastAndroid.SHORT)
    }
  }

  checkRule() {
    this.setState({
      checked: !this.state.checked
    })
  }

  render(){
    const checked = this.state.checked ? require('../images/xuanzhong.png') : require('../images/weixuan.png');
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
        <TouchableOpacity onPress={this.checkRule.bind(this)}>
          <View style={{flexDirection: 'row', width:Global.size.width - 40,justifyContent: 'center', alignItems: 'center', margin: 20}}>
            <Image source={checked} style={styles.checkedImage}/>
            <Text>我已阅读并同意</Text>
            <Text style={{color: 'red'}}>《用户服务条款》</Text>
          </View>
        </TouchableOpacity>
        <TouchableOpacity onPress={this.goRegister.bind(this)}>
          <View style={styles.loginButton}>
            <Text style={{color: '#fff'}} >下一步</Text>
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
    marginTop: 20,
    backgroundColor: '#DFE0E1',
    borderRadius: 5,
    height:40
  },

  input: {
    backgroundColor: '#DFE0E1',
    height: 40,
    width: Global.size.width - 80,
    paddingLeft: 10,
    fontSize: 16,
    borderRadius: 5,
  },

  checkedImage: {
    height: 15,
    resizeMode: Image.resizeMode.contain
  },

  loginButton:{
    marginLeft: 20,
    marginRight: 20,
    backgroundColor: '#FC4A68',
    height: 35,
    borderRadius: 5,
    justifyContent: 'center',
    alignItems: 'center',
  }
})
