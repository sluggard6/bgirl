// @flow

import React, {Component} from 'react';

import {
  StyleSheet,
  View,
  Image,
  Text,
  TouchableOpacity
} from 'react-native';

import Global from '../utils/global'
import ViewPic from './view_pic'
import FullViewTab from '../page/full_view_tab'

export default class TheTwo extends Component {

  constructor(props) {
    super(props);
  }
  render(){
    return (
      <View style={styles.list_container}>
        <TouchableOpacity onPress={() => this.props.onPress(this.props.data[0].group.id)}>
          <ViewPic pic={this.props.data[0].pic} group={this.props.data[0].group}/>
        </TouchableOpacity>
        <TouchableOpacity onPress={() => this.props.onPress(this.props.data[1].group.id)}>
          <ViewPic pic={this.props.data[1].pic} group={this.props.data[0].group} />
        </TouchableOpacity>
      </View>
    );
  }
}

var styles = StyleSheet.create({

  container: {
    flex: 1,
    flexDirection: 'column',
    justifyContent: 'flex-start',
    flexWrap: 'nowrap',
    alignItems: 'center',
  },

  list_container: {
    flex: 1,
    flexDirection: 'row',
    justifyContent: 'space-around',
    flexWrap: 'nowrap',
    alignItems: 'center',
    width: Global.size.width
  },

});
