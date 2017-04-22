// @flow

import React, { Component } from 'react';

import {
  View,
  Text,
  Image,
  StyleSheet
} from 'react-native'

import {TextTopBar} from '../component/top_bar'
import Global from '../utils/global'

export default class AboutUs extends Component {

  render() {
    return(
      <View style={styles.container}>
        <TextTopBar text={"关于我们"}/>
        <Image source={require('../images/pic1.png')} style={styles.head}/>
        <View style={styles.body}>
          <View style={styles.left}>
            <Image source={require('../images/logo_w.png')} style={styles.logo}/>
            <Text style={styles.text}>        昧昧是隶属于上海浮歌信息科技有限公司致力于美学向文化艺术的发展思路，以高品质美图和创意美学视频为内容载体，建立一个汇聚模特网红、摄影爱好者、艺术追求者、以及粉丝用户的全方位互动平台。</Text>
          </View>
          <Image source={require('../images//pic2.png')} style={styles.right}/>
        </View>
      </View>
    )
  }
}


const styles = StyleSheet.create({

  container: {
    flex: 1,
    flexDirection: 'column',
    flexWrap: 'nowrap',
    alignItems: 'center'
  },

  head: {
    width: Global.size.width,
    height: (Global.size.height-200/Global.pr)/3
  },

  body: {
    width: Global.size.width,
    height: (Global.size.height-200/Global.pr)*2/3,
    flexDirection: 'row',
    alignItems: 'center'
  },

  left: {
    flexDirection: 'column',
    justifyContent: 'space-around',
    alignItems: 'center',
    width: Global.size.width/2,
  },

  logo: {
    width: 100,
    height: 100,
    resizeMode: 'contain',
    marginBottom: 50
  },

  text: {
    borderTopWidth: 2,
    paddingTop: 30,
    width: Global.size.width/2-100,
    fontSize: 18
  },

  right: {
    width: Global.size.width/2,
    height: (Global.size.height-200/Global.pr)*2/3,
  },

})