// @flow

import React, { Component } from 'react';

import {
  View,
  Text,
  Image,
  TextInput,
  StyleSheet
} from 'react-native'

import {TextTopBar} from '../component/top_bar'
import Global from '../utils/global'

export default class Download extends Component {

  constructor(props) {
    super(props)
    this.state = {
      qq:"",
      weixin:""
    }
  }
  
  render() {
    return(
      <View style={styles.container}>
        <TextTopBar text={"下载说明"}/>
        <View style={styles.icon_view}>
          <Image source={require('../images/1.jpg')} style={styles.icon_img}/>
        </View>
        <View style={styles.inputContainer}>
          <Image source={require('../images/qq_b.png')} style={styles.inputLogo}/>
          <Text style={styles.input_text}>Q Q 客服 : 1057691850</Text>
        </View>
        <View style={[styles.inputContainer,{borderBottomWidth: 1}]}>
          <Image source={require('../images/weixin_b.png')} style={styles.inputLogo}/>
          <Text style={styles.input_text}>微信客服 : </Text>
        </View>
        <Image source={require('../images/renwu.png')} style={{width: 140,height: 100,marginTop: 35, resizeMode: Image.resizeMode.contain}}/>
        <Text style={styles.mid_text}>亲爱的哥哥，妹妹们的高清大图等您带回家</Text>
        <View style={styles.row_container}>
          <Image source={require('../images/erweima.png')} style={styles.left_image}/>
          <Text style={styles.right_text}>只需要通过微信关注“昧昧的御花园”公众号-公众号中留言：【下载】将会有小美眉来联系您，3步就能轻松搞定哟！</Text>
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
    alignItems: 'center',
    justifyContent: 'flex-start',
    backgroundColor: '#F2F3F4'
  },

  icon_view: {
    justifyContent: 'center',
    alignItems: 'center'
  },

  icon_img:{
    height: 100,
    width: Global.size.width
  },

  input_text: {
    width: 250
  },

  logoImage: {
    borderRadius: 35,
    height: 90,
    width: 90,
    marginTop: 120,
    alignSelf: 'center',
  },

  inputLogo: {
    height: 20,
    width: 20,
    marginLeft: 10,
    marginRight: 10,
    resizeMode: Image.resizeMode.contain
  },

  inputContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    width: Global.size.width,
    backgroundColor: 'white',
    height:40,
    borderTopWidth: 1,
    borderColor: "#DFE0E1"
  },

  input:{
    backgroundColor: 'transparent',
    height: 40,
    width: Global.size.width - 100,
    paddingLeft: 10,
    fontSize: 14,
  },

  mid_text: {
    width: Global.size.width,
    height: 35,
    textAlign: 'center',
    color: "red",
    textAlignVertical: "center",
    borderTopWidth: 1,
    borderBottomWidth: 1,
    borderColor: "#DFE0E1",
    backgroundColor:"white"
  },

  row_container: {
    flexDirection: "row",
    justifyContent: "center",
    alignItems: "center",
    width: Global.size.width,
    height: 150
  },

  left_image: {
    width: Global.size.width/3-30,
    height: Global.size.width/3-30,
    margin: 10
  },

  right_text: {
    width: Global.size.width*2/3,
    height: Global.size.width/3,
    paddingLeft: 20,
    paddingRight: 20,
    paddingTop: 10,
    letterSpacing: 10,
    lineHeight:25,
    fontSize: 12
  }
})