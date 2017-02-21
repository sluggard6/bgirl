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
  default_host : "http://test.api.vogor.cn/",
  pr: PixelRatio.get()
};

export default Global;
