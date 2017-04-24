// @flow

import React, {Component} from 'react';

import {
  StyleSheet,
  View,
  Image,
  TouchableOpacity,
  Text
} from 'react-native';

import Global from '../utils/global';

export default class ViewChannel extends Component {

  constructor(props) {
    super(props);
  }

  render(){
    return (
      <TouchableOpacity onPress={() => this.props.onPress(this.props.group.key)}>
        <Text style={styles.title}>{this.props.group.name}</Text>
        <View style={styles.container}>
          <Image source={{uri:this.props.group.t1}} style={styles.image_banner}>
            <View style={styles.text_container}>
            </View>
          </Image>
          <View style={styles.list_container}>
            <Image source={{uri:this.props.group.t2}} style={styles.image}/>
            <Image source={{uri:this.props.group.t3}} style={styles.image}/>
          </View>
        </View>
      </TouchableOpacity>
    );
  }
}

var styles = StyleSheet.create({

  container: {
    marginBottom: 20,
  },

  title: {
    width: Global.size.width,
    height: 30,
    fontSize: 16,
    flexDirection: "row",
    justifyContent: "flex-start",
    backgroundColor: "white",
    textAlignVertical: "center",
    paddingLeft: 10
  },

  image_banner: {
    flexDirection: "column",
    justifyContent: 'center',
    alignItems: 'stretch',
    height: Global.size.width/2,
    borderWidth: 1,
    borderColor: "white",
  },

  text_container: {
    flexDirection: "column",
    justifyContent: 'flex-end',
    alignItems: 'center',
  },

  text_name: {
    alignItems: 'flex-end',
    fontSize: 30,
  },

  text_des: {
    alignItems: 'flex-end',
    fontSize: 18,
  },

  list_container: {
    flexDirection: 'row',
    justifyContent: 'center',
    flexWrap: 'nowrap',
    alignItems: 'center',
    width: Global.size.width,
    borderWidth: 1,
    borderColor: "white"
  },

  image: {
    width: (Global.size.width-3)/2,
    height: (Global.size.width-3)/2,
  },

})
