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
      loaded: false,
      locked: false,
      goBack: true
    }
    this._loadData = this._loadData.bind(this)
  }

  componentDidMount() {
    this._loadData();
  }

  componentDidUpdate() {
    if(this.state.goBack) {
      this.state.goBack = false
      this.tabView.goToPage(Global.maxView - 1)
    } 
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

  doLock() {
    this.setState({
      locked: true
    })
  }

  unLock() {
    this.setState({
      locked: false,
      goBack: true
    })
  }

  render() {
    // console.log("scrollable view render : " + this.state.locked)
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
          locked={this.state.locked}
          onChangeTab={(tab) => {
            {/*console.log("onChangeTab : " + tab.i)*/}
            if(tab.i >= Global.maxView) {
              if(!Application.isVip()){
                Application.doAlert()
                this.doLock()
              }
            }
          }}
          >
          {
            this.state.pics.map((pic, index) => {
              return (<FullPicView pic={pic} tabLabel={index+1} key={index} unLock={this.unLock.bind(this)}/>);  // 单行箭头函数无需写return
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
