// @flow

import React, {Component} from 'react';

import {
  View,
  Text,
  ListView,
  StyleSheet,
  Navigator
} from 'react-native';

import Global from '../utils/global'

var user_info_menu = [
  {text:'我的下载', actionType:'innerView', actionPath:'downloaded'},
  {text:'未读消息', actionType:'innerView', actionPath:'downloaded'},
  {text:'每日任务', actionType:'innerView', actionPath:'downloaded'},
  {text:'个人设置', actionType:'innerView', actionPath:'downloaded'}
]

export default class User extends Component {
  constructor(props) {
    super(props)
    const ds = new ListView.DataSource({
      rowHasChanged: (row1, row2) => row1 !== row2,
    });
    this.state = {
      dataSource: ds.cloneWithRows(user_info_menu),
    };
  }

  _renderRow(menu) {
    return(
      <View style={styles.menu}>
        <Text>{menu.text}</Text>
      </View>
    );
  }

  render(){
    return (
      <View style={styles.container}>
        <View style={styles.userinfo}>
          <Text style={{fontSize: 25}}>Nick</Text>
        </View>
        <View style={styles.balance}>
          <Text style={{color: 'red'}}>VIP</Text>
          <Text>1000</Text>
        </View>
        <ListView
          dataSource={this.state.dataSource}
          renderRow={this._renderRow.bind(this)}
        />
      </View>
    );
  }
}

var styles = StyleSheet.create({

  container: {
    flex: 1,
    flexDirection: 'column',
    justifyContent: 'flex-start',
    alignItems: 'stretch',
    padding: 5,
  },
  userinfo: {
    flexDirection: 'row',
    justifyContent: 'center',
    alignItems: 'center',
    margin: 20
  },
  balance: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    alignItems: 'center',
    padding: 10,
    margin: 2,
    borderWidth: 1,
  },
  menu: {
    flexDirection: 'row',
    justifyContent: 'center',
    alignItems: 'center',
    padding: 10,
    margin: 2,
    borderWidth: 1,
  },
  list_view: {
    flexDirection: 'row',
  }
});
