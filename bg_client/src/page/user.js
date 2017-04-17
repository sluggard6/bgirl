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
import ChannelPackage from '../utils/channel_info'

var user_info_menu = [
  {text:'充值VIP', img:require('../images/chongzhi.png'), actionPath:Pay},
  {text:'关于我们', img:require('../images/guanyuwomen.png'), actionPath:Pay},
  {text:'免责申明', img:require('../images/mianzeshenming.png'), actionPath:Pay},
  {text:'帮助'+ChannelPackage.CHANNEL, img:require('../images/bangzhu.png'), actionPath:Pay}
  // {text:'我的下载', actionType:'innerView', actionPath:'downloaded'},
  // {text:'未读消息', actionType:'innerView', actionPath:'downloaded'},
  // {text:'每日任务', actionType:'innerView', actionPath:'downloaded'},
  // {text:'个人设置', actionType:'innerView', actionPath:'downloaded'}
]

export default class User extends Component {
  constructor(props) {
    super(props)
    this.goAction.bind(this)
    const ds = new ListView.DataSource({
      rowHasChanged: (row1, row2) => row1 !== row2,
    });
    this.state = {
      dataSource: ds.cloneWithRows(user_info_menu),
    };
  }

  _renderRow(menu) {
    return(
      <TouchableOpacity onPress={() => {
        this.goAction(menu.actionPath)
        }}>
        <View style={styles.menu}>
          <View style={{justifyContent: 'center', alignItems: 'center', flexDirection: 'row', height: 50}}>
          <Image source={menu.img} style={styles.menu_logo}/>
          <Text style={styles.menu_text}>{menu.text}</Text>
          </View>
          <Image source={require('../images/jiantou.png')} style={styles.menu_taget}/>
        </View>
      </TouchableOpacity>
    );
  }

  goAction(actionPath) {
    Global.navigator.push({
      component: actionPath
    })
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
      let payInfo = "普通用户"
      return (
        <View style={styles.userinfo}>
          <Image source={require('../images/touxiang.png')} style={{height: 80, resizeMode: Image.resizeMode.contain, marginLeft: 100/Global.pr, marginRight: 100/Global.pr}}/>
          <View style={styles.user_nick}>
            <Text style={{fontSize: 20, textAlign: 'center', marginBottom: 5}}>{nick}</Text>
            <TouchableOpacity onPress={this.checkVip.bind(this)}>
              <View style={styles.vip_info}>
                <Image source={require('../images/huangguan0.png')} style={{height: 20, width: 20, marginRight: 10, resizeMode: Image.resizeMode.contain}}/>
                <Text style={{fontSize: 18, textAlign: 'center'}}>{payInfo}</Text>
              </View>
            </TouchableOpacity>
          </View>
        </View>
      )
    }else{
      return (
        <View style={{backgroundColor: "white"}}>
          <TouchableOpacity onPress={this.loginPage.bind(this)}>
            <View style={[styles.userinfo,{justifyContent: 'center'}]}>
              <Image source={require('../images/touxiang.png')} style={{height: 80, resizeMode: Image.resizeMode.contain}}/>
            </View>
          </TouchableOpacity>
          <View style={styles.balance}>
            <TouchableOpacity onPress={this.loginPage.bind(this)}>
              <Text style={[styles.button,{backgroundColor: '#ff4563'}]}>登录</Text>
            </TouchableOpacity>
            <TouchableOpacity onPress={this.registerPage.bind(this)}>
              <Text style={[styles.button,{backgroundColor: '#ffa145'}]}>注册</Text>
            </TouchableOpacity>
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
    justifyContent: 'flex-start',
    alignItems: 'center',
    margin: 20,
    width: Global.size.width-40
  },
  user_nick: {
  },
  vip_info: {
    flexDirection: 'row',
    justifyContent: 'center',
    alignItems: 'center'
  },
  button: {
    fontSize: 18,
    height: 40,
    width: Global.size.width/2-20,
    borderRadius: 5,
    textAlign: 'center',
    textAlignVertical: 'center'
  },
  balance: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    alignItems: 'center',
    padding: 10,
    margin: 2,
    width: Global.size.width-10
  },
  menu: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    alignItems: 'center',
    padding: 10,
    margin: 2,
    borderTopWidth: 1,
    borderBottomWidth: 1,
    height: 60,
    borderColor: "#e0e0e0",
    width: Global.size.width-10
  },
  menu_text:{
    textAlign: 'center',
    fontSize: 18,
    width: 150
  },
  menu_logo: {
    height: 40,
    resizeMode: Image.resizeMode.contain
  },
  menu_taget: {
    height: 30,
    width: 30,
    resizeMode: Image.resizeMode.contain
  },
  list_view: {
    flexDirection: 'row',
    width: Global.size.width
  }
});
