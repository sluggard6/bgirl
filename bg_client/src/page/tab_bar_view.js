import React, {Component} from 'react';
import {View} from 'react-native'
import ScrollableTabView, {DefaultTabBar, } from 'react-native-scrollable-tab-view';

import Main from './main'
import ChannelTabView from './channel_tab_view'
import User from './user'
import BgirlTabBar from '../component/bgirl_tab_bar'
import LoginWiodow from '../component/windows'
import Global from '../utils/global'
import Application from '../utils/application'

export default class TabBarView extends Component {
  constructor(props) {
		super(props);
		this.state = {
			tabNames: ['美选', '频道', '我的'],
			tabIconNames: [require('../images/b_main.png'), require('../images/b_channel.png'), require('../images/b_user.png')],
      tabActiveIconNames: [require('../images/w_main.png'), require('../images/w_channel.png'), require('../images/w_user.png')]
		};
	}

  componentDidMount() {
    Global.navigator = this.props.navigator
    Application.autoLogin()
  }

  render() {
    return (
      <ScrollableTabView
        renderTabBar={() => <BgirlTabBar
          tabNames={this.state.tabNames}
          tabIconNames={this.state.tabIconNames}
          tabActiveIconNames={this.state.tabActiveIconNames}
        />}
        tabBarPosition="bottom">
        <Main tabLabel="Main" pageName="index"/>
        <ChannelTabView tabLabel="频道"/>
        <User tabLabel="User"/>
      </ScrollableTabView>
    );
  }
}
