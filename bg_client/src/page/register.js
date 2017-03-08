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

const VCODE = "/vcode"

export default class Register extends Component{

  constructor(props) {
    super(props);
    console.log(props.phone)
    this.state = {
      loading: false,
      seconds: 60,
      isDisabled: false,
      phone: ""
    };
  }

  countdown(seconds,isDisabled) {
    this.setState({seconds: seconds,isDisabled:isDisabled});
  }

  resetCount() {
    this.setState({seconds: 60,isDisabled:false})
  }

  onPress() {
    this.interval = setInterval(() => {
      this.props.countdown(this.props.seconds - 1,true);
    }, 1000);
    this.props.onVerfiy();
  }

  render(){
    const checked = this.state.checked ? require('../images/xuanzhong.png') : require('../images/weixuan.png');
    return (
      <View style={styles.loginContainer}>
        <View style={styles.topBar} />
        <View style={{flexDirection: 'row', alignItems: 'center',}}>
          <View style={styles.shortInputContainer}>
            <Image source={require('../images/shouji_w.png')} style={styles.inputLogo}/>
            <TextInput
              onChangeText={(phone) => {
                this.state.phone = phone
              }}
              underlineColorAndroid="transparent"
              style={styles.shortInput}
              placeholder='输入验证码' />
          </View>
          <TouchableOpacity onPress={()=>this.onPress()}
              style={{backgroundColor: '#ff5a37',width:150}}
              textStyle={{fontSize: 18}}
              isDisabled={this.props.isDisabled}>
            <View style={styles.vcodeBtn}>
              <Text style={{color: '#fff'}} >获取验证码</Text>
            </View>
          </TouchableOpacity>
        </View>
        <View style={styles.inputContainer}>
          <Image source={require('../images/mima_w.png')} style={styles.inputLogo}/>
          <TextInput
            underlineColorAndroid="transparent"
            secureTextEntry={true}
            style={styles.input}
            placeholder='密码'
            password={true} />
        </View>
        <View style={styles.inputContainer}>
          <Image source={require('../images/mima_w.png')} style={styles.inputLogo}/>
          <TextInput
            underlineColorAndroid="transparent"
            secureTextEntry={true}
            style={styles.input}
            placeholder='重复密码'
            password={true} />
        </View>
        <TouchableOpacity>
          <View style={styles.loginButton}>
            <Text style={{color: '#fff', fontSize: 22}} >完成</Text>
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

  vcodeBtn: {
    marginRight: 20,
    marginTop: 20,
    backgroundColor: "#ff4563",
    borderRadius: 5,
    alignItems: 'center',
    justifyContent: 'center',
    height: 40,
    width: (Global.size.width - 40)*1/3 - 5
  },

  shortInputContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    marginLeft: 20,
    marginRight: 7,
    marginTop: 20,
    backgroundColor: '#e0e0e0',
    borderRadius: 5,
    height:40,
    width: (Global.size.width - 40)*2/3 - 5
  },

  shortInput: {
    backgroundColor: '#e0e0e0',
    height: 40,
    width: 120,
    paddingLeft: 10,
    fontSize: 16,
    borderRadius: 5,
  },

  inputContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    marginLeft: 20,
    marginRight: 20,
    marginTop: 20,
    backgroundColor: '#e0e0e0',
    borderRadius: 5,
    height:40
  },

  input: {
    backgroundColor: '#e0e0e0',
    height: 40,
    width: Global.size.width - 100,
    paddingLeft: 10,
    fontSize: 16,
    borderRadius: 5,
  },

  checkedImage: {
    height: 15,
    resizeMode: Image.resizeMode.contain
  },

  loginButton:{
    margin: 20,
    backgroundColor: '#ff4563',
    height: 35,
    borderRadius: 5,
    justifyContent: 'center',
    alignItems: 'center',
  }
})
