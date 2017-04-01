// @flow

import React, {Component} from 'react';

import {
  View,
  Text,
  Image,
  Button,
  ListView,
  StyleSheet,
  Navigator,
  TouchableOpacity,
  ToastAndroid
} from 'react-native';

import Global from '../utils/global'
import Application from '../utils/application'
import TopBar from '../component/top_bar'
import Login from './login'
import RegisterPhone from './register_phone'
import Pay from './pay'

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

  loginPage() {
    Global.navigator.push({
      component: Login
    })
  }

  registerPage() {
    Global.navigator.push({
      component: RegisterPhone
    })
  }
  

  checkVip() {
    if(Application.isVip()) {
      ToastAndroid.show("您已经是至尊VIP了", ToastAndroid.CENTER)
    }else{
      Global.navigator.push({
        component: Pay
      })
    }
  }

  getSecPhone(){
    let phone = Global.user.phone
    let ps = phone.split("")
    ps[ps.length - 5] = '*'
    ps[ps.length - 6] = '*'
    ps[ps.length - 7] = '*'
    ps[ps.length - 8] = '*'
    return ps.join("")
  }

  getNick() {
    if(Global.isLogin) {
      let nick = Global.user.nick==null?this.getSecPhone():Global.user.nick
      return (
        <View>
        <TouchableOpacity>
          <View style={styles.userinfo}>
            <Text style={{fontSize: 25}}>{nick}</Text>
          </View>
        </TouchableOpacity>        
        <View style={styles.balance}>
          <TouchableOpacity onPress={this.checkVip.bind(this)}>
           <Text style={{color: 'red'}}>至尊VIP</Text>
          </TouchableOpacity>        
          <TouchableOpacity onPress={Application.unSupport}>
            <Text>0金币</Text>
          </TouchableOpacity>        
        </View>
        </View>
      )
    }else{
      return (
        <View>
          <TouchableOpacity onPress={this.loginPage.bind(this)}>
            <View style={styles.userinfo}>
              <Image source={require('../images/touxiang.png')} style={{height: 80, resizeMode: Image.resizeMode.contain}}/>
            </View>
          </TouchableOpacity>
          <View style={styles.balance}>
            <Button
              onPress={this.loginPage.bind(this)}
              style={styles.button}
              title="登录"
              color="#ff4563"/>
            <Button
              onPress={this.registerPage.bind(this)}
              style={styles.button}
              color="#ffa145"
              title="注册" />
          </View>
        </View>
      )
    }
  }

  render(){
    return (
      <View style={styles.container}>
        <TopBar/>
        {this.getNick()}
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
  button: {
    fontSize: 28,
    width: 80,

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
