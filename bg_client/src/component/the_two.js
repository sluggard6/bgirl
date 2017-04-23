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

export default class TheTwo extends Component {

  constructor(props) {
    super(props);
  }

  renderPic(data){
    if(this.props.square){
      return(
        <Image style={styles.image_square} source={{uri: data.pic.min}} />
      )
    }else{
      return (
        <ViewPic pic={data.pic} component={data.component}/>
      )
    }
  }

  render(){
    return (
      <View style={styles.list_container}>
        <TouchableOpacity onPress={() => this.props.onPress(this.props.data[0].component.id,this.props.data[0].category)}>
          {this.renderPic(this.props.data[0])}
        </TouchableOpacity>
        <TouchableOpacity onPress={() => this.props.onPress(this.props.data[1].component.id,this.props.data[1].category)}>
          {this.renderPic(this.props.data[1])}
        </TouchableOpacity>
      </View>
    );
  }
}

export class ViewPic extends Component {

  constructor(props) {
    super(props);
  }

  render(){
    return (
      <View style={[styles.container,{borderWidth: 1, borderColor: "white"}]}>
        <Image
          style={styles.image}
          source={{uri: this.props.pic.max}}
        />
        <Text style={styles.text}>{this.props.component.des}</Text>
      </View>
    );
  }
}


var styles = StyleSheet.create({

  container: {
    flexDirection: 'column',
    justifyContent: 'space-between',
    flexWrap: 'nowrap',
    alignItems: 'center',
  },

  list_container: {
    flexDirection: 'row',
    justifyContent: 'center',
    flexWrap: 'nowrap',
    alignItems: 'center',
    width: Global.size.width,
  },

  image_square: {
    width: (Global.size.width-4)/2,
    height: (Global.size.width-4)/2,
    borderWidth: 1,
    borderColor: "white"
  },
  
  image: {
    width: (Global.size.width-4)/2,
    height: (Global.size.width-4)/3*2,
  },

  text: {
    textAlign: 'center',
    width: (Global.size.width-4)/2,
    height: 30,
    backgroundColor: "#333740",
    fontSize: 18,
    color: "white"
  }

});
