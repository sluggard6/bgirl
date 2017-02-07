import React, {Component} from 'react';

import ScrollableTabView, {DefaultTabBar, } from 'react-native-scrollable-tab-view';

import Main from './main'
import Login from './login'

export default class TabBarView extends Component {
  render() {
    return (
      <ScrollableTabView
        renderTabBar={() => <DefaultTabBar/>}
        tabBarPosition="bottom">
        <Main tabLabel="Main" />
        <Main tabLabel="Group" />
        <Login tabLabel="User" />
      </ScrollableTabView>
    );
  }
}
