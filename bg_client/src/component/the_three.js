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
        <TouchableOpacity onPress={() => this.props.onPress(this.props.data[0].component.id,this.props.data[0].category)}>
          <Image source={{uri:this.props.data[0].pic.min}} style={image_style}/>
        </TouchableOpacity>
        <TouchableOpacity onPress={() => this.props.onPress(this.props.data[1].component.id,this.props.data[1].category)}>
          <Image source={{uri:this.props.data[1].pic.min}} style={image_style}/>
        </TouchableOpacity>
        <TouchableOpacity onPress={() => this.props.onPress(this.props.data[2].component.id,this.props.data[2].category)}>
          <Image source={{uri:this.props.data[2].pic.min}} style={image_style}/>
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

  image: {
    width: (Global.size.width-2)/3-1,
    height: (Global.size.width-2)/3-1,
    borderWidth: 1,
    borderColor: "white"
  },

  image_circle: {
    width: (Global.size.width-5)/3-10,
    height: (Global.size.width-5)/3-10,
    borderRadius: (Global.size.width-5)/6,
    borderWidth: 2,
    borderColor: "white",
    margin: 4
  }
});
