import React, { Component } from 'react';

import {
  Image,
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
        <Image source={Global.guide.image1} style={styles.backgroundImage}/>
        <Image source={Global.guide.image2} style={styles.backgroundImage}/>
        <Image source={Global.guide.image3} style={styles.backgroundImage}>
          <TouchableOpacity onPress={this._onPressButton.bind(this)}>
            <Image source={require('../images/start_button.png')} style={{height: 100, width: 100, margin: 150, resizeMode: Image.resizeMode.contain}} />
          </TouchableOpacity>
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
    flexDirection: "row",
    justifyContent: "center",
    alignItems: "flex-end",
    // margin: 5,
    resizeMode: Image.resizeMode.cover,
    overflow: "hidden"
  }
});
