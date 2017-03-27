import React, {Component} from 'react';
import {
  AsyncStorage
} from 'react-native';

import Global from './global'
import Http from './http'

export default class Application {

  static localLogin(uname, pwd, seid) {
    Http.httpGet(Application.getUrl(Global.urls.user), (res) => {
      console.log(res)
      if(res.success === true) {
        Global.user = res.user
        AsyncStorage.setItem('uname', uname)
        AsyncStorage.setItem('pwd', pwd)
        AsyncStorage.setItem('seid', seid)
        Global.isLogin = true
      }
    })
  }

  static isVip() {
    if(Global.isLogin){
      return Global.user.vipend > Global.serverTime
    }
    return false
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
