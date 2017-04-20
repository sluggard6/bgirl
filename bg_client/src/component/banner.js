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


  render(){
    return (
      <View style={styles.list_container}>
      <TouchableOpacity onPress={() => this.props.onPress(this.props.data[0].component.id, this.props.data[0].category)}>
        <Image source={{uri:this.props.data[0].pic.min}} style={styles.container}>
          <View style={styles.text_container}>
            <View style={styles.view_opacity}/>
            <Text style={styles.text_name}>{this.props.data[0].component.name}</Text>
          </View>
        </Image>
      </TouchableOpacity>
      </View>
    );
  }
}

var styles = StyleSheet.create({

  list_container: {
    flexDirection: 'row',
    justifyContent: 'center',
    flexWrap: 'nowrap',
    alignItems: 'center',
    width: Global.size.width
  },

  container: {
    flexDirection: "column",
    justifyContent: 'flex-end',
    alignItems: 'center',
    height: 255,
    width: Global.size.width-4,
    borderWidth: 1,
    borderColor: "white"
  },

  text_container: {
    flexDirection: "row",
    justifyContent: 'flex-start',
    alignItems: 'center',
    height: 60,
    backgroundColor:'transparent',
  },

  view_opacity: {
    width: Global.size.width,
    height: 60,
    opacity:0.5,
    backgroundColor:'#AEAEAE',
  },

  text_name: {
    position: 'absolute',
    color: 'white',
    paddingLeft: 10,
    fontSize: 22,
  },

})
