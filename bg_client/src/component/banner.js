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
import FullViewTab from '../page/full_view_tab'

export default class Banner extends Component {

  constructor(props) {
    super(props);
  }

  _onPressButton() {
    this.props.navigator.push({
			component: FullViewTab,
      groupId: this.props.data[0].group.id
		})
  }

  render(){
    return (
      <TouchableOpacity onPress={this.props.onPress}>
        <Image source={{uri:this.props.data[0].pic.min}} style={styles.container}>
          <View style={styles.text_container}>
            <Text style={styles.text_name}>{this.props.data[0].des}</Text>
          </View>
        </Image>
      </TouchableOpacity>
    );
  }
}

var styles = StyleSheet.create({

  container: {
    flexDirection: "column",
    justifyContent: 'flex-end',
    alignItems: 'stretch',
    height: 255,
    width: Global.size.width,
    borderWidth: 1,
    borderColor: "white",
    marginBottom:10,
  },

  text_container: {
    flexDirection: "row",
    justifyContent: 'flex-end',
    alignItems: 'center',
    paddingRight: 10,
    height: 60,
    opacity:0.5,
    backgroundColor:'#AEAEAF',
    borderColor: "black"
  },

  text_name: {
    alignItems: 'flex-end',
    color: 'white',
    fontSize: 22,
  },

  text_des: {
    alignItems: 'flex-end',
    fontSize: 18,
  }
})
