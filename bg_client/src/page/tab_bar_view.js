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
			tabIconNames: [require('../images/b_main.png'), require('../images/b_channel.png'), require('../images/b_user.png')],
      tabActiveIconNames: [require('../images/w_main.png'), require('../images/w_channel.png'), require('../images/w_user.png')]
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
        <Main tabLabel="Main" navigator={this.props.navigator}/>
        <Channel tabLabel="频道" navigator={this.props.navigator}/>
        <User tabLabel="User" navigator={this.props.navigator}/>
      </ScrollableTabView>
    );
  }
}
