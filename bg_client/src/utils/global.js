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
  urls: {
    profile: "/profile",
    channel: "/channel/list",
    group: "/group/",
    pageIndex: "/page/index",
    checkPhone: "/user/checkPhone",
    vcode: "/vcode",
    register: "/user/register",
    login: "/user/login",
    profile: "/user/profile",
    charge:"/charge/do"
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
    realname: "",
    score: 0,
    status: 0,
  },
  isLogin: false,
  buildVersion : '0.1.0',
  default_host : "http://test.api.vogor.cn",
  pr: PixelRatio.get()
};

export default Global;
