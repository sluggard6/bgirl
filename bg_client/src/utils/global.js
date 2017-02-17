import React from 'react';
import Dimensions from 'Dimensions';

const Global = {
  size: {
    width: Dimensions.get('window').width,
    height: Dimensions.get('window').height
  },
  default_host : "http://test.api.vogor.cn/"
};

export default Global;
