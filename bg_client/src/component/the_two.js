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

  renderPic(data){
    if(this.props.square){
      <Image style={styles.image} source={{uri: data.pic.max}} />
    }else{
      return (
        <ViewPic pic={data.pic} component={data.component}/>
      )
    }
  }

  render(){
    return (
      <View style={styles.list_container}>
        <TouchableOpacity onPress={() => this.props.onPress(this.props.data[0].component.id)}>
          {this.renderPic(this.props.data[0])}
        </TouchableOpacity>
        <TouchableOpacity onPress={() => this.props.onPress(this.props.data[1].component.id)}>
          {this.renderPic(this.props.data[1])}
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
    width: Global.size.width,
    marginBottom: 10
  },
  image: {
    width: (Global.size.width-20)/2,
    height: (Global.size.width-20)/2,
    borderWidth: 1,
    borderColor: "white"
  },

});
