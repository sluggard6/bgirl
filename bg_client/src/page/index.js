import React, { Component } from 'react';
import {
  AppRegistry,
  Navigator,
} from 'react-native';

import Guide from './guide';
import Main from './main';



const defaultRoute = {
  component: Guide
};

class Index extends Component {
  _renderScene(route, navigator) {
    let Component = route.component;
    console.log(Component);
    return (
      <Component {...route.params} navigator={navigator} />
    );
  }

  render() {
    return (
      <Navigator
        initialRoute={defaultRoute}
        renderScene={this._renderScene}
      />
    );
  }
}



AppRegistry.registerComponent('pv_client', () => Index );
