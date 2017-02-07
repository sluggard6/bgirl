import React, { Component } from 'react';

import {
  Image,
  View,
  Text,
  TextInput,
  StyleSheet
} from 'react-native';

export default class Login extends Component{

  render(){
    return (
      <View style={styles.loginContainer}>
        <Image
          style={styles.logoImage}
          source={{uri: 'http://7xr387.com1.z0.glb.clouddn.com/logo2.png'}} />
        <TextInput
          underlineColorAndroid="transparent"
          style={styles.accountInput}
          placeholder='手机号码' />
          <View style={{height:1,backgroundColor:'#f4f4f4'}} />
        <TextInput
          underlineColorAndroid="transparent"
          style={styles.passowrdInput}
          placeholder='密码'
          password={true} />
        <View style={styles.loginButton}>
          <Text style={{color: '#fff'}} >Login</Text>
        </View>
        <View style={{flex:1,flexDirection:'row',alignItems: 'flex-end',bottom:10}}>
          <Text style={styles.viewUnlogin}>
               无法登录?
          </Text>
          <Text style={styles.viewRegister}>
               新用户
          </Text>
        </View>
      </View>
    )
  }
}

var styles = StyleSheet.create({
  loginContainer: {
    flex: 1,
    backgroundColor: '#f4f4f4',
    paddingLeft:10,
    paddingRight:10,
  },

  logoImage:{
    borderRadius: 35,
    height: 70,
    width: 70,
    marginTop: 120,
    alignSelf: 'center',
  },

  accountInput:{
    backgroundColor: '#fff',
    marginTop: 20,
    height: 40,
    paddingLeft: 20,
    fontSize: 16,
    borderWidth: 1,
    borderRadius: 5,
    borderColor: 'lightblue',
  },

  passowrdInput:{
    backgroundColor: '#fff',
    height: 40,
    paddingLeft: 20,
    fontSize: 16,
    borderWidth: 1,
    borderRadius: 5,
    borderColor: 'lightblue',
  },

  loginButton:{
    marginTop: 15,
    marginLeft: 10,
    marginRight: 10,
    backgroundColor: '#63B8FF',
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
