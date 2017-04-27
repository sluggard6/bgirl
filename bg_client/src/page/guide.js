import React, { Component } from 'react';

import {
  Image,
  View,
  ScrollView,
  StyleSheet,
  TouchableOpacity,
  Text,
  Navigator
} from 'react-native';

import Global from '../utils/global';
// import Main from './main'
import TabBarView from './tab_bar_view';


export default class Guide extends Component {

  _onPressButton() {

    this.props.navigator.resetTo({
			component: TabBarView
		})
  }

  render() {
    return (
      <ScrollView
        showsHorizontalScrollIndicator={false}
        contentContainerStyle={styles.contentContainer}
        bounces={false}
        pagingEnabled={true}
        removeClippedSubviews={true}
        horizontal={true}>
        <Image source={Global.guide.image1} style={styles.backgroundImage}>
          <View style={styles.indexContainer}>
            <View style={styles.dian2}/>
            <View style={styles.dian}/>
            <View style={styles.dian}/>
          </View>
        </Image>
        <Image source={Global.guide.image2} style={styles.backgroundImage}>
          <View style={styles.indexContainer}>
            <View style={styles.dian}/>
            <View style={styles.dian2}/>
            <View style={styles.dian}/>
          </View>
        </Image>
        <Image source={Global.guide.image3} style={styles.backgroundImage}>
          <TouchableOpacity onPress={this._onPressButton.bind(this)}>
            <Image source={require('../images/start_button.png')} style={{height: 100, width: 100, margin: 50, resizeMode: Image.resizeMode.contain}} />
          </TouchableOpacity>
          <View style={styles.indexContainer}>
            <View style={styles.dian}/>
            <View style={styles.dian}/>
            <View style={styles.dian2}/>
          </View>
        </Image>
      </ScrollView>
    )
  }
}

var styles = StyleSheet.create({
  contentContainer: {
    width: Global.size.width*3,
    height: Global.size.height,
  },
  backgroundImage: {
    width: Global.size.width,
    height: Global.size.height,
    flexDirection: "column",
    justifyContent: "flex-end",
    alignItems: "center",
    // margin: 5,
    resizeMode: Image.resizeMode.cover,
    overflow: "hidden"
  },
  indexContainer: {
    flexDirection: "row",
    justifyContent: "center",
    alignItems: "center",
    width: 100,
    height: 50,
    backgroundColor: "transparent",
    margin: 30
  },
  dian:{
    height: 5,
    width: 5,
    borderRadius: 5,
    backgroundColor: "white",
    margin: 10,
    opacity:0.5
  },
  dian2:{
    height: 5,
    width: 5,
    borderRadius: 5,
    backgroundColor: "white",
    margin: 10
  }
});
