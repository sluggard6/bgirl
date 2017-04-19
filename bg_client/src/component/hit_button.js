// @flow

import React, {Component} from 'react';


import {
  StyleSheet,
  View,
  Image,
  Text,
  TouchableOpacity,
  ToastAndroid,
  AsyncStorage
} from 'react-native';

import Global from '../utils/global'
import Application from '../utils/application'
import Http from '../utils/http'

export default class HitButton extends Component {

  constructor(props) {
		super(props);
    this.state={
      good: false,
      bad: false
    }
	}

  componentDidMount(){
    AsyncStorage.getItem('pic:'+this.props.pic.id).then((hit) => {
      console.log(hit)
      if(hit != null) {
        this.setState(JSON.parse(hit))
      }
    })
  }

  good(){
    if(!Global.isLogin) {
      ToastAndroid.show("请先登录!", ToastAndroid.SHORT)
      this.props.doAlert(false)
      return
    }
    if(this.state.good) {
      ToastAndroid.show("已经赞过了", ToastAndroid.SHORT)
      return
    }
    if(this.state.bad){
      this.props.pic.bad -= 1
    }
    this.props.pic.good += 1
    Http.httpGet(Application.getUrl(Global.urls.pic)+this.props.pic.id+"/good",(res) => {
      if(res.success){
        AsyncStorage.setItem("pic:"+this.props.pic.id, JSON.stringify({
          good: true,
          bad: false
        }))
      }
    })
    this.setState({
      good: true,
      bad: false
    })

  }

  bad(){
    if(!Global.isLogin) {
      ToastAndroid.show("请先登录!", ToastAndroid.SHORT)
      this.props.doAlert(false)
      return
    }
    if(this.state.bad) {
      ToastAndroid.show("已经踩过了", ToastAndroid.SHORT)
      return
    }
    if(this.state.good){
      this.props.pic.good -= 1
    }
    this.props.pic.bad += 1
    Http.httpGet(Application.getUrl(Global.urls.pic)+this.props.pic.id+"/bad",(res) => {
      if(res.success){
        AsyncStorage.setItem("pic:"+this.props.pic.id, JSON.stringify({
          good: false,
          bad: true
        }))
      }
    })
    this.setState({
      bad: true,
      good: false
    })
  }

  render() {
    return(
      <View style={styles.bottom}> 
        <TouchableOpacity onPress={this.good.bind(this)}>
          <Image source={require('../images/zan.png')} style={styles.image}/>
        </TouchableOpacity>
        <Text style={{fontSize: 18, paddingLeft: 20, paddingRight: 20}}>{this.props.pic.good}</Text>
        <TouchableOpacity onPress={this.bad.bind(this)}>
          <Image source={require('../images/cai.png')} style={styles.image}/>
        </TouchableOpacity>
        <Text style={{fontSize: 18, paddingLeft: 20, paddingRight: 20}}>{this.props.pic.bad}</Text>
      </View>
    )
  }

}

var styles = StyleSheet.create({

  bottom: {
    flexDirection: "row",
    justifyContent: 'center',
    alignItems: 'center',
    height: (140/Global.pr)
    // backgroundColor: "white"
  },

  image: {
    width: 30, 
    height: 30, 
    resizeMode: Image.resizeMode.contain
  }
})