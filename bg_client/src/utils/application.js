import React, {Component} from 'react';
import {
  AsyncStorage
} from 'react-native';

import Global from './global'
import Http from './http'

export default class Application {

  static login(uname, pwd, seid) {
    AsyncStorage.setItem('uname', uname)
    AsyncStorage.setItem('pwd', pwd)
    AsyncStorage.setItem('seid', seid)
    Global.logined = true
  }

  static autoLogin() {
    AsyncStorage.getItem('seid').then(
      (seid) => {
        Http.httpGet()
      }
    )
  }

  static getHost() {
    return Global.host||Global.default_host
  }

  static getUrl(url) {
    return Application.getHost() + url
  }
}
