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
        <View style={styles.container}>
          <Image source={{uri:this.props.group.t1}} style={styles.image_banner}>
            <View style={styles.text_container}>
              <Text style={styles.text_name}>{this.props.group.name}</Text>
              <Text style={styles.text_des}>{this.props.group.description}</Text>
            </View>
          </Image>
          <View style={styles.list_container}>
            <Image source={{uri:this.props.group.t2}} style={styles.image}/>
            <Image source={{uri:this.props.group.t3}} style={styles.image}/>
            <Image source={{uri:this.props.group.t4}} style={styles.image}/>
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

  image_banner: {
    flexDirection: "column",
    justifyContent: 'center',
    alignItems: 'stretch',
    height: (Global.size.width-2)/3,
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
    width: Global.size.width
  },

  image: {
    width: (Global.size.width-2)/3,
    height: (Global.size.width-2)/3,
    borderWidth: 1,
    borderColor: "white"
  },

})
