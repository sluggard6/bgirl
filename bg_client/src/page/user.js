// @flow

import React, {Component} from 'react';

import {
  View,
  Text,
  ListView,
  StyleSheet,
  Navigator,
  TouchableOpacity
} from 'react-native';

import Global from '../utils/global'
import Application from '../utils/application'
import TopBar from '../component/top_bar'
import Login from './login'

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
      isLogin: Global.isLogin
    };
  }

  _renderRow(menu) {
    return(
      <View style={styles.menu}>
        <Text>{menu.text}</Text>
      </View>
    );
  }

  loginPage() {
    this.props.navigator.push({
      component: Login
    })
  }

  render(){
    return (
      <View style={styles.container}>
        <TopBar/>
        <TouchableOpacity onPress={this.loginPage.bind(this)}>
          <View style={styles.userinfo}>
            <Text style={{fontSize: 25}}>Nick</Text>
          </View>
        </TouchableOpacity>
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
    alignItems: 'center',
  },
  userinfo: {
    flexDirection: 'row',
    justifyContent: 'center',
    alignItems: 'center',
    margin: 20,
  },
  balance: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    alignItems: 'center',
    padding: 10,
    margin: 2,
    borderWidth: 1,
    width: Global.size.width-10
  },
  menu: {
    flexDirection: 'row',
    justifyContent: 'center',
    alignItems: 'center',
    padding: 10,
    margin: 2,
    borderWidth: 1,
    width: Global.size.width-10
  },
  list_view: {
    flexDirection: 'row',
    width: Global.size.width
  }
});
