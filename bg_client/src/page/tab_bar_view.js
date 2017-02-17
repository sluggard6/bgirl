import React, {Component} from 'react';

import ScrollableTabView, {DefaultTabBar, } from 'react-native-scrollable-tab-view';

import Main from './main'
import Channel from './channel'
import User from './user'

export default class TabBarView extends Component {
  render() {
    return (
      <ScrollableTabView
        renderTabBar={() => <DefaultTabBar/>}
        tabBarPosition="bottom">
        <Main tabLabel="Main" />
        <Channel tabLabel="频道" />
        <User tabLabel="User" />
      </ScrollableTabView>
    );
  }
}
