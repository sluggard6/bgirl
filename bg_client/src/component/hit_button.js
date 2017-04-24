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
      good: false
    }
	}

  componentDidMount(){
    AsyncStorage.getItem('pic:'+this.props.pic.id).then((hit) => {
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
    this.props.pic.good += 1
    Http.httpGet(Application.getUrl(Global.urls.pic)+this.props.pic.id+"/good",(res) => {
      if(res.success){
        AsyncStorage.setItem("pic:"+this.props.pic.id, JSON.stringify({
          good: true,
        }))
      }
    })
    this.setState({
      good: true
    })

  }


  render() {
    return(
      <View style={styles.bottom}> 
        <Text style={styles.designation}>{this.props.group.id}:{this.props.pic.id}:{this.props.group.designation}</Text>
        <View style={styles.good}>
          <TouchableOpacity onPress={this.good.bind(this)}>
            <Image source={require('../images/zan.png')} style={styles.image}/>
          </TouchableOpacity>
          <Text style={{fontSize: 18, paddingLeft: 20, paddingRight: 20}}>{this.props.pic.good}</Text>
        </View>
      </View>
    )
  }

}

var styles = StyleSheet.create({

  bottom: {
    flexDirection: "row",
    justifyContent: 'center',
    alignItems: 'center',
    height: 50
    // backgroundColor: "white"
  },

  designation: {
    width: Global.size.width*2/5,
    backgroundColor: '#FC4A68',
    textAlign: 'center',
    textAlignVertical: 'center',
    fontSize: 14,
    color: "white",
    height: 50
  },

  good: {
    flexDirection: "row",
    justifyContent: 'center',
    alignItems: 'center',
    height: 50,
    width: Global.size.width*3/5
  },

  image: {
    width: 30, 
    height: 30, 
    resizeMode: Image.resizeMode.contain
  }
})