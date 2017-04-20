// @flow

import React, { Component } from 'react';
import {
  View,
  FlatList,
  StyleSheet,
  Text
} from 'react-native';

import ViewChannel from '../component/view_channel'
import Http from '../utils/http'
import Global from '../utils/global'
import Application from '../utils/application'
import TopBar from '../component/top_bar'
import FullViewTab from './full_view_tab'


export default class Channel extends Component {

  constructor(props) {
    super(props);
  }

  onPress(componentId) {
    url = Application.getUrl(Global.urls.group)+componentId
    Http.httpGet(url, (res)=>{
      Global.navigator.push({
        component: FullViewTab,
        params: {
          pics: res.pics
        }
      })
    })
  }

  _renderRow=({item}) => (<ViewChannel group={item} onPress={this.onPress.bind(this)}/>)

  render(){
    return (
      <View style={styles.container}>
        <TopBar/>
        <FlatList
          style={styles.channel_list}
          data={this.props.groups}
          renderItem={this._renderRow}
        />
      </View>
    );
  }
}

var styles = StyleSheet.create({
  loading: {
    flex: 1,
    flexDirection: 'row',
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#F5FCFF',
  },

  container: {
    flex: 1,
    flexDirection: 'column',
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: "#333740",
  },

  channel_list: {
    width: Global.size.width,
  }
});
