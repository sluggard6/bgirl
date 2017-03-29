import React, {Component} from 'react';
import {
  AsyncStorage,
  ToastAndroid
} from 'react-native';

import Global from './global'
import Http from './http'
import TabBarView from '../page/tab_bar_view'

export default class Application {

  static localLogin(uname, pwd, seid) {
    Http.httpGet(Application.getUrl(Global.urls.user), (res) => {
      if(res.success === true) {
        Global.user = res.user
        AsyncStorage.setItem('uname', uname)
        AsyncStorage.setItem('pwd', pwd)
        AsyncStorage.setItem('seid', seid)
        Global.isLogin = true
      }
    })
  }

  static login(uname, pwd, callback) {
    console.log("uname : " + uname)
    console.log("pwd : " + pwd)
    console.log(callback)
    params = {
      uname: uname,
      pwd: pwd
    }
    Http.httpPost(Application.getUrl(Global.urls.login), params, (res) => {
      if(res.success === true) {
        Application.localLogin(uname, pwd, res.msg)
        console.log(typeof callback)
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



  // static autoLogin() {
  //   uname = AsyncStorage.getItem('uname')
  //   pwd = AsyncSotrage.getItem('pwd')
  //   if(uname != null && pwd != null) {
  //     Http.httpGet(Application.getHost(Global.url.login)+"?uname="+uname+"&pwd="+pwd)
  //   }
  //   AsyncStorage.getItem('seid').then(
  //     (seid) => {
  //       Http.httpGet()
  //     }
  //   )
  // }

  static getHost() {
    return Global.host||Global.default_host
  }

  static getUrl(url) {
    return Application.getHost() + url
  }
}
