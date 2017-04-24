import React from 'react';
import Dimensions from 'Dimensions';
import {
  PixelRatio
} from 'react-native';


const Global = {
  size: {
    width: Dimensions.get('window').width,
    height: Dimensions.get('window').height
  },
  products:{
    1: 3900,
    2: 29900
  },
  urls: {
    profile: "/profile",
    channel: "/group/list/",
    group: "/group/",
    page: "/page/",
    checkPhone: "/user/checkPhone",
    vcode: "/vcode",
    register: "/user/register",
    login: "/user/login",
    logout: "/logout",
    user: "/user/profile",
    charge: "/charge/do",
    pic: "/pic/"
  },
  guide: {
    image1: require('../images/guide_1.jpg'),
    image2: require('../images/guide_2.jpg'),
    image3: require('../images/guide_3.jpg')
  },
  user: {
    balance: 0,
    id: 0,
    nick: "",
    phone: "",
    realname: "",
    score: 0,
    status: 0,
    vipend: 0
  },
  isLogin: false,
  buildVersion : '0.1.0',
  default_host : "http://test.api.vogor.cn",
  loadingPage : require('../images/pic.jpg'),
  pr: PixelRatio.get(),
  maxView: 3,
  isAlert: false,
  serverTime: new Date().getTime(),
  navigator: null
};

export default Global;
