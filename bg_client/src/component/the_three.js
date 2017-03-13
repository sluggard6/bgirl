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

export default class TheTwo extends Component {

  constructor(props) {
    super(props);
  }
  render(){
    let image_style = this.props.circle?styles.image_circle:styles.image
    return (
      <View style={styles.list_container}>
        <TouchableOpacity onPress={() => this.props.onPress(this.props.data[0].group.id)}>
          <Image source={{uri:this.props.data[0].pic.min}} style={image_style}/>
        </TouchableOpacity>
        <TouchableOpacity onPress={() => this.props.onPress(this.props.data[1].group.id)}>
          <Image source={{uri:this.props.data[1].pic.min}} style={image_style}/>
        </TouchableOpacity>
        <TouchableOpacity onPress={() => this.props.onPress(this.props.data[2].group.id)}>
          <Image source={{uri:this.props.data[2].pic.min}} style={image_style}/>
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
    marginBottom: 1,
    width: Global.size.width
  },

  image: {
    width: (Global.size.width-5)/3,
    height: (Global.size.width-5)/3,
  },

  image_circle: {
    width: (Global.size.width-5)/3,
    height: (Global.size.width-5)/3,
    borderRadius: (Global.size.width-5)/6
  }
});
