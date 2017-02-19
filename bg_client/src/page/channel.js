// @flow

import React, { Component } from 'react';
import {
  AppRegistry,
  View,
  ListView,
  StyleSheet,
  Text
} from 'react-native';

import ViewChannel from '../component/view_channel'
import Http from '../utils/http'
import Global from '../utils/global'
import TopBar from '../component/top_bar'

const CHANNEL_URL = '/channel/list'

export default class Channel extends Component {

  constructor(props) {
    super(props);
    this.state = {
      dataSource: new ListView.DataSource({rowHasChanged: (r1, r2) => r1 !== r2}),
      loaded: false,
    };
    this.setState.bind(this)
    this._updateDataSource.bind(this)
  }

  _updateDataSource(responseData){
    this.setState({
      dataSource: this.state.dataSource.cloneWithRows(responseData.channels),
      loaded: true,
    });
  }

  fetchData() {
    url = Global.host + CHANNEL_URL
    Http.httpGet(url,this._updateDataSource.bind(this))
  }

  componentDidMount() {
    this.fetchData();
  }

  _renderRow(rowData,sectionID, rowID ){
    return (
      <ViewChannel data={rowData} />
    );
  }

  render(){
    if(this.state.loaded){
      return (
        <View style={styles.container}>
          <TopBar/>
          <ListView
            style={styles.channel_list}
            dataSource={this.state.dataSource}
            renderRow={this._renderRow.bind(this)}
          />
        </View>
      );
    }else{
      return (
        <View style={styles.loading}>
          <Text>
            Loading data...
          </Text>
        </View>
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
