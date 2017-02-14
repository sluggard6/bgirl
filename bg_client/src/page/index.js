// @flow

import React, { Component } from 'react';
import {
  AppRegistry,
  Navigator,
  View,
  AsyncStorage,
  Text,
  StyleSheet,
  Image,
  TouchableOpacity
} from 'react-native';

import Guide from './guide';
import TabBarView from './tab_bar_view'
import Main from './main';
import Http from '../utils/http'
import Global from '../utils/global'

const defaultRoute = {
  component: Guide
};

const buildVersion = '0.1.0'

const PROFILE_URL = Global.default_host +  "/profile"

class Index extends Component {
  constructor(props) {
    super(props);   //这一句不能省略，照抄即可
    this.state = {
      version: null,  //这里放你自己定义的state变量及初始值
    };
    this.loadVersion = this.loadVersion.bind(this)
  }

  componentDidMount() {
    this.loadVersion();
    this.loadProfile();
  }

  loadProfile() {
    Http.httpGet(PROFILE_URL,function(responseData){
      profile = responseData.profile
      Global.host = "http://" + profile.host + ":" + profile.port
    })
  }


  async loadVersion() {
    storageVersion = await AsyncStorage.getItem('buildVersion');
    if(!storageVersion) {storageVersion = "None"}
    this.setState({
      version: storageVersion
    })
  }

  _renderScene(route, navigator) {
    let Component = route.component;
    console.log(Component);
    return (
      <Component {...route.params} navigator={navigator} />
    );
  }

  rerenderLoadingView() {
    return (
      <View style={styles.container}>
        <Text>
          正在加载数据……
        </Text>
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


AppRegistry.registerComponent('bg_client', () => Index );
