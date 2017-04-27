// @flow

import React, { Component } from 'react';
import {
  AppRegistry,
  Platform,
  Navigator,
  View,
  AsyncStorage,
  Text,
  StyleSheet,
  Image,
  TouchableOpacity,
  ToastAndroid,
  BackAndroid
} from 'react-native';

import Guide from './guide';
import TabBarView from './tab_bar_view'
import Main from './main';
import Http from '../utils/http'
import Global from '../utils/global'
import Application from '../utils/application'
import * as WeChat from 'react-native-wechat'
import UMNative from '../utils/umeng_native'


const defaultRoute = {
  component: Guide
};

const buildVersion = '0.1.0'

class App extends Component {

  constructor(props) {
    super(props);   //这一句不能省略，照抄即可
    this.state = {
      version: null,  //这里放你自己定义的state变量及初始值
    };
  }

  componentWillMount() {
    if (Platform.OS === 'android') {
      BackAndroid.addEventListener('hardwareBackPress', this.onBackAndroid);
    }
    UMNative.onPageBegin("App")
  }

  componentWillUnmount() {
    if (Platform.OS === 'android') {
      BackAndroid.removeEventListener('hardwareBackPress', this.onBackAndroid);
    }
    UMNative.onPageEnd("App")
  }

  onBackAndroid = () => {
    const nav = this.refs.navigator;
    const routers = nav.getCurrentRoutes();
    if (routers.length > 1) {
      nav.pop();
      return true;
    }
    if (this.lastBackPressed && this.lastBackPressed + 2000 >= Date.now()) {
      //最近2秒内按过back键，可以退出应用。
      return false;
    }
    this.lastBackPressed = Date.now();
    ToastAndroid.show('再按一次退出应用', ToastAndroid.SHORT);
    return true;
  };

  componentDidMount() {
    this.loadVersion();
    this.loadProfile();
    WeChat.registerApp('wx11eaa73053dd1666')
  }

  loadProfile() {
    Http.httpGet(Application.getUrl(Global.urls.profile),function(responseData){
      profile = responseData.profile
      Global.host = profile.host
    })
  }


  async loadVersion() {
    this.timer = setTimeout(() => {
      this.setState({
        version: storageVersion
      })
      this.timer && clearTimeout(this.timer)
    },2000)
    storageVersion = await AsyncStorage.getItem('buildVersion');
    if(!storageVersion) {storageVersion = "None"}
    
  }

  _renderScene(route, navigator) {
    let Component = route.component;
    return (
      <Component {...route.params} navigator={navigator} />
    );
  }

  rerenderLoadingView() {
    return (
      <View style={styles.container}>
        <Image source={Global.loadingPage} style={{width: Global.size.width, height: Global.size.height, resizeMode: Image.resizeMode.cover}}>
        </Image>
      </View>
    );
  }


  render() {
    if(!this.state.version) {
      return this.rerenderLoadingView();
    }
    if(this.state.version === buildVersion) {
      defaultRoute = {
        component: TabBarView
      }
    }else{
      AsyncStorage.setItem('buildVersion', buildVersion)
    }
    return (
      <Navigator
        initialRoute={defaultRoute}
        renderScene={this._renderScene}
        ref='navigator'
      />
    );
  }
}


var styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#F5FCFF',
  },

  tabs:{
    flexDirection:"row"
  }
});


AppRegistry.registerComponent('bg_client', () => App );
