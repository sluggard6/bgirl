import React, {Component} from 'react';

import ScrollableTabView, {DefaultTabBar, } from 'react-native-scrollable-tab-view';

import Main from './main'
import User from './user'

export default class TabBarView extends Component {
  render() {
    return (
      <ScrollableTabView
        renderTabBar={() => <DefaultTabBar/>}
        tabBarPosition="bottom">
        <Main tabLabel="Main" />
        <User tabLabel="User" />
      </ScrollableTabView>
    );
  }
}
