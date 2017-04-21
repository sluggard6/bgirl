import React, {Component} from 'react';

import {
  View,
  Text,
  ListView,
  StyleSheet,
  Navigator
} from 'react-native'

import Page from '../component/page'
import Global from '../utils/global'
import Application from '../utils/application'
import Http from '../utils/http'
import TopBar from '../component/top_bar'

let temp = [];

export default class Main extends Component {

  constructor(props) {
    super(props);
  }

  render() {
    return (
      <View style={styles.container}>
        <TopBar/>
        <Page pageName={this.props.pageName}/>
      </View>
    )
  }
}

var styles = StyleSheet.create({

  container: {
    flex: 1,
    flexDirection: 'column',
    justifyContent: 'center',
    flexWrap: 'nowrap',
    alignItems: 'center',
    backgroundColor: '#e0e0e0'
  }

});
