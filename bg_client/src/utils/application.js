import React, {Component} from 'react';
import {
  AsyncStorage,
  ToastAndroid
} from 'react-native';

import Global from './global'
import Http from './http'
import TabBarView from '../page/tab_bar_view'

export default class Application {

  static saveLoginInfo(uname, pwd) {
    AsyncStorage.setItem('uname', uname)
    AsyncStorage.setItem('pwd', pwd)
  }

  static localLogin(seid) {
    console.log(Application.getUrl(Global.urls.user)+"?seid="+seid)
    Http.httpGet(Application.getUrl(Global.urls.user)+"?seid="+seid, (res) => {
      console.log(res)
      if(res.success === true) {
        Global.user = res.user
        AsyncStorage.setItem('seid', seid)
        Global.isLogin = true
      }else{
        AsyncStorage.removeItem('seid')
      }
    })
  }

  static autoLogin() {
    AsyncStorage.getItem('seid').then((seid) => {
      console.log(seid)
      if(seid != null) {
        Application.localLogin(seid)
      }
    })
  }


  static login(uname, pwd, callback) {
    // console.log("uname : " + uname)
    // console.log("pwd : " + pwd)
    // console.log(callback)
    params = {
      uname: uname,
      pwd: pwd
    }
    Http.httpPost(Application.getUrl(Global.urls.login), params, (res) => {
      if(res.success === true) {
        Application.saveLoginInfo(uname, pwd)
        Application.localLogin(res.msg)
        if(typeof callback === 'function'){
          callback()
        }
      }else{
        ToastAndroid.show(res.message,ToastAndroid.SHORT)
      }
    });
  }

  static unSupport() {
    ToastAndroid.show('敬请期待', ToastAndroid.SHORT);
  }

  static isVip() {
    if(Global.isLogin){
      return Global.user.vipend > Global.serverTime
    }
    return false
  }

  static doAlert() {
    Global.isAlert = true;
  }

  static cannel() {
    Global.isAlert = false;
  }

  static getHost() {
    return Global.host||Global.default_host
  }

  static getUrl(url) {
    return Application.getHost() + url
  }
}
