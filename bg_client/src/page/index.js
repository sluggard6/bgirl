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


const defaultRoute = {
  component: Guide
};

const buildVersion = '0.1.0'

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
