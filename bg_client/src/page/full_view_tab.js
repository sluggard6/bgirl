import React, {Component} from 'react';
import {
  View,
  Text,
  StyleSheet,
  BackAndroid
} from 'react-native';
import ScrollableTabView, {DefaultTabBar, } from 'react-native-scrollable-tab-view';

import Http from '../utils/http'
import Global from '../utils/global'
import Application from '../utils/application'
import FullPicView from './full_view'
import FullPicTabBar from '../component/full_pic_bar'
import UMNative from '../utils/umeng_native'



export default class FullViewTab extends Component {

  constructor(props) {
		super(props);
    this.state = {
      pics: "",
      locked: false,
      alert: false,
      goBack: false,
      tabNumber: 0
    }
  }

  componentWillMount() {
    UMNative.onPageBegin("group")
  }

  componentWillUnmount() {
    UMNative.onPageEnd("group")
  }

  componentDidUpdate() {
    if(this.state.goBack) {
      this.state.goBack = false
      if(!Application.isVip() && this.state.tabNumber >= Global.maxView) {
        this.tabView.goToPage(Global.maxView - 1)
      }
    }
  }

  doAlert() {
    this.setState({
      locked: true,
      alert: true
    })
  }

  cannel() {
    this.setState({
      locked: false,
      alert: false,
      goBack: true
    })
  }

  render() {
    return (
      <ScrollableTabView
        renderTabBar={() => <FullPicTabBar/>}
        tabBarPosition="top"
        ref={(tabView) => { this.tabView = tabView; }}
        locked={this.state.locked}
        onChangeTab={(tab) => {
          this.state.tabNumber = tab.i
          if(tab.i >= Global.maxView) {
            if(!Application.isVip()){
              this.doAlert()
            }
          }
        }}
        onScroll={(e) => {
          console.log(e)
        }}
        >
        {
          this.props.pics.map((pic, index) => {
            return (
              <FullPicView 
                pic={pic}
                group={this.props.group}
                tabLabel={index+1} 
                key={index} 
                alert={this.state.alert} 
                cannel={this.cannel.bind(this)} 
                doAlert={this.doAlert.bind(this)}
              />);  // 单行箭头函数无需写return
          })
        }
      </ScrollableTabView>
    )
  }
}

var styles = StyleSheet.create({
  loading: {
    flex: 1,
    flexDirection: 'row',
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#F5FCFF',
  }
});
