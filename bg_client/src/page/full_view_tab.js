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
import LoginWindow from '../component/login'



export default class FullViewTab extends Component {

  constructor(props) {
		super(props);
    this.state = {
      pics: "",
      loaded: false,
      alert: false,
    }
    this._loadData = this._loadData.bind(this);
    this._doAlert = this._doAlert.bind(this);
  }

  componentDidMount() {
    this._loadData();
  }

  _loadData() {
    url = Application.getUrl(Global.urls.group)+this.props.componentId
    Http.httpGet(url, this._setData.bind(this))
  }

  _setData(responseData) {
    this.setState({
      pics: responseData.pics,
      loaded: true,
      alert: false
    })
  }

  _doAlert() {
    if(this.state.alert) {
      return <LoginWindow/>
    }
  }

  render() {
    if(!this.state.loaded){
      return (
        <View style={styles.loading}>
          <Text>
            Loading data...
          </Text>
        </View>
      );
    }else{
      return (
        <ScrollableTabView
          renderTabBar={() => <FullPicTabBar/>}
          tabBarPosition="top"
          ref={(tabView) => { this.tabView = tabView; }}
          onChangeTab={(tab) => {
            console.log("onChangeTab : " + tab.i)
            if(tab.i >= Global.maxView) {
              if(!Application.isVip()){
                this.tabView.goToPage(tab.from)
              }
            }
          }}
          >
          {
            this.state.pics.map((pic, index) => {
              return (<FullPicView pic={pic} tabLabel={index+1} key={index} alert={false}/>);  // 单行箭头函数无需写return
            })
          }
        </ScrollableTabView>
      );
    }

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
