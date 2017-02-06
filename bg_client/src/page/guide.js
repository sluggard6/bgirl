import React, { Component } from 'react';

import {
  AppRegistry,
  Image,
  ScrollView,
  StyleSheet,
  TouchableOpacity,
  Text,
  Navigator
} from 'react-native';

import Util from './utils';
import Main from './main'

let image1 = require('../images/guide_1.jpg');
let image2 = require('../images/guide_2.jpg');
let image3 = require('../images/guide_3.jpg');


export default class Guide extends Component {

  _onPressButton() {

    this.props.navigator.push({
			component: Main
		})
  }

  render() {
    return (
      <ScrollView
        showsHorizontalScrollIndicator={false}
        contentContainerStyle={styles.contentContainer}
        bounces={false}
        pagingEnabled={true}
        horizontal={true}>
        <Image source={image1} style={styles.backgroundImage} resizeMode={Image.resizeMode.contain} />
        <Image source={image2} style={styles.backgroundImage} resizeMode={Image.resizeMode.contain} />
        <Image source={image3} style={styles.backgroundImage} resizeMode={Image.resizeMode.contain}>
          <TouchableOpacity onPress={this._onPressButton.bind(this)} style={styles.runMainButton}>
            <Text>点我跳转</Text>
          </TouchableOpacity>
        </Image>
      </ScrollView>
    )
  }
}

var styles = StyleSheet.create({
  contentContainer: {
    width: Util.size.width*3,
    height: Util.size.height,
  },
  backgroundImage: {
    width: Util.size.width,
    height: Util.size.height,
    flex: 1,
    flexDirection: "row",
    justifyContent: "center",
    alignItems: "flex-end",
    margin: 5,
  },
  runMainButton: {
    flex: 1,
    flexDirection: "row",
    justifyContent: "center",
    alignItems: "center",
    backgroundColor: "blue",
    width: 150,
    height : 50,
    margin: 150,
  }
});
