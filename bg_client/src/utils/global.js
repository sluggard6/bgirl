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
  buildVersion : '0.1.0',
  default_host : "http://192.168.12.104:8290",
  pr: PixelRatio.get(),
  logined: false
};

export default Global;
