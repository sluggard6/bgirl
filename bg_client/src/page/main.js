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
import Module from '../utils/module'

// const PIC_URL = "http://192.168.161.35:8290/pic/list?ids=1,2"

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
    justifyContent: 'flex-start',
    flexWrap: 'nowrap',
    alignItems: 'center',
    backgroundColor: '#DFE0E1'
  }

});
