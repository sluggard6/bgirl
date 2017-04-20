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



export default class FullViewTab extends Component {

  constructor(props) {
		super(props);
    this.state = {
      pics: "",
      // loaded: false,
      locked: false,
      alert: false,
      goBack: false,
      tabNumber: 0
    }
    // this._loadData = this._loadData.bind(this)
  }

  // componentDidMount() {
  //   this._loadData();
  // }

  componentDidUpdate() {
    if(this.state.goBack) {
      this.state.goBack = false
      if(!Application.isVip() && this.state.tabNumber >= Global.maxView) {
        this.tabView.goToPage(Global.maxView - 1)
      }
    }
  }

  // _loadData() {
  //   url = Application.getUrl(Global.urls.group)+this.props.componentId
  //   Http.httpGet(url, this._setData.bind(this))
  // }

  // _setData(responseData) {
  //   this.setState({
  //     pics: responseData.pics,
  //     loaded: true,
  //     alert: false
  //   })
  // }

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
    /*if(!this.state.loaded){
      return (
        <View style={styles.loading}>
          <Text>
            Loading data...
          </Text>
        </View>
      );
    }else{*/
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
          >
          {
            this.props.pics.map((pic, index) => {
              return (
                <FullPicView 
                  pic={pic} 
                  tabLabel={index+1} 
                  key={index} 
                  alert={this.state.alert} 
                  cannel={this.cannel.bind(this)} 
                  doAlert={this.doAlert.bind(this)}
                />);  // 单行箭头函数无需写return
            })
          }
        </ScrollableTabView>
      );
    // }
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
