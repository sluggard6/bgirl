import React, {Component} from 'react';
import ScrollableTabView, {DefaultTabBar, } from 'react-native-scrollable-tab-view';

import Main from './main'
import Channel from './channel'
import User from './user'
import BgirlTabBar from '../component/bgirl_tab_bar'

export default class TabBarView extends Component {
  constructor(props) {
		super(props);

		this.state = {
			tabNames: ['美选', '频道', '我的'],
			tabIconNames: ['../images/b_main.png', '../images/b_channel.png', '../images/b_user.png'],
      tabActiveIconNames: ['../images/w_main.png', '../images/w_channel.png', '../images/w_user.png']
		};
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
        <Main tabLabel="Main"/>
        <Channel tabLabel="频道"/>
        <User tabLabel="User"/>
      </ScrollableTabView>
    );
  }
}
